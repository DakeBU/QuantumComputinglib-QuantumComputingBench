"""Exact portable transport and optional future-CI invocation, never admission."""
import argparse,hashlib,importlib.util,json,os,subprocess,sys,zipfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
ARCHIVE_SHA256='97bfea091bf49cc17790aa52a3dab0f5e1d8316f2cef129e1989e5159ec35578'
APPROVED_SEAL_SHA256='27e4809bb7ec98fe0d3872ae314353f11e6dc1f75dda4f6a4d9d4b460edc8e24'
def digest(raw):return hashlib.sha256(raw).hexdigest()
def prepare(project):
    project=project.resolve();archive=HERE/'public-runtime-package.zip'
    if digest(archive.read_bytes())!=ARCHIVE_SHA256:raise ValueError('portable ZIP changed')
    with zipfile.ZipFile(archive) as z:
        names=z.namelist()
        if len(names)!=31 or len(names)!=len(set(names)):raise ValueError('portable member partition changed')
        data={n:z.read(n) for n in names}
    if digest(data['packet-seal.json'])!=APPROVED_SEAL_SHA256:raise ValueError('approved seal changed')
    seal=json.loads(data['packet-seal.json'])
    for row in seal['files']:
        raw=data[row['path']]
        if len(raw)!=row['bytes'] or digest(raw)!=row['sha256']:raise ValueError('payload changed')
    out=project/'_out/c34-native-ci5';out.mkdir(parents=True,exist_ok=True)
    if not out.resolve().is_relative_to(project):raise ValueError('transport output escapes project')
    package=out/'runtime'
    if not package.exists():
        package.mkdir()
        for name,raw in data.items():
            path=Path(name)
            if path.is_absolute() or '..' in path.parts or ':' in name or '\\' in name:raise ValueError('unsafe ZIP path')
            target=package/path;target.parent.mkdir(parents=True,exist_ok=True)
            with target.open('xb') as stream:stream.write(raw)
    for name,raw in data.items():
        target=package/name
        if not target.resolve().is_relative_to(package.resolve()) or target.read_bytes()!=raw:raise ValueError('transported runtime drift')
    return package,out
def diagnostics():
    path=HERE.parent/'real_preparation_native_c34_ci1/launch_ci2.py'
    expected='3d3a7c4d3d31a1eae397787951e7e43bd0adf23c24599c9ece45bcbd2ed72544'
    if digest(path.read_bytes())!=expected:raise ValueError('diagnostic source drift')
    spec=importlib.util.spec_from_file_location('c34_exact_failed_python_logging',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    if Path(module.__file__).resolve()!=path.resolve() or digest(path.read_bytes())!=expected:raise ValueError('diagnostic imported file drift')
    return module

def main():
    parser=argparse.ArgumentParser(description=__doc__);group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--python-tests',action='store_true');group.add_argument('--ci',action='store_true')
    args=parser.parse_args();project=HERE.parents[1];package,out=prepare(project)
    if args.python_tests:
        command=[sys.executable,'-B','-m','unittest','discover','-s',str(package),'-p','test*.py','-v']
    else:
        command=[sys.executable,'-B',str(package/'runner.py'),'--project',str(project),
                 '--ci','--approved-seal-sha256',APPROVED_SEAL_SHA256]
    child=subprocess.run(command,cwd=project,env=dict(os.environ,C34_TEST_PROJECT=str(project)),capture_output=True)
    public=out/'public';public.mkdir(exist_ok=True)
    logging=diagnostics();derivatives=logging.preserve_failed_python(public,child,project,package) if args.python_tests else []
    result=dict(schema='C34_PARENT_GATED_5120_CI5_LAUNCH_RECEIPT',exitCode=child.returncode,failedPythonDerivatives=derivatives,
        mode='PYTHON_ONLY_NO_LEAN' if args.python_tests else 'FINITE_CI_NATIVE_DIAGNOSTIC',
        actualArchiveSHA256=ARCHIVE_SHA256,approvedSealSHA256=APPROVED_SEAL_SHA256,
        stdoutSHA256=digest(child.stdout),stderrSHA256=digest(child.stderr),
        sourceAgreement=None,publicationBinding=None,nativeAccepted=False,scientific_ROOT=False)
    receipt=public/('python-result.json' if args.python_tests else 'launcher-result.json')
    with receipt.open('x',encoding='utf-8') as stream:json.dump(result,stream,indent=2);stream.write('\n')
    print(json.dumps(result));return child.returncode
if __name__=='__main__':sys.exit(main())
