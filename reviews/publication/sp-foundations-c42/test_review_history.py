"""Frozen packaging failures are detected and retained, never called acceptance."""
import hashlib,importlib.util,json,pathlib,unittest,zipfile
ROOT=pathlib.Path(__file__).resolve().parents[3];HERE=pathlib.Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def members(name):
    with zipfile.ZipFile(HERE/name) as z:return {n:z.read(n) for n in z.namelist()}
def data(name,member):return json.loads(members(name)[member])
class FoundationReviewHistory(unittest.TestCase):
    def test_seven_exact_capsules_and_original_seals(self):
        report=json.loads((ROOT/'reports/lean-433-migration/c42-sp-foundations-review-history.json').read_bytes())
        self.assertEqual([x['members'] for x in report['archives']],[25,3,6,6,6,7,15])
        for a in report['archives']:
            p=ROOT/a['path'];self.assertEqual(sha(p.read_bytes()),a['sha256']);f=members(p.name)
            self.assertEqual(len(f),a['members'])
            if 'seal' in a:self.assertEqual(sha(f[a['seal']]),a['seal_sha256'])
        self.assertFalse(report['registry_changed']);self.assertFalse(report['mathematical_route_refuted'])
    def test_four_cost_conclusions_are_really_truncated_and_not_accepted(self):
        inv=data('author-v1-frozen-wip.zip','declaration-inventory.json')['declarations']
        finding=data('source-first-phase3-changes-required.zip','findings-and-erratum.json')
        cost=next(x for x in finding['findings'] if x['id']=='I-COST-SIGNATURE-TRUNCATION')
        formal=members('formal-only-original15.zip');by={x['source_name']:x for x in inv}
        self.assertEqual(len(cost['affected_and_proposed_complete_signature']),4)
        for x in cost['affected_and_proposed_complete_signature']:
            broken=by[x['name']]['signature_or_structure_fields']
            self.assertTrue(broken.rstrip().endswith('{ auxiliaryQubits'));self.assertNotIn('oracleCalls',broken)
            self.assertIn(x['complete_signature'],formal[x['target']].decode())
            self.assertTrue(x['complete_signature'].endswith('oracleCalls := 0 }'))
    def test_21_partial_record_headers_and_real_graph_defects_are_retained(self):
        finding=data('source-first-phase3-changes-required.zip','findings-and-erratum.json')
        bad=next(x for x in finding['findings'] if x['id']=='I-RECORD-HEADER-SUFFIX')
        self.assertEqual(len(bad['affected_lexical_names']),21)
        inv=data('author-v1-frozen-wip.zip','declaration-inventory.json')['declarations']
        for name in bad['affected_lexical_names']:
            row=next(x for x in inv if x['source_name'].endswith('.'+name))
            self.assertIn('where',row['signature_or_structure_fields'])
        graph=data('source-first-phase3-changes-required.zip','author-topology-review.json')
        self.assertEqual(graph['complete_topology_approval'],'WITHHELD_CHANGES_REQUIRED')
        edges={x['id']:x for x in graph['edge_reviews']}
        self.assertEqual(edges['TREE']['result'],'MISSING_FACTORIZED_BRIDGE')
        self.assertEqual(edges['FACTORIZED']['result'],'MISSING_STATE_ACTION_BRIDGE')
        self.assertEqual(edges['PRODUCT-MATRIX']['result'],'VALID_ROUTE_BUT_ALTERNATIVES_MISSING')
    def test_actual_chronology_and_207_unchanged_raw_pins(self):
        p1=data('source-first-phase1-c41-public.zip','natural-only-seal.json')
        p2=data('source-first-phase2-c41-public.zip','phase2-seal.json')
        p3=data('source-first-phase3-changes-required.zip','phase3-seal.json')
        self.assertEqual(p2['prior_natural_only_seal_sha256'],sha(members('source-first-phase1-c41-public.zip')['natural-only-seal.json']))
        self.assertFalse(p2['exposure_attestation']['new_formal_decoder_read_before_this_seal'])
        self.assertFalse(p3['exposure_attestation']['prospective_metadata_or_current_binding_read'])
        self.assertEqual(p3['failure_class'],'IMPLEMENTATION_FAILED')
        source=members('author-v1-frozen-wip.zip')['natural-source.md']
        self.assertEqual(sha(source),p1['source']['sha256'])
        pins=data('author-v1-frozen-wip.zip','raw-input-seals.json')['rows'];self.assertEqual(len(pins),207)
        for x in pins:self.assertEqual(sha((ROOT/x['path']).read_bytes()),x['sha256'])
    def test_original_admission_validator_rejects_all_null_evidence_records(self):
        spec=importlib.util.spec_from_file_location('sp_history_gate',ROOT/'website/scripts/check_research_publications.py')
        gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
        obj=data('metadata-v1-prospective-wip.zip','prospective-records.json')
        records=obj['records'];self.assertEqual(len(records),3)
        for r in records:
            self.assertIsNone(r['decoder_evidence']);self.assertIsNone(r['reviewer_evidence'])
            with self.assertRaisesRegex(ValueError,'publication lacks decoder_evidence'):gate.validate_record(ROOT,r,{})
if __name__=='__main__':unittest.main()
