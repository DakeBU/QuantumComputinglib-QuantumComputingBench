import copy
import json
from pathlib import Path
import unittest
import validate as check

PACKAGE=Path(__file__).parent


class EvidenceTests(unittest.TestCase):
    def rows(self):
        return [json.loads((PACKAGE/name).read_text(encoding='utf-8')) for name in
            ('PrimitiveMacros.decoder-evidence.json','UniformlyControlledRy.decoder-evidence.json')]

    def test_both_exact_real_identity_and_opaque_bindings(self):
        rows=self.rows(); self.assertEqual({r['module'] for r in rows},set(check.LABELS))
        self.assertEqual(len({r['run_id'] for r in rows}),1)
        for row in rows:
            self.assertTrue(check.validate(row)); self.assertEqual(row['identity'],check.IDENTITY)
            self.assertIsNone(row['source_semantic_agreement'])

    def test_wrong_role_identity_run_or_binding_refused(self):
        row=self.rows()[0]
        for field,value in [('role','reviewer'),('identity','invented-independent-agent'),('run_id','claimed-CI-run'),
            ('binding_sha256',check.LABELS['QuantumBlockEncoding.UniformlyControlledRy'])]:
            bad=copy.deepcopy(row); bad[field]=value
            with self.assertRaises(ValueError): check.validate(bad)

    def test_fake_directory_packet_hash_and_artifact_binding_refused(self):
        row=self.rows()[0]
        for field,value in [('packet_path',str(Path(check.PACKET).parent)),('packet_sha256','0'*64),
            ('artifact_path','invented/result.zip'),('artifact_sha256','f'*64)]:
            bad=copy.deepcopy(row); bad[field]=value
            with self.assertRaises(ValueError): check.validate(bad)

    def test_unscoped_blindness_or_missing_late_context_disclosure_refused(self):
        row=self.rows()[0]
        for field in ('source_blind','source_blind_scope','later_context_disclosure'):
            bad=copy.deepcopy(row); bad.pop(field)
            with self.assertRaises(ValueError): check.validate(bad)
        bad=copy.deepcopy(row); bad['later_context_disclosure']['author_natural_source_read']=True
        with self.assertRaises(ValueError): check.validate(bad)

    def test_no_semantic_identity_from_opaque_label_and_no_status_promotion(self):
        row=self.rows()[0]
        for field in ('label_only','recomputed_by_decoder','semantic_identity_inferred'):
            bad=copy.deepcopy(row); bad['late_opaque_context'][field]=not bad['late_opaque_context'][field]
            with self.assertRaises(ValueError): check.validate(bad)
        for key in check.FORBIDDEN_KEYS:
            bad=copy.deepcopy(row); bad[key]=True
            with self.assertRaises(ValueError): check.validate(bad)
        bad=copy.deepcopy(row); bad['source_semantic_agreement']=True
        with self.assertRaises(ValueError): check.validate(bad)

    def test_exact_index_hashes_and_transport_member_seal(self):
        index=json.loads((PACKAGE/'index.json').read_text(encoding='utf-8'))
        for row in index['rows']:
            self.assertEqual(check.sha((PACKAGE/row['evidence_file']).read_bytes()),row['evidence_sha256'])
        self.assertEqual(check.sha((PACKAGE/'bridge.json').read_bytes()),index['bridge_sha256'])
        bridge=json.loads((PACKAGE/'bridge.json').read_text(encoding='utf-8'))
        self.assertEqual(len(bridge['exact_transport_members']),11)
        self.assertEqual(next(r['sha256'] for r in bridge['exact_transport_members'] if r['path']=='seal.json'),
            '775f7249bcad57053e2622e79f88837220f394375ebb3741d2cc750d5181646d')
        self.assertEqual(bridge['actual_addendum_scope']['roots'],62)
        self.assertEqual(bridge['actual_addendum_scope']['generated'],94)
        check.no_unsupported_claims(bridge)


if __name__=='__main__': unittest.main()
