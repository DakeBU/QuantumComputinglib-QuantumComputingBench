"""CI4: mandatory self-only reserved-init namespace contract; no PID1 interface read."""
import hashlib
from datetime import datetime
import os
from pathlib import Path, PurePosixPath
import re

INIT_CGROUP_INODE = 0xEFFFFFFB
ROOT_NA = 'DOCUMENTED_TRUE_ROOT_NOT_APPLICABLE_NOT_UNLIMITED'
DOC = 'https://docs.kernel.org/admin-guide/cgroup-v2.html#memory-interface-files'
MEMORY_FILES = ('memory.max', 'memory.current', 'memory.events')


def bind_common(module):
    # Only unchanged technical helpers; no source/math/axiom reconstruction is imported.
    for name in ('utc', 'context_check', 'require', 'actual_context', 'absolute_posix',
                 'mount_unescape', 'classify', 'native_metadata_complete', 'BUDGET_MIB', 'RESERVE_MIB', 'MIB'):
        globals()[name] = getattr(module, name)


def sample(context=None, read_bytes=None, read_link=None):
    context = actual_context() if context is None else context
    read_bytes = (lambda p: Path(p).read_bytes()) if read_bytes is None else read_bytes
    read_link = os.readlink if read_link is None else read_link
    row = dict(schema='C31_CI4_RESOURCE_SELF_NAMESPACE_V1', startedUTC=utc(), context=context,
        budgetMiB=5120, reserveMiB=2048, requiredHeadroomBytes=7168 * MIB,
        observationComplete=False, gatePassed=False, fileReads=[], namespaceReads=[], readAttempts=[],
        memAvailableBytes=None, effectiveHeadroomBytes=None, cgroupVersion=None, cgroups=[],
        rootObservation=None, failedReadLogicalPath=None, failedReadAtVerifiedMountRoot=None)
    try:
        context_check(context)
        def observe(path, logical, verified_root=None, link=False):
            attempt = dict(path=str(path), logicalPath=logical,
                operation='READLINK_UTF8' if link else 'READ_FILE_BYTES',
                atVerifiedMountRoot=verified_root, attemptedUTC=utc(), status='ATTEMPTED')
            row['readAttempts'].append(attempt)
            try:
                value = read_link(str(path)) if link else read_bytes(str(path))
                require(type(value) is str if link else type(value) is bytes, 'invalid resource-reader type')
                data = value.encode('utf-8') if link else value
                receipt = dict(path=str(path), logicalPath=logical, bytes=len(data),
                    sha256=hashlib.sha256(data).hexdigest(), atVerifiedMountRoot=verified_root,
                    hashScope='READLINK_TARGET_UTF8' if link else 'ORIGINAL_FILE_BYTES')
                row['namespaceReads' if link else 'fileReads'].append(receipt)
                attempt.update(status='READ_OK', sha256=receipt['sha256'], bytes=len(data), finishedUTC=utc())
                return value if link else data.decode('ascii', errors='strict')
            except Exception as error:
                attempt.update(status='READ_ERROR', exceptionType=type(error).__name__,
                    errno=getattr(error, 'errno', None), error=str(error), finishedUTC=utc())
                row['failedReadLogicalPath'] = logical
                row['failedReadAtVerifiedMountRoot'] = verified_root
                raise
        values = re.findall(r'(?m)^MemAvailable:\s*(\d+)\s+kB\s*$',
                            observe('/proc/meminfo', '$PROC/meminfo'))
        require(len(values) == 1, 'unknown/duplicate MemAvailable')
        row['memAvailableBytes'] = int(values[0]) * 1024
        membership = observe('/proc/self/cgroup', '$PROC/self/cgroup').splitlines()
        v2 = [s.split(':', 2)[2] for s in membership if s.startswith('0::')]
        require(len(v2) == 1, 'V1_OR_UNKNOWN_OR_AMBIGUOUS_CGROUP_MEMBERSHIP')
        member = absolute_posix(v2[0])
        row['cgroupVersion'] = 2
        mounts = []
        for line in observe('/proc/self/mountinfo', '$PROC/self/mountinfo').splitlines():
            left, sep, right = line.partition(' - ')
            if sep and right.split() and right.split()[0] == 'cgroup2':
                f = left.split(); require(len(f) >= 6, 'malformed cgroup2 mount')
                mounts.append((absolute_posix(mount_unescape(f[3])), absolute_posix(mount_unescape(f[4]))))
        require(len(mounts) == 1, 'UNKNOWN_OR_AMBIGUOUS_CGROUP2_MOUNT')
        root, mount = mounts[0]
        row.update(cgroupMountRoot=str(root), cgroupMountPoint=str(mount), cgroupMembership=str(member))
        require(root == PurePosixPath('/'), 'HIDDEN_DELEGATED_MOUNT_ROOT_REFUSED')
        ns_values = []
        for path, logical in (('/proc/self/ns/cgroup', '$PROC/self/ns/cgroup'),):
            text = observe(path, logical, link=True)
            found = re.fullmatch(r'cgroup:\[(\d+)\]', text)
            require(found is not None, 'UNKNOWN_CGROUP_NAMESPACE_LINK_FORMAT')
            ns_values.append(int(found[1]))
        row['namespaceObservation'] = dict(selfInode=ns_values[0], requiredInitInode=INIT_CGROUP_INODE,
            policy='SELF_ONLY_RESERVED_INIT_V1',
            pid1Observation=dict(status='NOT_REQUESTED_NOT_REQUIRED', readRequested=False, value=None),
            recognition='LINUX_V6_12_RESERVED_INIT_CGROUP_INODE_IMPLEMENTATION_FINGERPRINT_NOT_BINARY_ATTESTATION')
        require(ns_values == [INIT_CGROUP_INODE],
                'SELF_NAMESPACE_VIRTUAL_OR_UNKNOWN_REFUSED_NO_PID1_FALLBACK')
        current = mount / member.relative_to(root)
        headrooms = [row['memAvailableBytes']]
        for depth in range(65):
            require(depth < 64, 'bounded cgroup ancestry exceeded')
            if current == mount:
                controllers = observe(current / 'cgroup.controllers', '$CGROUP_REAL_ROOT/cgroup.controllers', True).split()
                require('memory' in controllers, 'MEMORY_CONTROLLER_UNAVAILABLE_AT_VERIFIED_ROOT')
                procs = observe(current / 'cgroup.procs', '$CGROUP_REAL_ROOT/cgroup.procs', True).split()
                require(all(p.isdigit() for p in procs), 'invalid root cgroup.procs')
                row['rootObservation'] = dict(type=ROOT_NA, path=str(current), logicalPath='$CGROUP_REAL_ROOT',
                    atVerifiedMountRoot=True, mountFSType='cgroup2', mountRoot='/',
                    namespaceObservation=row['namespaceObservation'], coreControllerMemoryObserved=True,
                    coreProcessCount=len(procs), documentation=DOC,
                    memoryInterfaces={name: dict(applicability=ROOT_NA, value=None,
                        readRequested=False, unlimitedObserved=False) for name in MEMORY_FILES})
                break
            logical = '$CGROUP_NONROOT_' + str(depth)
            maximum_raw = observe(current / 'memory.max', logical + '/memory.max', False).strip()
            current_raw = observe(current / 'memory.current', logical + '/memory.current', False).strip()
            require(maximum_raw == 'max' or re.fullmatch('[0-9]+', maximum_raw), 'unknown nonroot memory.max')
            require(re.fullmatch('[0-9]+', current_raw), 'unknown nonroot memory.current')
            maximum = None if maximum_raw == 'max' else int(maximum_raw)
            used = int(current_raw); events = {}
            for line in observe(current / 'memory.events', logical + '/memory.events', False).splitlines():
                p = line.split()
                require(len(p) == 2 and p[0] not in events and re.fullmatch('[0-9]+', p[1]),
                        'malformed/duplicate nonroot events')
                events[p[0]] = int(p[1])
            require('oom' in events and 'oom_kill' in events, 'missing required nonroot OOM counters')
            available = None if maximum is None else max(0, maximum - used)
            if available is not None: headrooms.append(available)
            row['cgroups'].append(dict(path=str(current), logicalPath=logical, memoryMaxRaw=maximum_raw,
                memoryMaxBytes=maximum, memoryCurrentBytes=used, headroomBytes=available,
                limitUnlimited=maximum is None, memoryEvents=events, atVerifiedMountRoot=False))
            require(current.is_relative_to(mount) and current.parent != current, 'ancestor traversal escaped mount')
            current = current.parent
        require(len(row['cgroups']) > 0, 'ROOT_ONLY_PROCESS_SHAPE_UNSUPPORTED_NO_HOST_ONLY_FALLBACK')
        require(row['rootObservation'] is not None, 'missing verified true-root boundary')
        row['effectiveHeadroomBytes'] = min(headrooms)
        row['observationComplete'] = True
        row['gatePassed'] = row['effectiveHeadroomBytes'] >= row['requiredHeadroomBytes']
        if not row['gatePassed']: row['failure'] = 'INSUFFICIENT_MEASURED_EFFECTIVE_HEADROOM'
    except Exception as error:
        row.update(failureType=type(error).__name__, failure=str(error))
    row['finishedUTC'] = utc()
    return row


def validate_snapshot(row, require_pass=True):
    require(set(('schema','startedUTC','finishedUTC','context','budgetMiB','reserveMiB',
        'requiredHeadroomBytes','observationComplete','gatePassed','fileReads','namespaceReads',
        'readAttempts','memAvailableBytes','effectiveHeadroomBytes','cgroupVersion','cgroups',
        'rootObservation','failedReadLogicalPath','failedReadAtVerifiedMountRoot',
        'cgroupMountRoot','cgroupMountPoint','cgroupMembership','namespaceObservation')) <= set(row),
        'missing mandatory resource field')
    require(row.get('schema') == 'C31_CI4_RESOURCE_SELF_NAMESPACE_V1' and row.get('observationComplete') is True,
            'root API observation incomplete')
    context_check(row.get('context', {}))
    require(row.get('budgetMiB') == 5120 and row.get('reserveMiB') == 2048 and
            row.get('requiredHeadroomBytes') == 7168 * MIB, 'memory threshold changed')
    require(row.get('cgroupVersion') == 2 and row.get('cgroupMountRoot') == '/', 'unknown/hidden mount')
    ns = row.get('namespaceObservation', {})
    require(set(ns) == {'selfInode','requiredInitInode','recognition','policy','pid1Observation'}
            and ns.get('selfInode') == INIT_CGROUP_INODE
            and ns.get('policy') == 'SELF_ONLY_RESERVED_INIT_V1'
            and ns.get('pid1Observation') == dict(status='NOT_REQUESTED_NOT_REQUIRED', readRequested=False, value=None)
            and ns.get('requiredInitInode') == INIT_CGROUP_INODE and ns.get('recognition') ==
            'LINUX_V6_12_RESERVED_INIT_CGROUP_INODE_IMPLEMENTATION_FINGERPRINT_NOT_BINARY_ATTESTATION',
            'initial namespace implementation fingerprint unverified')
    root = row.get('rootObservation', {})
    require(root.get('type') == ROOT_NA and root.get('atVerifiedMountRoot') is True
            and root.get('mountFSType') == 'cgroup2' and root.get('mountRoot') == '/'
            and root.get('namespaceObservation') == ns and root.get('coreControllerMemoryObserved') is True
            and root.get('documentation') == DOC and type(root.get('coreProcessCount')) is int
            and root['coreProcessCount'] >= 0,
            'missing typed documented true-root observation')
    require(root.get('memoryInterfaces') == {name: dict(applicability=ROOT_NA, value=None,
            readRequested=False, unlimitedObserved=False) for name in MEMORY_FILES},
            'root NA was confused with measured unlimited or fabricated values')
    groups = row.get('cgroups'); require(isinstance(groups, list) and len(groups) > 0, 'root-only/empty accounting')
    mount = absolute_posix(row.get('cgroupMountPoint', ''))
    member = absolute_posix(row.get('cgroupMembership', ''))
    chain = [absolute_posix(g['path']) for g in groups]
    require(chain[0] == mount / member.relative_to(PurePosixPath('/')) and chain[-1].parent == mount
            and all(a.parent == b for a,b in zip(chain, chain[1:])) and len(chain) <= 63
            and root.get('path') == str(mount) and root.get('logicalPath') == '$CGROUP_REAL_ROOT',
            'missing/noncontiguous nonroot ancestor coverage')
    available = row.get('memAvailableBytes'); require(type(available) is int and available >= 0, 'missing MemAvailable')
    headrooms = [available]
    for i,g in enumerate(groups):
        require(g.get('logicalPath') == '$CGROUP_NONROOT_' + str(i) and g.get('atVerifiedMountRoot') is False,
                'nonroot coordinate or applicability drift')
        require(set(('memoryMaxBytes','memoryCurrentBytes','memoryMaxRaw','headroomBytes','limitUnlimited','memoryEvents')) <= set(g),
                'missing mandatory nonroot field')
        maximum, used = g['memoryMaxBytes'], g['memoryCurrentBytes']
        require(type(used) is int and used >= 0, 'invalid nonroot current')
        if maximum is None:
            require(g['memoryMaxRaw'] == 'max' and g['limitUnlimited'] is True and g['headroomBytes'] is None,
                    'unknown nonroot limit is not unlimited')
        else:
            require(type(maximum) is int and maximum >= 0 and g['memoryMaxRaw'] == str(maximum)
                    and g['limitUnlimited'] is False, 'invalid nonroot limit')
            remaining = max(0, maximum-used); headrooms.append(remaining)
            require(g['headroomBytes'] == remaining, 'nonroot subtraction changed')
        require(isinstance(g['memoryEvents'], dict) and {'oom','oom_kill'} <= set(g['memoryEvents'])
                and all(type(v) is int and v >= 0 for v in g['memoryEvents'].values()), 'missing actual nonroot counters')
    require(row.get('effectiveHeadroomBytes') == min(headrooms) and type(row.get('gatePassed')) is bool
            and row['gatePassed'] == (min(headrooms) >= 7168 * MIB), 'forged/changed effective gate')
    expected = {'$PROC/meminfo','$PROC/self/cgroup','$PROC/self/mountinfo',
                '$CGROUP_REAL_ROOT/cgroup.controllers','$CGROUP_REAL_ROOT/cgroup.procs'} | \
               {g['logicalPath']+'/'+name for g in groups for name in MEMORY_FILES}
    reads = row.get('fileReads'); links = row.get('namespaceReads'); attempts = row.get('readAttempts')
    require(isinstance(reads,list) and len(reads) == len(expected) and {r['logicalPath'] for r in reads} == expected,
            'missing/duplicate real resource-file observations')
    require(isinstance(links,list) and len(links) == 1 and {r['logicalPath'] for r in links} ==
            {'$PROC/self/ns/cgroup'}, 'namespace link reads missing')
    require(isinstance(attempts,list) and len(attempts) == len(reads)+len(links)
            and all(a.get('status') == 'READ_OK' for a in attempts), 'incomplete/failed read attempt cannot be green')
    for receipt in reads+links:
        logical = receipt['logicalPath']
        expected_root = True if logical.startswith('$CGROUP_REAL_ROOT/') else (
            False if logical.startswith('$CGROUP_NONROOT_') else None)
        link = receipt in links
        expected_path = ({'$PROC/meminfo':'/proc/meminfo', '$PROC/self/cgroup':'/proc/self/cgroup',
            '$PROC/self/mountinfo':'/proc/self/mountinfo', '$PROC/self/ns/cgroup':'/proc/self/ns/cgroup'}.get(logical))
        if expected_path is None:
            coordinates = [(g['logicalPath'], g['path']) for g in groups] + [('$CGROUP_REAL_ROOT',str(mount))]
            matches = [str(PurePosixPath(path) / logical[len(prefix)+1:]) for prefix,path in coordinates
                       if logical.startswith(prefix+'/')]
            require(len(matches) == 1, 'ambiguous receipt coordinate')
            expected_path = matches[0]
        require(receipt.get('path') == expected_path and receipt.get('atVerifiedMountRoot') is expected_root
                and 'atVerifiedMountRoot' in receipt and receipt.get('hashScope') ==
                ('READLINK_TARGET_UTF8' if link else 'ORIGINAL_FILE_BYTES'), 'resource binding/path/hash scope changed')
        if link:
            raw = ('cgroup:[' + str(INIT_CGROUP_INODE) + ']').encode('utf-8')
            require(receipt['sha256'] == hashlib.sha256(raw).hexdigest() and receipt['bytes'] == len(raw),
                    'namespace observation/target hash mismatch')
        require(type(receipt.get('bytes')) is int and receipt['bytes'] >= 0 and
                re.fullmatch('[0-9a-f]{64}',receipt.get('sha256','')), 'missing original observation hash')
        matching = [a for a in attempts if a.get('logicalPath') == receipt['logicalPath']]
        require(len(matching) == 1 and matching[0].get('sha256') == receipt['sha256']
                and matching[0].get('bytes') == receipt['bytes']
                and matching[0].get('atVerifiedMountRoot') is receipt['atVerifiedMountRoot']
                and 'atVerifiedMountRoot' in matching[0] and matching[0].get('path') == expected_path
                and matching[0].get('operation') == ('READLINK_UTF8' if link else 'READ_FILE_BYTES')
                and all(type(matching[0].get(k)) is str and
                    datetime.fromisoformat(matching[0][k]).utcoffset() is not None
                    for k in ('attemptedUTC','finishedUTC')), 'attempt/receipt disagreement')
    require(row.get('failedReadLogicalPath') is None and row.get('failedReadAtVerifiedMountRoot') is None,
            'failed read was silently ignored')
    for key in ('startedUTC','finishedUTC'):
        require(type(row.get(key)) is str and datetime.fromisoformat(row[key]).utcoffset() is not None,
                'resource UTC absent')
    if require_pass: require(row['gatePassed'], 'insufficient effective headroom')
    return True
