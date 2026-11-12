"""Sealed partial evidence and negative preservation, not theorem-source equivalence."""
import ast,hashlib,json,re,unittest,zipfile
from pathlib import Path
BASE=Path(__file__).resolve().parent
SHA=lambda b:hashlib.sha256(b).hexdigest()
class SequentialEvidenceTests(unittest.TestCase):
    def check_manifest(self,z,seal_name,seal_sha,manifest_name,manifest_sha,key,path_key):
        self.assertEqual(SHA(z.read(seal_name)),seal_sha)
        self.assertEqual(SHA(z.read(manifest_name)),manifest_sha)
        for row in json.loads(z.read(manifest_name))[key]:self.assertEqual(SHA(z.read(row[path_key])),row['sha256'])
    def test_exact_source_and_original_negative_graph_are_not_rewritten(self):
        self.assertEqual(SHA((BASE/'natural-source-v1.md').read_bytes()),'583cc9333ea977ec6684313749b6f52b49aded53e50456913f065487cada426a')
        self.assertEqual(SHA((BASE/'source-graph-v1.json').read_bytes()),'ffb1b18419c2f340baa76b0ded4ceb5f0fcc3c25a18da03b1d87d8d7c2eff805')
        self.assertEqual(json.loads((BASE/'source-graph-v1.json').read_bytes())['or_alternatives'],[])
    def test_actual_stage1_exact_nine_allowlist_and_mathematical_scope(self):
        with zipfile.ZipFile(BASE/'raw-source-stage1-public9.zip') as z:
            self.assertEqual(len(z.namelist()),9)
            self.assertEqual(set(z.namelist()),set(json.loads(z.read('publicsafe-allowlist.json'))['files']))
            self.check_manifest(z,'stage1-seal.json','8bec8f6db81825bde182d33a0c82e29931f83f51662a9123c50d87e3f5066045','manifest.json','4789395f2eed72ecda52b3d8d17e0a163dc366946f35bbb9074e0d8be176a6e2','payloads','file')
            self.assertIn('no formal/Lean acceptance',json.loads(z.read('manifest.json'))['verdict'])
    def test_actual_stage2_negative_two_blocking_findings_and_no_formal_read(self):
        with zipfile.ZipFile(BASE/'source-topology-stage2-negative-public7.zip') as z:
            self.assertEqual(len(z.namelist()),7)
            self.check_manifest(z,'stage2-seal.json','2e7aba785700c885e8cf813ebe4fbe48e97ad913e61d8a12722f090dcf89fc80','manifest.json','463acb07fa0684921eaa41fd5f0af98f9ff25377fb994d0bc66be785379d4bee','payloads','file')
            finding=json.loads(z.read('findings.json'))
            self.assertEqual(finding['verdict'],'NEEDS_TOPOLOGY_REVISION_STOP_BEFORE_FORMAL')
            self.assertEqual([f['id'] for f in finding['findings'] if f['severity']=='blocking topology'],['T2-01','T2-02'])
            self.assertEqual(json.loads(z.read('manifest.json'))['stage3'],'NOT_ENTERED')
    def test_author_successor_retains_established_route_and_lossless_coverage(self):
        old=json.loads((BASE/'source-graph-v1.json').read_bytes())
        with zipfile.ZipFile(BASE/'topology-c55-author-proposal5.zip') as z:
            raw=z.read('source-graph.successor.json');new=json.loads(raw)
            self.assertEqual(SHA(raw),'21e9cadc1325b35382dea47c46e2fdad4a99e8f34fdbe90a4347567d5b67323d')
            self.assertEqual(len(z.namelist()),5)
            for key in ('nodes','coverage','excluded','no_Lean_import_graph_substitution'):self.assertEqual(new[key],old[key])
            self.assertEqual(len(new['coverage']),71)
    def test_two_OR_groups_are_unresolved_and_support_only_restricted_route(self):
        with zipfile.ZipFile(BASE/'topology-c55-author-proposal5.zip') as z:
            graph=json.loads(z.read('source-graph.successor.json'))
            self.assertEqual(len(graph['or_alternatives']),2)
            for group in graph['or_alternatives']:
                self.assertEqual(group['connective'],'OR');self.assertEqual(group['status'],'ALL_ROUTES_UNRESOLVED')
                self.assertTrue(all(r['supplier_status']=='NONE_DELIVERED_BY_THIS_REPAIR' for r in group['routes']))
            group=next(g for g in graph['or_alternatives'] if g['id']=='or:target-contraction')
            routes={r['id']:r for r in group['routes']}
            self.assertEqual(routes['route:contraction-full-domain']['and_tail'],['obligation:initial-boundary-match','obligation:core-columns-full-domain'])
            self.assertIn('obligation:active-support-preservation',routes['route:contraction-restricted-active']['and_tail'])
    def test_distinct_formal_decoder_eight_originals_exact_37_whole_declarations(self):
        with zipfile.ZipFile(BASE/'formal-decoder-c53-original8.zip') as z:
            self.assertEqual(len(z.namelist()),8)
            self.assertEqual(set(z.namelist()),set(json.loads(z.read('allowlist.json'))['files']))
            self.check_manifest(z,'seal.json','9c855eea1016f1e470f03ff915acf377a325a15c802f2df89dac94e1a213ccdd','manifest.json','3b7e437b3f8ac6baf7771daf4dbfa6851cc3f5b1e010811095aaea957f50a95f','files','path')
            packet=json.loads(z.read('public-packet.json'));self.assertEqual(packet['declaration_inventory']['authored'],37)
            self.assertFalse(packet['admission']);self.assertIsNone(packet['independent_reviewer_verdict'])
            self.assertEqual(z.read('public-packet.json'),(BASE/'decoder-c53-packet.json').read_bytes())
            self.assertEqual(z.read('reconstruction.md'),(BASE/'decoder-c53-reconstruction.md').read_bytes())
    def test_all_archived_raw_and_recursive_path_values_are_publicsafe(self):
        bad=re.compile(r'[A-Za-z]:[\\/]|(?:github_pat_|ghp_)[A-Za-z0-9_]{20,}|'+re.escape('/'+'/'.join(('home','runner'))+'/'),re.I)
        def strings(obj):
            if isinstance(obj,dict):
                for k,v in obj.items():yield k;yield from strings(v)
            elif isinstance(obj,list):
                for v in obj:yield from strings(v)
            elif isinstance(obj,str):yield obj
        for path in BASE.glob('*.zip'):
            with zipfile.ZipFile(path) as z:
                for name in z.namelist():
                    text=z.read(name).decode();values=[] if name.endswith('.json') else [text]
                    if name.endswith('.json'):values += list(strings(json.loads(text)))
                    if name.endswith('.py'):values += [n.value for n in ast.walk(ast.parse(text)) if isinstance(n,ast.Constant) and isinstance(n.value,str)]
                    self.assertFalse(any(bad.search(s) for s in values),str(path.name)+':'+name)
                    self.assertIsNone(re.search(r'(?:github_pat_|ghp_)[A-Za-z0-9_]{20,}',text))
    def test_JSON_escape_handling_does_not_hide_actual_drive_paths(self):
        path_pattern=re.compile(r'[A-Za-z]:[\\/]')
        mathematical={'formula':'R:'+chr(10)+'sum'}
        raw=json.dumps(mathematical)
        self.assertIsNotNone(path_pattern.search(raw))
        self.assertFalse(any(path_pattern.search(s) for s in json.loads(raw).values()))
        actual=chr(67)+':'+chr(92)+'example'+chr(92)+'file'
        self.assertTrue(any(path_pattern.search(s) for s in json.loads(json.dumps({'path':actual})).values()))
        encoded='{"path":"'+chr(92)+'u0043:'+chr(92)+'u005c'+'example"}'
        self.assertTrue(any(path_pattern.search(s) for s in json.loads(encoded).values()))
if __name__=='__main__':unittest.main()
