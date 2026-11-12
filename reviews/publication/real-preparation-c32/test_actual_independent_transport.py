"""Read-only archive replay of real independent data, not source/Lean acceptance."""
import argparse,contextlib,hashlib,io,json,pathlib,types,unittest,zipfile
ROOT=pathlib.Path(__file__).resolve().parents[3];HERE=pathlib.Path(__file__).resolve().parent
def sha(raw):return hashlib.sha256(raw).hexdigest()
def load_archive(path):
    with zipfile.ZipFile(path) as z:
        names=z.namelist();assert len(names)==len(set(names))
        return {n:z.read(n) for n in names}
def read_only_decoder_replay():
    files=load_archive(HERE/'decoder-actual-c39-public.zip')
    m=types.ModuleType('c40_actual_decoder_read_only');exec(compile(files['replay.py'],'$SEALED_DECODER/replay.py','exec'),m.__dict__)
    captured={};sentinel=ROOT/'_out/virtual-only-c40-decoder-output'
    Base=type(pathlib.Path())
    class MemoryPath(Base):
        def exists(self):
            if self==sentinel or self.parent==sentinel:return False
            return super().exists()
        def mkdir(self,*a,**k):
            if self!=sentinel:raise AssertionError('forbidden mkdir')
        def write_text(self,text,encoding=None,errors=None,newline=None):
            if self.parent!=sentinel:raise AssertionError('forbidden file write')
            captured[self.name]=text;return len(text)
    # Replace this replay module's Path constructor only, never global pathlib.
    m.pathlib=types.SimpleNamespace(Path=MemoryPath)
    args=argparse.Namespace(actual=str(HERE/'c34-ci5-actual-success-public.zip'),runtime=str(ROOT/'tools/real_preparation_native_c34_ci5/public-runtime-package.zip'),
        static=str(HERE/'decoder-static-public-bundle.zip'),repo=str(ROOT),out=str(sentinel),parent_context=str(ROOT/'reports/lean-433-migration/c39-ci5-context-api.json'))
    output=io.StringIO()
    with contextlib.redirect_stdout(output):m.main(args)
    return files,captured,json.loads(output.getvalue())
class RealIndependentTransportTests(unittest.TestCase):
    def test_exact_allowlists_seals_and_original_manifest(self):
        r=json.loads((ROOT/'reports/lean-433-migration/c40-real-independent-transport.json').read_bytes())
        self.assertEqual([a['members'] for a in r['archives']],[19,5,3])
        for a in r['archives']:
            raw=(ROOT/a['path']).read_bytes();self.assertEqual(sha(raw),a['sha256']);f=load_archive(ROOT/a['path'])
            self.assertEqual(len(f),a['members']);self.assertEqual(sha(f[a['seal']]),a['seal_sha256'])
            allow=json.loads(f[a['allowlist']])
            if 'allowed' in allow:
                self.assertEqual(set(f),set(allow['allowed']));s=json.loads(f['seal.json']);self.assertEqual(sha(f['hashmanifest.json']),s['manifest_sha256'])
                for p in json.loads(f['hashmanifest.json'])['files']:self.assertEqual(sha(f[p['path']]),p['sha256'])
            elif 'dataFiles' in allow:
                self.assertEqual(set(f),set(allow['dataFiles'])|set(allow['controlFiles']))
                for n,d in allow['dataFiles'].items():self.assertEqual(sha(f[n]),d)
            else:
                self.assertEqual(set(f),set(allow['files'])|{a['allowlist']})
                for n,d in allow['files'].items():self.assertEqual(sha(f[n]),d)
    def test_same_decoder_recalculation_matches_all_derived_objects_without_writes(self):
        f,new,summary=read_only_decoder_replay()
        self.assertGreaterEqual(len(new),10)
        for n,text in new.items():
            if n.endswith('.json'):self.assertEqual(json.loads(text),json.loads(f[n]),n)
            else:self.assertEqual(text.replace('\r\n','\n'),f[n].decode().replace('\r\n','\n'),n)
        self.assertEqual((summary['roots'],summary['generated'],summary['owned'],summary['providers']),(57,47,104,34))
        self.assertEqual(summary['source_mismatches'],[]);self.assertEqual(len(set(summary['process_pids'])),10)
        self.assertEqual(summary['runtime_context_shas'],['a12a5eb7fe33514a63f04ed3372ee03f0ee9e145'])
    def test_actual_owned_not_namespace_and_pre_post_headroom_distinction(self):
        f=load_archive(HERE/'decoder-actual-c39-public.zip');generated=json.loads(f['actual-generated.json'])
        row=next(x for x in generated if x['actualName']=='QuantumBlockEncoding.zeroBasisIndex.eq_1')
        self.assertEqual(row['module'],'QuantumBlockEncoding.RealAmplitudePreparation')
        stages=json.loads(f['independent-resource-processes.json'])['stages']
        self.assertEqual(min(s['pre']['effective_headroom'] for s in stages),15280009216)
        self.assertEqual(min(s[p]['effective_headroom'] for s in stages for p in ('pre','post')),15279939584)
    def test_source_v3_is_exact_declared_literal_change_not_old_source_rewrite(self):
        f=load_archive(HERE/'source-v3-author-proposal-public.zip');p=json.loads(f['source-change-record-v3.json']);new=f['source-effective-v3.md']
        self.assertEqual(sha(new),p['source_sha256']);text=new.decode();self.assertEqual(text.count(p['after']),1)
        previous=text.replace(p['after'],p['before'],1).encode();self.assertEqual(sha(previous),p['previous_source_sha256'])
        self.assertFalse(p['production_changed']);self.assertFalse(p['preproof_claim']);self.assertEqual(p['independent_review'],'PENDING')
        for k in ('B','C','D','E','F','G','H','I'):
            marker='## '+k+'.';self.assertEqual(previous.decode().split(marker,1)[1],text.split(marker,1)[1])
if __name__=='__main__':unittest.main()
