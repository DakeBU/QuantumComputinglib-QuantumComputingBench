"""Recheck this fixed preparatory library fragment; never accepts model output."""
from __future__ import annotations
import argparse,ctypes,hashlib,json,os,re,shutil,subprocess,sys,time
from pathlib import Path

PACKAGE=Path(__file__).resolve().parent
ROOT=PACKAGE.parents[2]
ROOTS=['QuantumBlockEncoding.MeasurementProbability.sum_norm_sq_eq',
       'QuantumBlockEncoding.MeasurementProbability.outcome_probability_mem_Icc',
       'MeasurementIntakeCanary.qa_consumer']
ORDINARY={'propext','Classical.choice','Quot.sound'}
FILES=['QuantumBlockEncoding/MeasurementProbability.lean','Canary.lean','ExportGraph.lean',
       'controls/WrongTarget.lean','controls/SorryControl.lean']
sha=lambda b:hashlib.sha256(b).hexdigest()

def observations(text,expected):
    rows=[];cursor=0
    for m in re.finditer(r"'([^']+)' depends on axioms: \[([^\]]+)\]",text,re.DOTALL):
        if text[cursor:m.start()].strip():raise ValueError('unexpected observation prelude')
        names=[x.strip() for x in m[2].split(',')]
        if len(names)!=len(set(names)):raise ValueError('duplicate axiom')
        rows.append({'name':m[1],'axioms':names});cursor=m.end()
    if text[cursor:].strip() or [r['name'] for r in rows]!=expected:
        raise ValueError('missing, reordered or unparsed observation')
    return rows

def check_positive(text):
    rows=observations(text,ROOTS)
    if any(set(r['axioms'])-ORDINARY for r in rows):raise ValueError('extra axiom')
    return rows

def windows_memory_preflight(required=5120):
    if os.name!='nt':return None
    class Memory(ctypes.Structure):
        _fields_=[('length',ctypes.c_ulong),('load',ctypes.c_ulong),*[(n,ctypes.c_ulonglong) for n in
            ('total','available','page','apage','virtual','avirtual','extended')]]
    m=Memory();m.length=ctypes.sizeof(m)
    if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m)):raise RuntimeError('memory unavailable')
    available=m.available//1048576
    if available<required:raise RuntimeError('free memory below reserve; no compiler launched')
    return available

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',required=True);a=p.parse_args()
    if Path(a.output).is_absolute() or '..' in Path(a.output).parts or not a.output.replace('\\','/').startswith('_out/'):
        p.error('output must be a new repository-relative _out/ directory')
    out=(ROOT/a.output).resolve()
    if not out.is_relative_to(ROOT.resolve()):p.error('output escapes checkout')
    pins={n:sha((PACKAGE/n).read_bytes()) for n in FILES}
    if (ROOT/'lean-toolchain').read_text().strip()!='leanprover/lean4:v4.33.0':
        raise RuntimeError('requires the separately provisioned Lean4.33 context')
    free=windows_memory_preflight();out.mkdir(parents=True,exist_ok=False)
    record={'success':False,'status':'started','input_pins':pins,'free_MiB':free,'commands':[],
            'full_repository_gate':False,'main_admitted':False,'stable_QA_gold':False}
    def save():
        (out/'result.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    save()
    try:
        for n in FILES:
            target=out/n;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(PACKAGE/n,target)
        prefix=subprocess.check_output(['lake','env','lean','--print-prefix'],cwd=ROOT).decode().strip()
        binary=Path(prefix)/('bin/lean.exe' if os.name=='nt' else 'bin/lean')
        binary_hash=sha(binary.read_bytes())
        base=subprocess.check_output(['lake','env',sys.executable,'-B','-c',
            'import os; print(os.environ.get("LEAN_PATH", ""))'],cwd=ROOT).decode().strip()
        env=dict(os.environ,LEAN_PATH=str(out)+os.pathsep+base)
        def run(label,args):
            windows_memory_preflight();start=time.monotonic()
            r=subprocess.run([str(binary),*args],cwd=ROOT,env=env,capture_output=True,timeout=120)
            for key,data in [('stdout',r.stdout),('stderr',r.stderr)]:(out/(label+'.'+key)).write_bytes(data)
            record['commands'].append({'label':label,'exit_code':r.returncode,'seconds':round(time.monotonic()-start,3),
                'stdout_sha256':sha(r.stdout),'stderr_sha256':sha(r.stderr)})
            save();return r
        version=run('version',['--version'])
        if version.returncode or b'version 4.33.0' not in version.stdout:raise RuntimeError('wrong binary')
        source=out/FILES[0];own=source.with_suffix('.olean')
        compiled=run('source',['-M1536','-j1','--root='+str(out),'-o',str(own),str(source)])
        if compiled.returncode or not own.is_file():raise RuntimeError('source failed')
        own_hash=sha(own.read_bytes())
        deps=run('consumer-deps',['--deps',str(out/'Canary.lean')])
        selected=[Path(s.strip()).resolve() for s in deps.stdout.decode().splitlines() if s.strip()]
        if deps.returncode or [x for x in selected if x.name==own.name]!=[own.resolve()]:raise RuntimeError('wrong own dependency')
        positive=run('consumer',['-M1536','-j1',str(out/'Canary.lean')])
        if positive.returncode:raise RuntimeError('consumer failed')
        record['axioms']=check_positive(positive.stdout.decode())
        wrong=run('wrong-target',['-M1536','-j1',str(out/'controls/WrongTarget.lean')])
        if wrong.returncode==0 or b'error:' not in wrong.stdout:raise RuntimeError('wrong target not rejected')
        negative=run('sorry-control',['-M1536','-j1',str(out/'controls/SorryControl.lean')])
        # Ignore only the explicit Lean warning prefix; exact theorem observation is still required.
        text=negative.stdout.decode();start=text.find("'measurementIntakeSorryControl'")
        if negative.returncode or start<0:raise RuntimeError('negative fixture failed to run')
        rows=observations(text[start:],['measurementIntakeSorryControl'])
        if 'sorryAx' not in rows[0]['axioms']:raise RuntimeError('sorryAx not rejected')
        windows_memory_preflight(6144)
        graph=run('graph',['-M2048','-j1',str(out/'ExportGraph.lean')])
        text=graph.stdout.decode().strip()
        if graph.returncode or not text.startswith('MEASUREMENT_GRAPH|'):raise RuntimeError('graph failed')
        data=json.loads(text.removeprefix('MEASUREMENT_GRAPH|'))
        if [r['name'] for r in data['rows']]!=ROOTS[:2] or ROOTS[0] not in data['rows'][1]['proof_references']:
            raise RuntimeError('wrong graph roots or missing direct reuse')
        (out/'proof-term-graph.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
        if any(sha((PACKAGE/n).read_bytes())!=h or sha((out/n).read_bytes())!=h for n,h in pins.items()):raise RuntimeError('source changed')
        if sha(own.read_bytes())!=own_hash or sha(binary.read_bytes())!=binary_hash:raise RuntimeError('binary changed')
        record.update(success=True,status='focused_preparatory_fragment_only',own_olean_sha256=own_hash,
            binary_sha256=binary_hash,wrong_target_rejected=True,sorryAx_rejected=True,
            graph_sha256=sha((out/'proof-term-graph.json').read_bytes()))
    except Exception as error:
        record.update(success=False,status='failed',failure_class=type(error).__name__)
        raise
    finally:save()
    print(json.dumps({'success':True,'scope':record['status']}))

if __name__=='__main__':main()
