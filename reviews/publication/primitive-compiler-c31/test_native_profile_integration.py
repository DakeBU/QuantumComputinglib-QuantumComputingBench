"""Exact optional diagnostic transport and no acceptance authority."""
import hashlib
import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[3]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda p:json.loads(p.read_bytes())

class NativeProfileIntegrationTests(unittest.TestCase):
    def test_exact_original_package_and_parent_transport(self):
        receipt=load(ROOT/'reports/lean-433-migration/c31-native-profile-integration.json')
        for row in receipt['files']:
            # The old receipt is immutable history. Its sole changed file has
            # an exact retained predecessor plus a separately tested successor.
            path=row['path']
            if path=='.github/workflows/c31-native-diagnostic.yml':
                path='tools/primitive_compiler_native_profile_ci2/workflow-before-ci2.yml.txt'
            self.assertEqual(sha(ROOT/path),row['sha256'])
        package=ROOT/'tools/primitive_compiler_native_profile_v1'
        manifest=load(package/'proposal-bindings.json')
        for name,digest in manifest['files'].items():self.assertEqual(sha(package/name),digest)
        profile=load(package/'profile.json')
        self.assertEqual(len(profile['roots']),87)
        for name,digest in profile['projectInputs'].items():self.assertEqual(sha(ROOT/name),digest)

    def test_optional_workflow_original_and_exact_ci2_successor_only(self):
        package=ROOT/'tools/primitive_compiler_native_profile_v1'
        original=(package/'c31-native-diagnostic.workflow.PROPOSAL.yml').read_text()
        expected=original.replace('# PROPOSAL ONLY: parent review/integration required. Not an installed workflow.','# Optional WIP diagnostic; not a required scientific acceptance gate.').replace('name: C31 three-module fresh native diagnostic proposal','name: C31 three-module fresh native diagnostic WIP').replace('    paths:\n',"    paths:\n      - '.github/workflows/c31-native-diagnostic.yml'\n")
        predecessor=ROOT/'tools/primitive_compiler_native_profile_ci2/workflow-before-ci2.yml.txt'
        self.assertEqual(predecessor.read_text(),expected)
        replacements=[
            ("      - 'tools/primitive_compiler_native_profile_v1/**'\n", "      - 'tools/primitive_compiler_native_profile_v1/**'\n      - 'tools/primitive_compiler_native_profile_ci2/**'\n"),
            ("      - name: Set up pinned Lean and inherited dependency caches\n", "      - name: CI2 finite resource gate negative and Python-only tests\n        run: python3 -B -m unittest discover -s tools/primitive_compiler_native_profile_ci2 -p 'test*.py' -v\n      - name: Set up pinned Lean and inherited dependency caches\n"),
            ('        run: lake env python3 tools/primitive_compiler_native_profile_v1/runner.py\n', '        run: lake env python3 -B tools/primitive_compiler_native_profile_ci2/runner_v2.py\n'),
        ]
        receipt=load(ROOT/'reports/lean-433-migration/c31-ci2-native-integration.json')
        self.assertEqual(receipt['workflow_delta'],[dict(before=a,after=b) for a,b in replacements])
        for before,after in replacements:
            self.assertEqual(expected.count(before),1)
            expected=expected.replace(before,after)
        current=ROOT/'tools/primitive_compiler_native_profile_ci3/workflow-before-ci3.yml.txt'
        self.assertEqual(current.read_text(),expected)
        self.assertEqual(sha(current),receipt['workflow_after_sha256'])
        self.assertIn('contents: read',expected);self.assertIn('cancel-in-progress: false',expected)

    def test_ci2_exact_proposal_transport_and_finite_boundary(self):
        attributes=(ROOT/'.gitattributes').read_text()
        self.assertIn('tools/primitive_compiler_native_profile_v1/** -text',attributes)
        self.assertIn('tools/primitive_compiler_native_profile_ci2/** -text',attributes)
        receipt=load(ROOT/'reports/lean-433-migration/c31-ci2-native-integration.json')
        for row in receipt['files']:
            self.assertEqual(sha(ROOT/row['path']),row['sha256'])
        package=ROOT/'tools/primitive_compiler_native_profile_ci2'
        seal=load(package/'ci2-seal.json')
        self.assertEqual(sha(package/'ci2-seal.json'),'373c06cc36e7f043cad97b323f8f6eea15e170f310cf8aa3a17dd9b57a6d430c')
        self.assertEqual(sha(package/'ci2-bindings.json'),seal['ci2ManifestSHA256'])
        for name,digest in load(package/'ci2-bindings.json')['files'].items():
            self.assertEqual(sha(package/name),digest)
        self.assertEqual((receipt['budget_mib'],receipt['reserve_mib'],receipt['minimum_measured_headroom_mib']),(5120,2048,7168))
        self.assertEqual(receipt['parent_tests']['tests_run'],20)
        self.assertEqual(receipt['parent_tests']['exit_code'],0)
        self.assertFalse(receipt['old_local_gate_changed'])
        self.assertFalse(receipt['required_workflows_changed'])
        self.assertFalse(receipt['trusted_verifier_changed'])
        self.assertFalse(receipt['nativeAccepted'])
        self.assertFalse(receipt['scientific_ROOT'])
        self.assertIsNone(receipt['sourceAgreement'])

    def test_actual_python_is_not_native_and_local_gate_failure_is_environment(self):
        receipt=load(ROOT/'reports/lean-433-migration/c31-native-profile-integration.json')
        launch=receipt['local_launch']
        self.assertEqual(launch['Lean_calls'],0);self.assertEqual(launch['lake_calls'],0)
        self.assertLess(launch['commit_free_GiB'],launch['commit_threshold_GiB'])
        self.assertEqual(launch['failure_class'],'ENV_BLOCKED')
        self.assertFalse(receipt['trusted_verifier_changed']);self.assertFalse(receipt['nativeAccepted'])
        parent=load(ROOT/'reports/lean-433-migration/c31-native-profile-parent-check.json')
        self.assertEqual(parent['tests_run'],18);self.assertEqual(parent['exit_code'],0)

    def test_ci3_successor_exact_transport_and_no_gate_relaxation(self):
        receipt=load(ROOT/'reports/lean-433-migration/c31-ci3-native-integration.json')
        for row in receipt['files']:
            self.assertEqual(sha(ROOT/row['path']),row['sha256'])
        package=ROOT/'tools/primitive_compiler_native_profile_ci3'
        self.assertEqual(sha(package/'ci3-seal.json'),'674d09b0be9e9f776d36ec688984587e9e56707749e31772ab0741187c41b418')
        seal=load(package/'ci3-seal.json')
        self.assertEqual(sha(package/'ci3-bindings.json'),seal['manifestSHA256'])
        for name,digest in load(package/'ci3-bindings.json')['files'].items():
            self.assertEqual(sha(package/name),digest)
        old=(package/'workflow-before-ci3.yml.txt').read_text()
        self.assertEqual(sha(package/'workflow-before-ci3.yml.txt'),receipt['workflow_before_sha256'])
        for replacement in receipt['workflow_delta']:
            self.assertEqual(old.count(replacement['before']),1)
            old=old.replace(replacement['before'],replacement['after'])
        predecessor=ROOT/'tools/primitive_compiler_native_profile_ci4/workflow-before-ci4.yml.txt'
        self.assertEqual(predecessor.read_text(),old)
        self.assertEqual(sha(predecessor),receipt['workflow_after_sha256'])
        self.assertIn('contents: read',old);self.assertIn('cancel-in-progress: false',old)
        self.assertIn('tools/primitive_compiler_native_profile_ci3/** -text',(ROOT/'.gitattributes').read_text())
        self.assertEqual((receipt['budget_mib'],receipt['reserve_mib'],receipt['minimum_measured_headroom_mib']),(5120,2048,7168))
        self.assertEqual(receipt['parent_tests']['tests_run'],14)
        self.assertEqual(receipt['parent_tests']['exit_code'],0)
        for field in ('trusted_verifier_changed','required_workflows_changed','old_local_gate_changed','nativeAccepted','scientific_ROOT'):
            self.assertFalse(receipt[field])
        self.assertIsNone(receipt['sourceAgreement'])
        self.assertEqual(len(receipt['workflow_delta']),3)

    def test_ci4_exact_transport_and_sufficient_self_only_contract(self):
        r=load(ROOT/'reports/lean-433-migration/c31-ci4-native-integration.json')
        for row in r['files']:self.assertEqual(sha(ROOT/row['path']),row['sha256'])
        p=ROOT/'tools/primitive_compiler_native_profile_ci4'
        s=load(p/'ci4-seal.json')
        self.assertEqual(sha(p/'ci4-seal.json'),'76e4fa028689e2e713346725f5b554afdc61c817c51464fb379e64fd69d1abf8')
        self.assertEqual(sha(p/'ci4-bindings.json'),s['manifestSHA256'])
        for name,digest in load(p/'ci4-bindings.json')['files'].items():self.assertEqual(sha(p/name),digest)
        old=(p/'workflow-before-ci4.yml.txt').read_text()
        for change in r['workflow_delta']:
            self.assertEqual(old.count(change['before']),1);old=old.replace(change['before'],change['after'])
        self.assertEqual((ROOT/'.github/workflows/c31-native-diagnostic.yml').read_text(),old)
        self.assertEqual(sha(ROOT/'.github/workflows/c31-native-diagnostic.yml'),r['workflow_after_sha256'])
        self.assertEqual((r['budget_mib'],r['reserve_mib'],r['minimum_measured_headroom_mib']),(5120,2048,7168))
        self.assertEqual(r['parent_tests']['tests_run'],17);self.assertEqual(r['parent_tests']['exit_code'],0)
        self.assertFalse(r['PID1_read_requested']);self.assertIsNone(r['PID1_observed_value'])
        for field in ('trusted_verifier_changed','required_workflows_changed','old_local_gate_changed','nativeAccepted','scientific_ROOT'):
            self.assertFalse(r[field])
        self.assertIn('tools/primitive_compiler_native_profile_ci4/** -text',(ROOT/'.gitattributes').read_text())

    def test_actual_ci3_permission_refusal_is_preserved_not_rewritten_as_success(self):
        import zipfile
        r=load(ROOT/'reports/lean-433-migration/c31-actual-ci3-permission-refusal.json')
        self.assertEqual(sha(ROOT/r['archive']),r['archive_sha256'])
        with zipfile.ZipFile(ROOT/r['archive']) as z:
            self.assertEqual(len(z.namelist()),4)
            pre=__import__('json').loads(z.read('ci2-01-help.preflight.json'))
        self.assertFalse(pre['observationComplete']);self.assertFalse(pre['gatePassed'])
        self.assertEqual(pre['failedReadLogicalPath'],'$PROC/pid1/ns/cgroup')
        self.assertEqual(pre['readAttempts'][-1]['errno'],13)
        self.assertEqual(len(pre['namespaceReads']),1);self.assertEqual(pre['cgroups'],[])
        self.assertEqual(r['analysis']['nativeChildrenStarted'],0)
        self.assertNotEqual(r['job_API_head_sha'],r['analysis']['actualContext']['GITHUB_SHA'])
        self.assertIsNone(r['analysis']['executedCheckoutSHA'])

if __name__=='__main__':unittest.main()
