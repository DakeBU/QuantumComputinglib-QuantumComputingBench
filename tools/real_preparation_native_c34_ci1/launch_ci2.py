"""Versioned launcher: preserve immutable runtime and expose sanitized Python failures."""
import argparse,hashlib,importlib.util,json,os,re,subprocess,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
BASE_SHA='a5f96cf4c6fb64ab553b563425b32d6e381c5de5e1da272c628bb95c98dbc414'
def digest(raw):return hashlib.sha256(raw).hexdigest()
def load_base():
    p=HERE/'launch.py'
    if digest(p.read_bytes())!=BASE_SHA:raise ValueError('immutable CI1 launcher drift')
    spec=importlib.util.spec_from_file_location('c34_parent_ci1_exact',p);base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
    if Path(base.__file__).resolve()!=p:raise ValueError('CI1 executed path drift')
    return base
def sanitized(raw,project,package):
    text=raw.decode('utf-8',errors='replace')
    roots=[(package,'$PACKAGE'),(project,'$PROJECT'),(Path(sys.prefix),'$PYTHON'),(Path.home(),'$USER_HOME'),(Path(tempfile.gettempdir()),'$TEMP')]
    for path,label in sorted(roots,key=lambda r:len(str(r[0])),reverse=True):
        for spelling in {str(path),str(path).replace('\\','/'),str(path).replace('/','\\')}:
            text=text.replace(spelling,label)
    text=re.sub(r'(?:github_pat_|gh[pousr]_)[A-Za-z0-9_]+','<credential-redacted>',text)
    text=re.sub(r'(?<![A-Za-z0-9_$])[A-Za-z]:[\\/][^\r\n"<>]*','<absolute-path-redacted>',text)
    text=re.sub(r'(?<![A-Za-z0-9_$])/(?:home|Users|tmp|opt|usr|mnt|root)/[^\s"\')>,;]*','<absolute-path-redacted>',text)
    return text.encode('utf-8')
def preserve_failed_python(public,child,project,package):
    rows=[]
    if child.returncode==0:return rows
    for label,raw in [('stdout',child.stdout),('stderr',child.stderr)]:
        safe=sanitized(raw,project,package);path=public/('ci2-python-failure.'+label+'.sanitized.txt')
        with path.open('xb') as stream:stream.write(safe)
        rows.append(dict(path=path.name,rawSHA256=digest(raw),rawBytes=len(raw),publicSHA256=digest(safe),publicBytes=len(safe),redacted=True))
    return rows
def main():
    parser=argparse.ArgumentParser(description=__doc__);g=parser.add_mutually_exclusive_group(required=True)
    g.add_argument('--python-tests',action='store_true');g.add_argument('--ci',action='store_true');args=parser.parse_args()
    base=load_base();project=HERE.parents[1];package,out=base.prepare(project)
    if args.python_tests:command=[sys.executable,'-B','-m','unittest','discover','-s',str(package),'-p','test*.py','-v']
    else:command=[sys.executable,'-B',str(package/'runner.py'),'--project',str(project),'--ci','--approved-seal-sha256',base.APPROVED_SEAL_SHA256]
    child=subprocess.run(command,cwd=project,env=dict(os.environ,C34_TEST_PROJECT=str(project)),capture_output=True)
    public=out/'public';public.mkdir(exist_ok=True)
    diagnostics=preserve_failed_python(public,child,project,package) if args.python_tests else []
    result=dict(schema='C34_PARENT_CI2_VERSIONED_LAUNCH_RECEIPT',exitCode=child.returncode,mode='PYTHON_ONLY_NO_LEAN' if args.python_tests else 'FINITE_CI_NATIVE_DIAGNOSTIC',
        immutableCI1LauncherSHA256=BASE_SHA,actualArchiveSHA256=base.ARCHIVE_SHA256,approvedSealSHA256=base.APPROVED_SEAL_SHA256,
        stdoutSHA256=digest(child.stdout),stderrSHA256=digest(child.stderr),failedPythonDerivatives=diagnostics,
        sourceAgreement=None,publicationBinding=None,nativeAccepted=False,scientific_ROOT=False)
    path=public/('ci2-python-result.json' if args.python_tests else 'ci2-launcher-result.json')
    with path.open('x',encoding='utf-8') as stream:json.dump(result,stream,indent=2);stream.write('\n')
    print(json.dumps(result));return child.returncode
if __name__=='__main__':sys.exit(main())
