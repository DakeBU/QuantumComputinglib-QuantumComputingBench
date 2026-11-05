"""Check exact scoped evidence, never turn an external build into admission."""
import hashlib,json,re,unittest,zipfile
from pathlib import Path
BASE=Path(__file__).resolve().parent
SHA=lambda raw:hashlib.sha256(raw).hexdigest()
class UncomputeCompatibilityEvidenceTests(unittest.TestCase):
    def report(self):return json.loads((BASE/'compatibility-observation.json').read_bytes())
    def test_archive_members_and_licenses_remain_exact(self):
        report=self.report();self.assertEqual(len(report['archives']),2)
        for item in report['archives']:
            path=BASE/Path(item['path']).name;self.assertEqual(SHA(path.read_bytes()),item['sha256'])
            with zipfile.ZipFile(path) as archive:
                self.assertEqual(set(archive.namelist()),{m['path'] for m in item['members']})
                for member in item['members']:
                    raw=archive.read(member['path']);self.assertEqual(SHA(raw),member['sha256']);self.assertEqual(len(raw),member['bytes'])
        with zipfile.ZipFile(BASE/'upstream-divsteps-inputs-64b5a13-original.zip') as archive:
            self.assertEqual(len(archive.namelist()),5);self.assertIn('LICENSE',archive.namelist());self.assertIn('lean/divsteps/LICENSE-safegcd-bounds',archive.namelist())
            for path,digest in report['input_hashes'].items():self.assertEqual(SHA(archive.read(path)),digest)
    def test_initial_memory_failure_is_not_erased_or_mathematical(self):
        first=self.report()['initial_attempt'];self.assertEqual(first['status'],'ENV_MEMORY_LIMIT')
        self.assertEqual(first['memory_limit_MiB'],1024);self.assertEqual(first['Defs_exit_code'],0);self.assertNotEqual(first['NumberTheory_exit_code'],0)
        self.assertIn('not a theorem',first['diagnostic'])
    def test_capacity_successor_has_actual_outputs_and_safe_measured_margin(self):
        row=self.report()['successor_attempt'];self.assertTrue(row['all_four_commands_succeeded'])
        self.assertEqual([m['module'] for m in row['modules']],['Defs','NumberTheory','Recovery','Audit'])
        self.assertTrue(all(m['exit_code']==0 for m in row['modules']))
        self.assertGreaterEqual(row['observed_available_MiB'],row['memory_limit_MiB']+row['reserve_MiB'])
        self.assertEqual(row['memory_limit_MiB'],1536);self.assertEqual(row['reserve_MiB'],2048)
        self.assertIn('version 4.33.0',self.report()['observed_Lean'])
    def test_four_reported_axiom_sets_are_exact_and_not_a_whole_project_claim(self):
        report=self.report();text=(BASE/'actual-types-and-axioms.txt').read_text()
        self.assertEqual(len(report['actual_axiom_lines']),4)
        for name,line in zip(report['selected_theorems'],report['actual_axiom_lines']):
            self.assertEqual(line,"'"+name+"' depends on axioms: [propext, Classical.choice, Quot.sound]")
            self.assertIn(line,text)
        self.assertNotIn('sorryAx',text);self.assertNotIn('Lean.ofReduceBool',text)
    def test_source_only_original_is_not_self_approved(self):
        with zipfile.ZipFile(BASE/'appendix-source-first-c81-original8.zip') as archive:
            self.assertEqual(len(archive.namelist()),8)
            self.assertEqual(SHA(archive.read('seal.json')),self.report()['source_first']['seal_sha256'])
            self.assertEqual(SHA(archive.read('manifest.json')),self.report()['source_first']['manifest_sha256'])
            manifest=json.loads(archive.read('manifest.json'))
            self.assertEqual(manifest['evidence_class'],'SOURCE_ONLY');self.assertEqual(manifest['approval_status'],'none')
    def test_no_production_or_full_paper_admission_is_manufactured(self):
        report=self.report();self.assertTrue(report['compiled_external_asset_only'])
        for key in ('production_Lean_changed','publication_registry_changed','independent_source_formal_admission','full_upstream_project_built','DQI_built','native590_certificate_built','full_circuit_verified','new_ASPBE_theorem_credit','scientific_ROOT','PURIFIED'):
            self.assertFalse(report[key],key)
    def test_public_observations_and_originals_contain_no_host_paths_or_credentials(self):
        items=[(p.name,p.read_bytes()) for p in BASE.iterdir() if p.is_file() and p.suffix!='.zip']
        for archive_path in BASE.glob('*.zip'):
            with zipfile.ZipFile(archive_path) as archive:items.extend((name,archive.read(name)) for name in archive.namelist())
        for name,raw in items:
            text=raw.decode('utf-8-sig')
            self.assertIsNone(re.search(r'(?<![A-Za-z0-9])[A-Za-z]:[\\/](?:Users|qb261009)',text),name)
            self.assertNotIn('/'+'/'.join(('home','runner'))+'/',text,name)
            self.assertIsNone(re.search(r'(?:github_'+'pat_|gh'+'p_)[A-Za-z0-9_]{20,}',text),name)
if __name__=='__main__':unittest.main()
