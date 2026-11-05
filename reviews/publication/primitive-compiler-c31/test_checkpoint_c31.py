"""Audit WIP integrity, never Lean, source agreement or publication acceptance."""
import hashlib
import json
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
load = lambda p: json.loads(p.read_bytes())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


class PrimitiveCompilerWIPTests(unittest.TestCase):
    def test_explicit_transports_and_nonacceptance(self):
        old = load(HERE/'parent-stage-transport-c31.json')
        self.assertEqual([len(old[k]) for k in ('author_files','decoder_files','source_first_files')],[29,8,2])
        static = load(HERE/'parent-static-transport-c31.json')
        self.assertEqual(len(static['files']),3)
        self.assertEqual(len({old[k] for k in ('author_identity','decoder_identity','reviewer_identity')}),3)
        for receipt in (old,static):
            self.assertIsNone(receipt['sourceAgreement'])
            self.assertIsNone(receipt['publicationBinding'])
            for flag in ('native_acceptance','main_admission','scientific_ROOT','PURIFIED'):
                self.assertFalse(receipt[flag])
        for row in old['author_files']+old['decoder_files']+old['source_first_files']+static['files']:
            self.assertEqual(sha(ROOT/row['path']),row['sha256'])
            self.assertEqual((ROOT/row['path']).stat().st_size,row['bytes'])

    def test_original_source_and_all_target_bytes(self):
        self.assertEqual(sha(HERE/'source-only.md'),'5907262565b6202fec61b189c42d942cb84d6215223a0da4211d63b92d3ad168')
        self.assertEqual((HERE/'source-only.md').read_bytes(),(ROOT/'docs/lessons/exact-primitive-macros-controlled-rotations-finite-cubic.md').read_bytes())
        context = load(HERE/'author-formal-context.json')
        self.assertEqual(len(context['target_files']),3)
        for row in context['target_files']+context['dependency_context']:
            raw = (ROOT/row['path']).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(),row['sha256'])
            self.assertEqual(''.join(row['full_source_lines']).encode(),raw)

    def test_all_roots_and_lossless_natural_source(self):
        context = load(HERE/'author-formal-context.json')
        roots = context['inventory']
        self.assertEqual(len(roots),87)
        self.assertEqual(len({r['name'] for r in roots}),87)
        self.assertEqual(sum(r['private'] for r in roots),8)
        for row in roots:
            lines = (ROOT/row['module']).read_bytes().splitlines(keepends=True)
            raw = b''.join(lines[row['line']-1:row['source_end_line_before_next_declaration']])
            self.assertEqual(hashlib.sha256(raw).hexdigest(),row['source_block_sha256'])
        coverage = load(HERE/'author-source-coverage.json')
        self.assertEqual(''.join(p['exact_text'] for p in coverage['source_paragraphs']).encode(),(HERE/'source-only.md').read_bytes())
        self.assertEqual(len(coverage['source_paragraphs']),34)
        self.assertEqual(len(coverage['whole_module_inventory']),87)

    def test_decoder_is_source_formal_only(self):
        seal = load(HERE/'decoder-c31/source-formal-seal.json')
        self.assertEqual((seal['sourceDeclarationCount'],seal['privateSourceDeclarations']),(87,8))
        self.assertEqual(seal['leanInvocationCount'],0)
        self.assertEqual(seal['nativeStatus'],'NOT_RUN')
        self.assertEqual(seal['privateGeneratedStatus'],'PENDING_NATIVE_ENVIRONMENT_ENUMERATION')
        self.assertEqual(seal['sourceComparison'],'NOT_PERFORMED')
        self.assertEqual(len(seal['publicSafeAllowlist']),8)
        for name,digest in seal['artifactBindings'].items():
            self.assertEqual(sha(HERE/'decoder-c31'/name),digest)
        for row in seal['targetBindings']:
            self.assertEqual(sha(ROOT/(row['module'].replace('.','/')+'.lean')),row['rawSHA256'])

    def test_original_source_first_chronology_and_static_boundaries(self):
        static = load(HERE/'reviewer-c31/phase2-static-seal.json')
        self.assertTrue(static['original_phase1_natural_context_preserved'])
        self.assertFalse(static['decoder_identity_or_result_read'])
        for row in static['original_phase1_artifacts']:
            self.assertFalse(row['modified'])
            self.assertEqual(sha(HERE/'reviewer-c31'/row['path'].removeprefix('$REVIEWER/')),row['sha256'])
        self.assertIsNone(static['source_agreement_verdict'])
        for key in ('formal_acceptance_claimed','native_acceptance_claimed','root_closure_claimed','main_admission_claimed','purification_claimed'):
            self.assertFalse(static[key])
        self.assertEqual(static['mechanical_source_checks']['all_87_lexical_root_names_and_order_match'],True)

    def test_findings_cannot_be_erased_by_counts(self):
        static = load(HERE/'reviewer-c31/phase2-static-seal.json')
        findings = {r['id']:r for r in static['findings']}
        self.assertEqual(set(findings),{'F1','F2','F3','F4','F5'})
        self.assertEqual(findings['F1']['affected_roots'],['C31-055','C31-056'])
        self.assertTrue(findings['F1']['metadata_correction_needed'])
        self.assertTrue(findings['F2']['metadata_correction_needed'])
        self.assertTrue(findings['F3']['graph_refinement_needed'])
        self.assertFalse(findings['F4']['concrete_boolean_only_certificate'])
        self.assertFalse(findings['F4']['generic_certificate_type_alone_certifies_physics'])
        self.assertEqual(load(HERE/'parent-static-transport-c31.json')['versioned_author_metadata_successor'],'REQUESTED_NOT_ACCEPTED')

    def test_private_original_handoff_is_not_public_derivative_alias(self):
        allow = load(HERE/'public-export/public-allowlist.json')
        originals = [r for r in allow['original_artifacts'] if r['kind']=='EXACT_ORIGINAL_REFERENCE']
        derivatives = [r for r in allow['original_artifacts'] if r['kind']=='PATH_ONLY_DERIVATIVE']
        self.assertEqual((len(originals),len(derivatives)),(22,1))
        for row in derivatives:
            self.assertFalse(row['original_alias'])
            self.assertEqual(sha(ROOT/row['planned_public_path']),row['sha256'])
        self.assertFalse((HERE/'handoff.txt').exists())


if __name__ == '__main__':
    unittest.main()
