"""Whole-module evidence and byte-transport checks, not source equivalence proofs."""
import hashlib,json,subprocess,unittest
from pathlib import Path

BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
sha=lambda b:hashlib.sha256(b).hexdigest()
class HBIPublicationTests(unittest.TestCase):
    def record(self):
        return next(r for r in json.loads((ROOT/'website/research/publications.json').read_bytes())['records']
                    if r['module']=='QuantumBlockEncoding/HermiteBoundaryInjection.lean')
    def test_full_module_public_set_and_obligations(self):
        r=self.record()
        inv=json.loads((ROOT/'web/library/declarations.json').read_bytes())['declarations']
        names={x['fullName'] for x in inv if x.get('source')==r['module']}
        self.assertEqual(len(names),121)
        self.assertEqual(set(r['declarations']),names)
        self.assertEqual({n for x in r['obligation_map'] for n in x['declarations']},names)
    def test_genuine_distinct_roles_bind_exact_decoder_transport(self):
        r=self.record()
        d=json.loads((ROOT/r['decoder_evidence']).read_bytes())
        v=json.loads((ROOT/r['reviewer_evidence']).read_bytes())
        self.assertEqual(len({r['formalizer'],d['identity'],v['identity']}),3)
        self.assertTrue(d['source_blind']);self.assertTrue(v['anti_anchored'])
        self.assertEqual(v['verdict'],'accepted')
        self.assertEqual(v['decoder_evidence_sha256'],sha((ROOT/r['decoder_evidence']).read_bytes()))
        original=json.loads((BASE/'decoder-role-association-original.json').read_bytes())
        self.assertTrue(all(d[k]==value for k,value in original.items()))
        self.assertFalse(d['envelope_transport']['new_semantic_review_performed'])
    def test_exact_original_lesson_and_git_byte_transport(self):
        p=ROOT/self.record()['lesson_path'];b=p.read_bytes()
        self.assertEqual(sha(b),'69f7b917b21e70ca98285530571b11668ea69333f8fdcc0cfca43b19cf898018')
        self.assertEqual((b.count(b'\r\n'),b.count(b'\n')),(404,404))
        rel=p.relative_to(ROOT).as_posix()
        attr=subprocess.check_output(['git','check-attr','text','--',rel],cwd=ROOT,text=True).strip()
        self.assertTrue(attr.endswith(': text: unset'))
        a=subprocess.check_output(['git','hash-object','--path='+rel,str(p)],cwd=ROOT)
        c=subprocess.check_output(['git','hash-object','--no-filters',str(p)],cwd=ROOT)
        self.assertEqual(a,c)
    def test_additional_config_pin_not_mislabelled_as_scientific_digest_input(self):
        s=json.loads((BASE/'additional-config-pin.json').read_bytes())
        p=s['additional_context']
        self.assertFalse(p['direct_input_to_existing_scientific_binding_digest'])
        self.assertFalse(p['included_in_C112_204_raw_context_vector'])
        self.assertEqual(sha((ROOT/p['path']).read_bytes()),p['current_raw_sha256'])
    def test_frozen_crlf_and_eof_exceptions_are_exact_scoped_with_byte_guards(self):
        paths={'final-review.md':'553473310493305d7881d6142fad9142f5f4253eb33bb394f7622a93d40a0fe1',
               'reviewer.json':'8c3a29a4073973ced54045f0755df5534695c82eaaeadb2aeb95c43da4dec867'}
        for name,digest in paths.items():
            p=BASE/name
            self.assertEqual(sha(p.read_bytes()),digest)
            a=subprocess.check_output(['git','check-attr','whitespace','--',p.relative_to(ROOT).as_posix()],cwd=ROOT,text=True)
            self.assertIn('cr-at-eol',a);self.assertIn('-blank-at-eof',a)
            self.assertIn('trailing-space',a);self.assertIn('space-before-tab',a)
    def test_source_and_graph_originals_match_reviewed_proposal(self):
        r=self.record();self.assertEqual(r['formalizer'],'UNKNOWN')
        self.assertEqual(r['graph_contribution']['classes'],['reorganisation'])
        self.assertEqual(sha((BASE/'source-graph-v2.json').read_bytes()),'c0e6f83e2eb402836a325810bf3ad3c78cee18f4e871f6d1dc426ade3b859aa0')
        self.assertEqual(sha((BASE/'source-coverage.json').read_bytes()),'95b198eaf46578ccbf83c154647a8020bbb36d1c8dda2f0712849a60ad6c5021')
        self.assertIn('No normalized quantum state',r['residual_boundary'])

if __name__=='__main__':unittest.main()
