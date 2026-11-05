"""Actual sealed source/decoder evidence integrity; not a source-fidelity prover."""
import ast,hashlib,json,re,shutil,subprocess,tempfile,unittest,zipfile
from pathlib import Path
BASE=Path(__file__).resolve().parent
SHA=lambda b:hashlib.sha256(b).hexdigest()
def strings(obj):
    if isinstance(obj,dict):
        for k,v in obj.items():yield k;yield from strings(v)
    elif isinstance(obj,list):
        for v in obj:yield from strings(v)
    elif isinstance(obj,str):yield obj
class ActualSourceAndDecoderSuccessorTests(unittest.TestCase):
    def test_actual_source_successor_has_only_nine_authorized_payloads(self):
        with zipfile.ZipFile(BASE/'natural-source-v2-stage3-public9.zip') as z:
            self.assertEqual(len(z.namelist()),9)
            self.assertEqual(SHA(z.read('source-topology-review.md')),'95065ce4d1ada2f7bd12e0fa6bbfd168eadae2b04b4eb465c6ee8fc060b5238e')
            finding=json.loads(z.read('typed-findings.json'))
            self.assertEqual(finding['verdict'],'ACCEPT_BOUNDED_SOURCE_TOPOLOGY_SUCCESSOR')
            self.assertEqual(finding['findingHistory'][0]['successorStatus'],'RESOLVED_FOR_PINNED_GRAPH_V4_COVERAGE_V3_ONLY')
            for private in ('scope-manifest.json','SHA256SUMS.json','SEAL.md'):self.assertNotIn(private,z.namelist())
    def test_actual_independent_1669_assertion_diagnostic_replays(self):
        node=shutil.which('node');self.assertIsNotNone(node,'Missing runtime is not a successful check')
        with zipfile.ZipFile(BASE/'natural-source-v2-stage3-public9.zip') as z:
            expected=json.loads(z.read('select-context-checks.json'))
            with tempfile.TemporaryDirectory() as tmp:
                path=Path(tmp)/'check.js';path.write_bytes(z.read('select-context-checks.js'))
                run=subprocess.run([node,str(path)],capture_output=True,check=True,timeout=30)
            self.assertEqual(json.loads(run.stdout),expected)
            self.assertIn('1669',json.dumps(expected));self.assertIn('256',json.dumps(expected))
    def test_old_negative_review_not_silently_upgraded(self):
        with zipfile.ZipFile(BASE/'natural-source-v2-stage2-public6.zip') as z:
            finding=json.loads(z.read('typed-findings.json'))
            self.assertEqual(finding['verdict'],'REQUEST_CHANGES_SOURCE_COVERAGE_ONLY')
            self.assertEqual(finding['findings'][0]['status'],'OPEN')
    def test_decoder_exact_19_allowlist_manifest_and_all17_payload_hashes(self):
        with zipfile.ZipFile(BASE/'decoder-c49-publicsafe-original19.zip') as z:
            self.assertEqual(SHA(z.read('seal.json')),'87be99d0328957ff8c7e09ea1f48d49afde67590a4a28aafcfb1efe182466548')
            seal=json.loads(z.read('seal.json'));manifest=json.loads(z.read('manifest.json'))
            self.assertEqual(SHA(z.read('manifest.json')),seal['manifestSha256'])
            self.assertEqual(len(z.namelist()),19)
            self.assertEqual(set(z.namelist()),set(seal['publicsafeAllowlist']))
            self.assertEqual(set(z.namelist()),set(manifest['publicsafeAllowlist']))
            self.assertEqual(set(z.namelist()),set(json.loads(z.read('publicsafe-allowlist.json'))['files']))
            self.assertEqual(len(manifest['artifacts']),17)
            for row in manifest['artifacts']:
                self.assertEqual(SHA(z.read(row['file'])),row['sha256']);self.assertEqual(len(z.read(row['file'])),row['bytes'])
    def test_raw_math_and_signature_captures_not_changed_by_privacy_transport(self):
        with zipfile.ZipFile(BASE/'decoder-c49-publicsafe-original19.zip') as z:
            self.assertEqual(SHA(z.read('reconstruction.md')),'ebd11e8da0663f9ddb46eba785c72437d382303cc10aa7155112419f6e8dc167')
            self.assertEqual(SHA(z.read('declaration-inventory.json')),'aabcebada0e5a5686a397796ba9515aa8af0af0f16fa635dd87c13c565db3121')
            self.assertEqual(z.read('reconstruction.md'),(BASE/'decoder-c49-reconstruction.md').read_bytes())
            self.assertEqual(z.read('source-blind-packet.json'),(BASE/'decoder-c49-source-blind-packet.json').read_bytes())
            inventory=json.loads(z.read('declaration-inventory.json'))
            self.assertEqual(len(inventory['targets']),9)
            self.assertEqual(sum(len(t['declarations']) for t in inventory['targets']),215)
    def test_original_privacy_failure_and_control_mismatch_are_retained(self):
        with zipfile.ZipFile(BASE/'decoder-c49-publicsafe-original19.zip') as z:
            origin=json.loads(z.read('origin-binding.json'));delta=json.loads(z.read('privacy-delta-v1.json'))
            self.assertEqual(origin['originalManifestCount'],13);self.assertEqual(origin['originalStandaloneAllowlistCount'],15)
            self.assertEqual(delta['pathValueReplacementCount'],208)
            self.assertEqual(delta['finding'],'ACTUAL_PUBLICATION_PRIVACY_FAILURE')
            self.assertNotIn('build_packet.py',z.namelist())
            self.assertEqual(origin['publicationDigest'],'NOT_SUPPLIED_NO_BINDING_WRAPPER_CREATED')
    def test_every_published_payload_raw_and_recursive_values_are_path_safe(self):
        runner='/'+'/'.join(('home','runner'))+'/'
        unsafe=re.compile(r'[A-Za-z]:[\\/]|'+re.escape(runner)+r'|(?:github_pat_|ghp_)[A-Za-z0-9_]{20,}',re.I)
        with zipfile.ZipFile(BASE/'decoder-c49-publicsafe-original19.zip') as z:
            for name in z.namelist():
                text=z.read(name).decode();values=[text]
                if name.endswith('.json'):values+=list(strings(json.loads(text)))
                if name.endswith('.py'):values += [n.value for n in ast.walk(ast.parse(text)) if isinstance(n,ast.Constant) and isinstance(n.value,str)]
                self.assertFalse(any(unsafe.search(s) for s in values),name)
if __name__=='__main__':unittest.main()
