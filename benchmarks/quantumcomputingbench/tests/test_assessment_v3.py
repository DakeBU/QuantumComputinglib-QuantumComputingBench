"""Public study identity and provenance boundaries, without private questions."""
from copy import deepcopy
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import qcb_assessment_v3 as bank
from qcb_core import digest
from qcb_integrity import text_sha


class StudyCoreGates(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.root = Path(self.tmp.name)
        self.source = self.root / 'QuantumBlockEncoding/Fixture.lean'
        self.source.parent.mkdir(); self.source.write_text('def fixture := True\n')
        self.old = {'cohort_digest': 'a' * 64, 'proof_inputs_sha256': 'b' * 64,
                    'catalog_hash': 'c' * 64, 'snapshot_id': 'snapshot',
                    'library_revision': 'd' * 40, 'lean_toolchain': 'lean4:pinned', 'probe_index': []}
        pairs = [str(uuid4()), str(uuid4())]; rows=[]; cores=[]
        for i in range(4):
            identity = str(uuid4()); core = 'candidate:' + identity
            rows.append({'probe_id': identity, 'pair_id': pairs[i // 2], 'cluster_id': 'promise_register_protocols',
                         'parent_core_ids': [core], 'parent_contracts': {core: 'e' * 64},
                         'split': 'test_public', 'source_nodes': ['declaration:fixture'], 'difficulty_band': 'D2'})
            cores.append({'core_id': core, 'probe_id': identity, 'contract_hash': 'e' * 64,
                          'mechanism_id': ['dirty_flag_involution', 'target_only_control_hoisting'][i // 2],
                          'exposure_group': 'promise_register_protocols', 'canonical_alias': None,
                          'canonical_admission': False, 'source_nodes': ['declaration:fixture']})
        self.seal = {'schema_version': 'qcb.sealed_assessment_extension.v3', 'release_id': 'qcb-sealed-assessment-v3-20261106',
                     'base_v2_seal_digest': digest(self.old), 'base_cohort_digest': self.old['cohort_digest'],
                     'cohort_digest': 'f' * 64, 'private_files_sha256_lf': {'cohort.json': '0' * 64, 'provenance.json': '1' * 64},
                     'provenance_files_sha256_lf': {'provenance/' + n: '2' * 64 for n in bank.PROVENANCE_NAMES},
                     'probe_index': rows, 'study_core_index': cores,
                     'source_bindings': [{'path': 'QuantumBlockEncoding/Fixture.lean', 'sha256_lf': text_sha(self.source)}],
                     **{k: self.old[k] for k in ['proof_inputs_sha256','catalog_hash','snapshot_id','library_revision','lean_toolchain']},
                     'exposure_audit_digest': '3' * 64,
                     'exposure_scope': 'held_out_target_compositions_relative_to_frozen_train_export; shared_subproofs_and_witness_templates; public_library_exposed; pretraining_unknown',
                     'canonical_admissions_changed': False, 'model_performance_measured': False}
        graph = {'declaration:fixture': {'inventory_status': 'Compiled', 'open_obligation': False,
                                          'source': 'QuantumBlockEncoding/Fixture.lean'}}
        self.rpatch = patch.object(bank, 'R', self.root); self.rpatch.start()
        self.gpatch = patch('qcb_curriculum.load_catalog', return_value=({}, None, graph)); self.gpatch.start()
        self.graph = graph

    def tearDown(self):
        self.gpatch.stop(); self.rpatch.stop(); self.tmp.cleanup()

    def test_study_cores_are_not_public_canonical_admissions(self):
        result = bank.validate_seal(self.seal, base_seal=self.old)
        self.assertFalse(result['canonical_admissions_changed'])
        self.assertEqual(len({c['exposure_group'] for c in result['study_core_index']}), 1)

    def test_public_rows_reject_hidden_question_gold_or_rationale(self):
        for field in ['question', 'gold', 'rationale']:
            seal=deepcopy(self.seal);seal['probe_index'][0][field]='SECRET'
            with self.assertRaises(ValueError): bank.validate_seal(seal, base_seal=self.old)
        seal=deepcopy(self.seal);seal['study_core_index'][0]['contract']='SECRET'
        with self.assertRaises(ValueError): bank.validate_seal(seal, base_seal=self.old)

    def test_existing_train_parent_cannot_be_relabelled_as_new_study_core(self):
        seal=deepcopy(self.seal);p=seal['probe_index'][0]
        p['parent_core_ids']=['qcb-core-be-102'];p['parent_contracts']={'qcb-core-be-102':'e'*64}
        with self.assertRaisesRegex(ValueError, 'borrow or relabel'):
            bank.validate_seal(seal, base_seal=self.old)

    def test_alias_admission_or_cross_split_group_is_rejected(self):
        for field,value in [('canonical_alias','qcb-core-be-102'),('canonical_admission',True)]:
            seal=deepcopy(self.seal);seal['study_core_index'][0][field]=value
            with self.assertRaises(ValueError): bank.validate_seal(seal, base_seal=self.old)
        seal=deepcopy(self.seal);seal['probe_index'][0]['split']='dev'
        with self.assertRaises(ValueError): bank.validate_seal(seal, base_seal=self.old)

    def test_new_ids_and_immutable_base_binding_are_required(self):
        seal=deepcopy(self.seal);seal['base_v2_seal_digest']='0'*64
        with self.assertRaisesRegex(ValueError, 'frozen v2'): bank.validate_seal(seal, base_seal=self.old)
        seal=deepcopy(self.seal);seal['probe_index'][0]['probe_id']='polarity-true'
        with self.assertRaises(ValueError): bank.validate_seal(seal, base_seal=self.old)

    def test_closed_compiled_relevant_source_is_required(self):
        self.graph['declaration:fixture']['open_obligation']=True
        with self.assertRaisesRegex(ValueError,'compiled closed'):bank.validate_seal(self.seal,base_seal=self.old)
        self.graph['declaration:fixture']['open_obligation']=False
        self.graph['declaration:fixture']['source']='QuantumBlockEncoding/Other.lean'
        with self.assertRaises(ValueError):bank.validate_seal(self.seal,base_seal=self.old)

    def test_public_qualification_cannot_smuggle_arbitrary_payload(self):
        with patch.object(bank, 'read_json', return_value={'question':'SECRET'}):
            with self.assertRaisesRegex(ValueError,'extension qualification'):
                bank.validate_qualification(self.seal)

    def test_private_paths_cannot_escape_the_owner_bundle(self):
        seal=deepcopy(self.seal);seal['provenance_files_sha256_lf']={'../secret.json':'a'*64}
        with self.assertRaises(ValueError):bank.validate_seal(seal,base_seal=self.old)
        with self.assertRaisesRegex(ValueError,'outside'):
            bank.load_private_bank(self.root/'_out/private')

    def test_contract_identity_does_not_depend_on_a_response_modality(self):
        p={'question':'mathematics','assumptions':[],'conventions':[],
           'formal_context':{'imports':['Fixture'],'proposition':'True'},
           'gold':{'answer':'not an input to the contract'}}
        before=digest(bank.study_contract(p,[]));p['gold']={'answer':'different grader reference'}
        self.assertEqual(before,digest(bank.study_contract(p,[])))
        p['formal_context']['proposition']='False'
        self.assertNotEqual(before,digest(bank.study_contract(p,[])))

    def test_approved_metadata_slots_cannot_contain_nested_or_free_text_secrets(self):
        for value in [{'question': 'SECRET'}, 'private answer is true']:
            seal=deepcopy(self.seal);seal['release_id']=value
            with self.assertRaisesRegex(ValueError,'release identifier'):
                bank.validate_seal(seal,base_seal=self.old)
        seal=deepcopy(self.seal)
        seal['provenance_files_sha256_lf']={'provenance/private-answer-is-true.json':'a'*64}
        with self.assertRaisesRegex(ValueError,'neutral fixed'):
            bank.validate_seal(seal,base_seal=self.old)

    def test_receipt_envelope_cannot_contradict_no_model_nonisolated_scope(self):
        from qcb_learning_reference import REFERENCE_PROFILE
        packet={};seal={};q={'source_commit':'a'*40}
        r={'schema_version':'qcb.private_assessment_references.v3','seal_digest':digest(seal),
           'cohort_digest':digest(packet),'source_commit':q['source_commit'],'tested_code_commit':q['source_commit'],
           'pipeline_source_hashes_lf':{},'semantic_review':{},'profile':REFERENCE_PROFILE.copy(),
           'passed':True,'results':[],'transport_results':[],'new_reference_checks':{},'elapsed_seconds':1.0,
           'execution_class':'trusted_local_authored_reference','isolated':False,'model_calls':0,
           'model_performance_measured':False}
        bank.validate_receipt_header(packet,seal,q,r)
        for key,value in [('passed',False),('isolated',True),('model_calls',True),('model_calls',1),
                          ('model_performance_measured',True),('elapsed_seconds',float('nan')),
                          ('elapsed_seconds',float('inf')),('elapsed_seconds',True),
                          ('cohort_digest','0'*64),('source_commit','b'*40),('profile',{})]:
            with self.subTest(key=key,value=value):
                changed=deepcopy(r);changed[key]=value
                with self.assertRaises(ValueError):bank.validate_receipt_header(packet,seal,q,changed)


if __name__ == '__main__': unittest.main()
