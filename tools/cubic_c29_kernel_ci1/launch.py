"""Run an exact sealed candidate outside production sources; never grant admission."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
import zipfile

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
PROJECT=Path.cwd().resolve()
OUT=PROJECT/'_out/cubic-c29-kernel-ci1'
FLAGS=dict(sourceAgreement=None,publicationBinding=None,axiomPolicyPass=None,
           nativeAccepted=False,scientific_ROOT=False)
sha=lambda raw:hashlib.sha256(raw).hexdigest()
read=lambda p:json.loads(p.read_bytes())

def write_new(path,raw):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('xb') as f:f.write(raw)

def json_new(path,value):
    write_new(path,(json.dumps(value,indent=2)+'\n').encode())

def safe_output():
    if not OUT.resolve().is_relative_to(PROJECT):raise ValueError('output escaped project')
    if any(p.is_symlink() for p in (PROJECT/'_out',OUT)):
        raise ValueError('output symlink refused')

def archive_bytes(path,expected_sha,expected_members):
    if sha(path.read_bytes())!=expected_sha:raise ValueError('sealed archive changed')
    with zipfile.ZipFile(path) as z:
        names=z.namelist()
        if len(names)!=len(set(names)) or set(names)!=set(expected_members):
            raise ValueError('exact archive member partition changed')
        data={}
        for name in names:
            p=PurePosixPath(name)
            if p.is_absolute() or '..' in p.parts or '\\' in name or ':' in name:
                raise ValueError('unsafe archive path')
            raw=z.read(name)
            if sha(raw)!=expected_members[name]:raise ValueError('sealed member changed: '+name)
            data[name]=raw
        return data

def inputs():
    manifest=read(HERE/'integration-pins.json')
    if manifest.get('schema')!='C29_OPTIONAL_KERNEL_CI1_TRANSPORT_V1':raise ValueError('unknown transport')
    if sha((HERE/'launch.py').read_bytes())!=manifest['launcher_sha256']:
        raise ValueError('launcher bytes changed')
    runtime=archive_bytes(HERE/'public-runtime-package.zip',manifest['runtime_archive_sha256'],manifest['runtime_files'])
    tests=archive_bytes(HERE/'sealed-v2-python-suite.zip',manifest['tests_archive_sha256'],manifest['tests_files'])
    if set(runtime)!=set(read(HERE/'runtime-public-allowlist.json')['files'][i]['relativePath']
                         for i in range(10)):
        raise ValueError('runtime allowlist partition changed')
    if sha((HERE/'runtime-public-allowlist.json').read_bytes())!=manifest['allowlist_sha256']:
        raise ValueError('public transport allowlist changed')
    return manifest,runtime,tests

def prepare_runtime(runtime):
    safe_output();target=OUT/'runtime'
    if target.is_symlink():raise ValueError('runtime symlink refused')
    if target.exists():
        present={p.relative_to(target).as_posix():p.read_bytes() for p in target.rglob('*') if p.is_file()}
        if present!=runtime:raise ValueError('existing prepared runtime differs')
    else:
        target.mkdir(parents=True,exist_ok=False)
        for name,raw in runtime.items():write_new(target/name,raw)
    return target

def python_tests():
    manifest,runtime,tests=inputs()
    prepare_runtime(runtime)
    suite=OUT/'python-suite';suite.mkdir(exist_ok=False)
    for name,raw in {**runtime,**tests}.items():write_new(suite/name,raw)
    (suite/'tests-private').mkdir()
    private=OUT/'private';private.mkdir(exist_ok=False)
    public=OUT/'public';public.mkdir(exist_ok=False)
    started=datetime.now(timezone.utc).isoformat()
    proc=subprocess.Popen([sys.executable,'-B',str(suite/'test_kernel_only.py')],
        cwd=PROJECT,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    timed_out=False
    try:out,err=proc.communicate(timeout=60)
    except subprocess.TimeoutExpired:
        timed_out=True;proc.kill();out,err=proc.communicate()
    write_new(private/'python.stdout.raw',out);write_new(private/'python.stderr.raw',err)
    text=(out+err).decode(errors='replace')
    passed=not timed_out and proc.returncode==0 and 'Ran 31 tests' in text and text.rstrip().endswith('OK')
    result=dict(schema='C29_ACTUAL_OPTIONAL_CI_PYTHON_TESTS_V1',PID=proc.pid,startedUTC=started,
        finishedUTC=datetime.now(timezone.utc).isoformat(),exitCode=proc.returncode,timedOut=timed_out,
        tests=31 if passed else None,passed=passed,stdoutSHA256=sha(out),stderrSHA256=sha(err),
        runtimeArchiveSHA256=manifest['runtime_archive_sha256'],LeanCalls=0,
        scope='Synthetic validator/fixture tests; not a candidate Lean certificate',**FLAGS)
    json_new(public/'python-result.json',result)
    print(json.dumps(result),flush=True)
    return 0 if passed else 1

def execute():
    manifest,runtime,_=inputs()
    if not sys.platform.startswith('linux') or os.environ.get('GITHUB_ACTIONS')!='true' \
            or os.environ.get('RUNNER_OS')!='Linux':
        raise ValueError('reviewed candidate execution is GitHub Linux CI only')
    target=prepare_runtime(runtime)
    receipt=read(OUT/'public/python-result.json')
    if not (receipt.get('passed') is True and receipt.get('exitCode')==0 and receipt.get('tests')==31
            and receipt.get('runtimeArchiveSHA256')==manifest['runtime_archive_sha256']):
        raise ValueError('actual preceding Python gate missing or failed')
    # Original adapter owns finite 600s target / 300s probe / 3072-MiB / one-thread gates.
    # No production Lean, original binding, verifier or scoring bytes are changed.
    return subprocess.call([sys.executable,'-B',str(target/'kernel_only.py'),
        '--project',str(PROJECT),'--execute-after-parent-review'],cwd=PROJECT)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--python-tests',action='store_true')
    group.add_argument('--execute-reviewed-candidate',action='store_true')
    args=parser.parse_args()
    try:code=python_tests() if args.python_tests else execute()
    except Exception as error:
        print(json.dumps(dict(status='LAUNCH_FAILED_CLOSED',failureType=type(error).__name__,**FLAGS)))
        code=1
    sys.exit(code)
