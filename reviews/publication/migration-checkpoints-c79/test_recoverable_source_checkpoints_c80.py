"""Transport and exact acceptance scope; not a mathematical verifier."""
import hashlib,importlib.util,json,unittest,zipfile
from pathlib import Path
BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
SHA=lambda raw:hashlib.sha256(raw).hexdigest()
def privacy_scanner():
    spec=importlib.util.spec_from_file_location('privacy',ROOT/'reviews/publication/robin-fixed-routes-c45/test_privacy_transport_c70.py')
    privacy=importlib.util.module_from_spec(spec);spec.loader.exec_module(privacy)
    return privacy.scan_public_transport
def scan_public_checkpoint(name,raw):
    sources={'hermite-boundary-c74-topology-author-successor/natural-source.md':'69f7b917b21e70ca98285530571b11668ea69333f8fdcc0cfca43b19cf898018',
        'hermite-boundary-c74-topology-author-successor/source-coverage.json':'95b198eaf46578ccbf83c154647a8020bbb36d1c8dda2f0712849a60ad6c5021'}
    if name in sources and SHA(raw)==sources[name]:
        cast_text='(j:'+chr(92)+'mathbb R)'
        cast=(json.dumps(cast_text)[1:-1] if name.endswith('.json') else cast_text).encode()
        assert raw.count(cast)==1
        return privacy_scanner()(name,raw.replace(cast,b'(natural j cast to real)'))
    if name=='PUBLIC/chapter-stage1.md' and SHA(raw)=='5cbc1c6d2a43c34a0d9fcbf79dd33e3adff5f49f6a40b227ac5a85f3d5612321':
        derivative=raw
        for term,typ in [('e','String'),('s','Fin'),('H','Matrix')]:
            cast=(term+':'+chr(92)+'mathrm{'+typ+'}').encode()
            assert derivative.count(cast)==1
            derivative=derivative.replace(cast,(term+' has type '+typ).encode())
        return privacy_scanner()(name,derivative)
    return privacy_scanner()(name,raw)
class RecoverableCheckpointTests(unittest.TestCase):
    def receipt(self):
        return json.loads((ROOT/'reports/lean-433-migration/c80-recoverable-source-checkpoints.json').read_bytes())
    def test_every_archive_member_remains_exact_and_public_allowlisted(self):
        receipt=self.receipt();self.assertEqual(len(receipt['packages']),7)
        self.assertEqual(sum(len(p['members']) for p in receipt['packages']),78)
        for item in receipt['packages']:
            path=ROOT/item['path'];self.assertEqual(SHA(path.read_bytes()),item['sha256'])
            with zipfile.ZipFile(path) as archive:
                self.assertEqual(set(archive.namelist()),{m['path'] for m in item['members']})
                self.assertEqual(SHA(archive.read(item['seal_name'])),item['seal_sha256'])
                for member in item['members']:
                    raw=archive.read(member['path']);self.assertEqual(len(raw),member['bytes']);self.assertEqual(SHA(raw),member['sha256'])
                self.assertFalse(any('/PRIVATE/' in n or 'private-formal/' in n for n in archive.namelist()))
    def test_actual_full_build_has_both_real_commands_and_exact_version(self):
        with zipfile.ZipFile(BASE/'installed-full-lean-80b6187-original.zip') as archive:
            snapshot=json.loads(archive.read('snapshot.json'));result=json.loads(archive.read('result.json'))
        self.assertFalse(snapshot['full_Lean_Tests_success']);self.assertTrue(result['full_Lean_Tests_success'])
        self.assertTrue(result['input_bytes_unchanged']);self.assertIn('version 4.33.0',result['Lean_version'])
        self.assertEqual(result['validated_existing_records'],48);self.assertEqual(len(result['publication_missing_modules']),3)
        report=json.loads((ROOT/'reports/lean-433-migration/c79-installed-full-lean-tests-success.json').read_bytes())
        self.assertEqual(report['actual_commands'],['lake build','lake build Tests'])
        self.assertEqual(report['run']['id'],39049265047);self.assertEqual(report['job']['id'],117444336302)
        self.assertEqual(SHA((BASE/'installed-full-lean-80b6187-original.zip').read_bytes()),report['artifact']['sha256'])
        self.assertGreaterEqual(len(report['actual_terminal_lines']),2)
    def test_current_registry_and_CI_scope_are_not_conflated(self):
        report=json.loads((ROOT/'reports/lean-433-migration/c79-installed-full-lean-tests-success.json').read_bytes())
        self.assertEqual(report['current_committed_inputs_compared'],211);self.assertEqual(report['current_committed_inputs_equal'],209)
        self.assertEqual(report['current_committed_inputs_different'],['website/research/publications.json','website/research/sources.json'])
        self.assertTrue(report['current_205_proof_and_config_inputs_equal']);self.assertTrue(report['current_49_records_separately_validated'])
        self.assertEqual(len(report['current_missing_module_admissions']),2)
        for key in ('main_admitted','publication_complete','scientific_ROOT','Hermite_finitebit_family_root','PURIFIED'):self.assertFalse(report[key])
    def test_HBI_negative_and_source_successor_remain_distinct(self):
        with zipfile.ZipFile(BASE/'hbi-reviewer-c62-topology-stage2-negative-original.zip') as archive:
            negative=archive.read('seal.json').decode()
        with zipfile.ZipFile(BASE/'hbi-reviewer-c62-topology-stage3-successor-original.zip') as archive:
            successor=json.loads(archive.read('seal.json'))
        self.assertIn('NEGATIVE_AS_COMPLETE_SOURCE_TOPOLOGY',negative)
        self.assertEqual(successor['verdict'],'ACCEPT_SOURCE_TOPOLOGY_SUCCESSOR_ONLY')
        self.assertEqual(successor['unresolved_source_topology_blockers'],[])
        self.assertEqual(successor['accepted_objects']['source']['sha256'],self.receipt()['HBI']['source_sha256'])
        self.assertFalse(successor['isolation']['Lean_formal_decoder_or_R_read'])
    def test_Robin_prefix_is_only_author_not_whole_admission(self):
        with zipfile.ZipFile(BASE/'robin-matrix-author-c76-prefix-public13-original.zip') as archive:
            seal=json.loads(archive.read('prefix-seal.json'))
        self.assertEqual(seal['own_read_prefix'],[1,16034]);self.assertEqual(seal['prefix_declarations'],343)
        self.assertEqual(seal['C78_tail_declarations_pending'],334)
        for key in ('whole_semantic_complete','independent_acceptance','production_admission','scientific_ROOT','purification'):self.assertFalse(seal[key])
    def test_Robin_tail_checkpoint_does_not_promote_unread_bodies(self):
        with zipfile.ZipFile(BASE/'robin-matrix-author-c78-tail-stage1-public4-original.zip') as archive:
            seal=json.loads(archive.read('PUBLIC/content-seal-stage1.json'))
        self.assertEqual(seal['read_span'],[16035,19708]);self.assertEqual(seal['fully_read_declarations'],152)
        self.assertEqual(seal['unread_owned_declarations'],182)
        row=self.receipt()['RobinMatrix'];self.assertEqual(row['body_read_total'],495);self.assertEqual(495+182,677)
        self.assertFalse(row['whole_source_complete']);self.assertFalse(row['independent_source_formal_admission'])
    def test_all_public_archive_content_passes_existing_transport_scan(self):
        for item in self.receipt()['packages']:
            with zipfile.ZipFile(ROOT/item['path']) as archive:
                for name in archive.namelist():scan_public_checkpoint(name,archive.read(name))
    def test_exact_mathematical_cast_is_not_a_path(self):
        name='hermite-boundary-c74-topology-author-successor/natural-source.md'
        with zipfile.ZipFile(BASE/'hbi-author-c74-primary-release13-original.zip') as archive:raw=archive.read(name)
        self.assertEqual(scan_public_checkpoint(name,raw),0)
    def test_renamed_or_modified_math_source_is_not_exempt(self):
        name='hermite-boundary-c74-topology-author-successor/natural-source.md'
        with zipfile.ZipFile(BASE/'hbi-author-c74-primary-release13-original.zip') as archive:raw=archive.read(name)
        for path,data in (('other.md',raw),(name,raw+b'\n')):
            with self.assertRaises(AssertionError):scan_public_checkpoint(path,data)
    def test_real_paths_and_credentials_are_rejected(self):
        for raw in ((chr(67)+':'+chr(92)+'private').encode(),('github_'+'pat_'+'x'*25).encode()):
            with self.assertRaises(AssertionError):scan_public_checkpoint('other.md',raw)
if __name__=='__main__':unittest.main()
