"""Finite Linux/GitHub-CI-only memory gate. No permissive unknown fallback."""
from datetime import datetime, timezone
import hashlib
import os
from pathlib import Path, PurePosixPath
import re
import sys
import math

BUDGET_MIB = 5120
RESERVE_MIB = 2048
MIB = 1024 ** 2


def utc():
    return datetime.now(timezone.utc).isoformat()


def actual_context():
    return dict(platform=sys.platform, CI=os.environ.get('CI'),
                GITHUB_ACTIONS=os.environ.get('GITHUB_ACTIONS'),
                RUNNER_OS=os.environ.get('RUNNER_OS'),
                GITHUB_RUN_ID=os.environ.get('GITHUB_RUN_ID'),
                GITHUB_JOB=os.environ.get('GITHUB_JOB'), GITHUB_SHA=os.environ.get('GITHUB_SHA'))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def context_check(context):
    require(context.get('platform') == 'linux', 'CI-only budget forbidden on Windows/non-Linux')
    require(context.get('CI') == 'true' and context.get('GITHUB_ACTIONS') == 'true'
            and context.get('RUNNER_OS') == 'Linux', 'requires explicit Linux GitHub CI context')
    require(isinstance(context.get('GITHUB_RUN_ID'), str) and context['GITHUB_RUN_ID'].isdigit(),
            'missing actual CI run identity')
    require(isinstance(context.get('GITHUB_JOB'), str) and context['GITHUB_JOB'], 'missing CI job identity')
    require(isinstance(context.get('GITHUB_SHA'), str) and
            re.fullmatch('[0-9a-fA-F]{40}', context['GITHUB_SHA']), 'missing actual CI SHA')


def absolute_posix(value):
    require(type(value) is str and value.startswith('/') and '..' not in value.split('/'),
            'unsafe kernel-reported path')
    return PurePosixPath(value)


def mount_unescape(value):
    return re.sub(r'\\([0-7]{3})', lambda m: chr(int(m[1], 8)), value)


def sample(context=None, read_bytes=None):
    """Production calls use real OS reads; dependency injection is only a Python test fixture."""
    context = actual_context() if context is None else context
    read_bytes = (lambda name: Path(name).read_bytes()) if read_bytes is None else read_bytes
    row = dict(schema='C31_CI2_RESOURCE_PREFLIGHT_V1', startedUTC=utc(), context=context,
               budgetMiB=BUDGET_MIB, reserveMiB=RESERVE_MIB,
               requiredHeadroomBytes=(BUDGET_MIB + RESERVE_MIB) * MIB,
               observationComplete=False, gatePassed=False, fileReads=[],
               memAvailableBytes=None, effectiveHeadroomBytes=None, cgroupVersion=None, cgroups=[])
    try:
        context_check(context)
        def read(name, logical=None):
            data = read_bytes(str(name))
            require(type(data) is bytes, 'resource reader must return raw bytes')
            row['fileReads'].append(dict(path=str(name), logicalPath=logical or str(name).replace('/proc', '$PROC', 1), bytes=len(data),
                                        sha256=hashlib.sha256(data).hexdigest()))
            return data.decode('ascii', errors='strict')
        mem = read('/proc/meminfo')
        values = re.findall(r'(?m)^MemAvailable:\s*(\d+)\s+kB\s*$', mem)
        require(len(values) == 1, 'missing/duplicate/unknown MemAvailable')
        row['memAvailableBytes'] = int(values[0]) * 1024
        groups = read('/proc/self/cgroup').splitlines()
        v2 = [s.split(':', 2)[2] for s in groups if s.startswith('0::')]
        if not v2 and any('memory' in s.split(':')[1].split(',') for s in groups if s.count(':') == 2):
            row['cgroupVersion'] = 1
            raise ValueError('cgroup v1 memory accounting unsupported: refuse, do not assume host capacity')
        require(len(v2) == 1, 'missing/ambiguous cgroup v2 membership')
        row['cgroupVersion'] = 2
        group = absolute_posix(v2[0])
        mounts = []
        for line in read('/proc/self/mountinfo').splitlines():
            left, sep, right = line.partition(' - ')
            if sep and right.split() and right.split()[0] == 'cgroup2':
                fields = left.split()
                require(len(fields) >= 6, 'malformed cgroup2 mount')
                mounts.append((absolute_posix(mount_unescape(fields[3])),
                               absolute_posix(mount_unescape(fields[4]))))
        require(len(mounts) == 1, 'missing/ambiguous cgroup2 mount: refuse unknown hierarchy')
        root, mount = mounts[0]
        require(root == PurePosixPath('/'),
                'delegated mount hides higher cgroup limits: unknown effective ceiling refused')
        require(group.is_relative_to(root), 'cgroup membership/mount root mismatch')
        current = mount / group.relative_to(root)
        row['cgroupMountRoot'] = str(root)
        row['cgroupMountPoint'] = str(mount)
        row['cgroupMembership'] = str(group)
        headrooms = [row['memAvailableBytes']]
        for depth in range(65):
            require(depth < 64, 'cgroup ancestry exceeds bounded inspection')
            logical = '$CGROUP_ANCESTOR_' + str(depth)
            limit_text = read(current / 'memory.max', logical + '/memory.max').strip()
            usage_text = read(current / 'memory.current', logical + '/memory.current').strip()
            require(limit_text == 'max' or re.fullmatch('[0-9]+', limit_text), 'unknown memory.max')
            require(re.fullmatch('[0-9]+', usage_text), 'unknown memory.current')
            limit = None if limit_text == 'max' else int(limit_text)
            usage = int(usage_text)
            events = {}
            for line in read(current / 'memory.events', logical + '/memory.events').splitlines():
                parts = line.split()
                require(len(parts) == 2 and re.fullmatch('[0-9]+', parts[1]) and
                        parts[0] not in events, 'malformed/duplicate cgroup memory.events')
                events[parts[0]] = int(parts[1])
            require('oom' in events and 'oom_kill' in events, 'missing cgroup OOM counters')
            remaining = None if limit is None else max(0, limit - usage)
            if remaining is not None:
                headrooms.append(remaining)
            row['cgroups'].append(dict(path=str(current), logicalPath=logical, memoryMaxRaw=limit_text,
                memoryMaxBytes=limit, memoryCurrentBytes=usage, headroomBytes=remaining,
                limitUnlimited=limit is None, memoryEvents=events))
            if current == mount:
                break
            require(current.is_relative_to(mount) and current.parent != current,
                    'cgroup traversal escaped visible mount')
            current = current.parent
        row['effectiveHeadroomBytes'] = min(headrooms)
        row['observationComplete'] = True
        row['gatePassed'] = row['effectiveHeadroomBytes'] >= row['requiredHeadroomBytes']
        if not row['gatePassed']:
            row['failure'] = 'INSUFFICIENT_MEASURED_EFFECTIVE_HEADROOM'
    except Exception as error:
        row['failureType'] = type(error).__name__
        row['failure'] = str(error)
    row['finishedUTC'] = utc()
    return row


def classify(result, stderr, before, after, stdout=''):
    """Observed termination, not a mathematical verdict or speculative OS attribution."""
    if not native_metadata_complete(result):
        return 'NATIVE_STARTUP_OR_RESULT_METADATA_INCOMPLETE'
    if result['timedOut']:
        return 'WRAPPER_TIMEOUT_KILLED_OWN_CHILD'
    code = result['exitCode']
    internal = ('lean::memory_exception' in stderr and 'excessive memory consumption' in stderr)
    if code == -6 and internal:
        return 'LEAN_INTERNAL_MEMORY_EXCEPTION_SIGABRT_NOT_OS_OOM_PROOF'
    if code == -9:
        if before.get('observationComplete') and after.get('observationComplete'):
            old = {r['path']: r['memoryEvents']['oom_kill'] for r in before['cgroups']}
            if any(r['path'] in old and r['memoryEvents']['oom_kill'] > old[r['path']]
                   for r in after['cgroups']):
                return 'SIGKILL_WITH_CGROUP_OOM_EVENT_CORRELATION_NOT_PID_ATTRIBUTION_PROOF'
        return 'PROCESS_SIGKILL_UNATTRIBUTED_NOT_INTERNAL_CAP_CLASSIFIED'
    if code == 0:
        return 'CONTRADICTORY_ZERO_EXIT_MEMORY_EXCEPTION' if internal else 'PROCESS_EXIT_ZERO'
    if internal:
        return 'LEAN_INTERNAL_MEMORY_EXCEPTION_NONZERO_NOT_OS_OOM_PROOF'
    if re.search(r'(^|\n).*\berror:', stderr + '\n' + stdout):
        return 'LEAN_REPORTED_ERROR_API_OR_IMPLEMENTATION_UNRESOLVED'
    return 'PROCESS_NONZERO_UNCLASSIFIED'


def native_metadata_complete(result):
    if not isinstance(result, dict) or type(result.get('exitCode')) is not int or \
            type(result.get('PID')) is not int or result['PID'] <= 0 or \
            type(result.get('timedOut')) is not bool or \
            type(result.get('wallSeconds')) not in (int, float) or \
            not math.isfinite(result['wallSeconds']) or result['wallSeconds'] < 0:
        return False
    for key in ('stdoutSHA256', 'stderrSHA256'):
        if not isinstance(result.get(key), str) or re.fullmatch('[0-9a-f]{64}', result[key]) is None:
            return False
    try:
        return all(type(result.get(key)) is str and
                   datetime.fromisoformat(result[key]).utcoffset() is not None
                   for key in ('startedUTC', 'finishedUTC'))
    except ValueError:
        return False


def validate_snapshot(row, require_pass=True):
    """Independently recheck computed accounting; incomplete/unknown is never green."""
    require(row.get('schema') == 'C31_CI2_RESOURCE_PREFLIGHT_V1', 'resource schema')
    context_check(row.get('context', {}))
    require(row.get('observationComplete') is True, 'resource observation incomplete')
    require(row.get('budgetMiB') == BUDGET_MIB and row.get('reserveMiB') == RESERVE_MIB,
            'finite budget/reserve changed')
    require(row.get('cgroupVersion') == 2, 'only measured v2 accounting supported')
    minimum = (BUDGET_MIB + RESERVE_MIB) * MIB
    require(row.get('requiredHeadroomBytes') == minimum, 'headroom threshold changed')
    available = row.get('memAvailableBytes')
    require(type(available) is int and available >= 0, 'missing actual MemAvailable')
    groups = row.get('cgroups')
    require(isinstance(groups, list) and len(groups) > 0, 'missing cgroup accounting')
    paths = set(); headrooms = [available]
    for group in groups:
        require(set(('path', 'logicalPath', 'memoryMaxRaw', 'memoryMaxBytes', 'memoryCurrentBytes',
                     'headroomBytes', 'limitUnlimited', 'memoryEvents')) <= set(group),
                'missing cgroup observation field')
        path = group.get('path')
        require(type(path) is str and path not in paths, 'missing/duplicate cgroup path')
        paths.add(path)
        maximum, current = group.get('memoryMaxBytes'), group.get('memoryCurrentBytes')
        require(type(current) is int and current >= 0, 'missing actual cgroup current')
        if maximum is None:
            require(group.get('memoryMaxRaw') == 'max' and group.get('limitUnlimited') is True
                    and group.get('headroomBytes') is None, 'unknown/unlimited limit confusion')
        else:
            require(type(maximum) is int and maximum >= 0 and group.get('memoryMaxRaw') == str(maximum)
                    and group.get('limitUnlimited') is False, 'invalid actual cgroup max')
            remaining = max(0, maximum - current)
            require(group.get('headroomBytes') == remaining, 'cgroup subtraction mismatch')
            headrooms.append(remaining)
        events = group.get('memoryEvents')
        require(isinstance(events, dict) and 'oom' in events and 'oom_kill' in events
                and all(type(x) is int and x >= 0 for x in events.values()), 'missing actual OOM counters')
    require(row.get('effectiveHeadroomBytes') == min(headrooms), 'effective headroom formula changed')
    require(type(row.get('gatePassed')) is bool and row['gatePassed'] == (min(headrooms) >= minimum),
            'forged/inconsistent resource gate')
    reads = row.get('fileReads')
    require(isinstance(reads, list) and len(reads) == 3 + 3 * len(groups), 'missing resource-file reads')
    require(len({r['path'] for r in reads}) == len(reads), 'duplicate resource read')
    for read in reads:
        require(type(read.get('bytes')) is int and read['bytes'] >= 0 and
                re.fullmatch('[0-9a-f]{64}', read.get('sha256', '')) and
                type(read.get('logicalPath')) is str, 'resource raw-hash/logical binding absent')
    require({r['path'] for r in reads} == {'/proc/meminfo', '/proc/self/cgroup', '/proc/self/mountinfo'} |
            {str(PurePosixPath(g['path']) / suffix) for g in groups
             for suffix in ('memory.max', 'memory.current', 'memory.events')},
            'actual resource read set incomplete')
    require([g['logicalPath'] for g in groups] == ['$CGROUP_ANCESTOR_' + str(i) for i in range(len(groups))],
            'logical cgroup coordinates changed')
    require({r['logicalPath'] for r in reads} == {'$PROC/meminfo', '$PROC/self/cgroup', '$PROC/self/mountinfo'} |
            {g['logicalPath'] + '/' + suffix for g in groups
             for suffix in ('memory.max', 'memory.current', 'memory.events')},
            'public-safe logical read coordinates incomplete')
    root = absolute_posix(row.get('cgroupMountRoot', ''))
    mount = absolute_posix(row.get('cgroupMountPoint', ''))
    member = absolute_posix(row.get('cgroupMembership', ''))
    require(root == PurePosixPath('/'), 'hidden cgroup ancestor limits unsupported')
    require(member.is_relative_to(root), 'membership/mount root inconsistent')
    chain = [PurePosixPath(g['path']) for g in groups]
    require(chain[0] == mount / member.relative_to(root) and chain[-1] == mount and
            len(chain) <= 64 and all(a.parent == b for a, b in zip(chain, chain[1:])),
            'incomplete visible cgroup ancestor chain')
    for key in ('startedUTC', 'finishedUTC'):
        require(type(row.get(key)) is str and datetime.fromisoformat(row[key]).utcoffset() is not None,
                'resource timestamp absent')
    if require_pass:
        require(row['gatePassed'] is True, 'insufficient measured headroom')
    return True
