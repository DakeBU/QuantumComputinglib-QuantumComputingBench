"""Topology/finite-bit-map diagnostics only, not exact complex or Lean acceptance."""
import hashlib,json,unittest,zipfile
from pathlib import Path
BASE=Path(__file__).resolve().parent
SHA=lambda b:hashlib.sha256(b).hexdigest()
class SelectContextSuccessorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.new=zipfile.ZipFile(BASE/'select-context-c50-author-proposal5.zip')
        cls.old=zipfile.ZipFile(BASE/'natural-source-v2-author-original18.zip')
        cls.addClassCleanup(cls.new.close);cls.addClassCleanup(cls.old.close)
        cls.graph=json.loads(cls.new.read('source-graph-v4-proposal.json'))
        cls.previous=json.loads(cls.old.read('source-graph-v3-proposal.json'))
    def test_exact_five_file_transport_and_pinned_positive_graph(self):
        self.assertEqual(set(self.new.namelist()),{'public-review-allowlist.json','repair-ledger.json','select-context-construction-audit.md','source-coverage-v3-proposal.json','source-graph-v4-proposal.json'})
        self.assertEqual(SHA(self.new.read('source-graph-v4-proposal.json')),'eb559adfcb49ed3760de99f28a9cc1b7baebf480927a867cdce3d684ad877e18')
        self.assertEqual(SHA(self.new.read('source-coverage-v3-proposal.json')),'e1f3c17e0ea3d0fcf1a853eed4b74f21b74f4dfecf5694fd02c6c79099db6137')
    def test_all_original_nodes_edges_nonedges_and_projected_OR_unchanged(self):
        new={n['id']:n for n in self.graph['nodes']}
        old={n['id']:n for n in self.previous['nodes']}
        self.assertEqual(len(old),73);self.assertEqual(len(new),74)
        self.assertEqual({n:new[n] for n in old},old)
        previous={e['id']:e for e in self.previous['edges']}
        current={e['id']:e for e in self.graph['edges']}
        self.assertEqual(len(previous),20);self.assertEqual(len(current),21)
        self.assertEqual({e:current[e] for e in previous},previous)
        for key in ('non_edges','alternative_routes'):self.assertEqual(self.graph[key],self.previous[key])
    def test_complete_AND_suppliers_not_a_new_public_premise_or_OR(self):
        edge=next(e for e in self.graph['edges'] if e['id']=='E20-CONTEXT-SELECT8')
        self.assertEqual(edge['mode'],'AND');self.assertEqual(edge['heads'],['SELECT8-CONTEXT'])
        self.assertEqual(edge['tails'],['N06','N08','N14','N22'])
        node=next(n for n in self.graph['nodes'] if n['id']=='SELECT8-CONTEXT')
        self.assertTrue(node['not_final_anchor_binder']);self.assertTrue(node['not_an_OR_winner'])
        self.assertIn('REQUIRES_ACTUAL_INDEPENDENT_REVIEW',node['status'])
    def test_same_lossless_source_only_four_semantic_associations_changed(self):
        coverage=json.loads(self.new.read('source-coverage-v3-proposal.json'))['lines']
        prior=json.loads(self.old.read('source-proof-coverage-proposal.json'))['lines']
        self.assertEqual(len(coverage),414)
        self.assertEqual(''.join(r['text'] for r in coverage).encode(),self.old.read('natural-source-v2.md'))
        self.assertEqual([r['line'] for r in coverage],list(range(1,415)))
        self.assertEqual([a['line'] for a,b in zip(coverage,prior) if a!=b],[181,182,183,184])
    def test_literal_all256_input_permutation_matches_supplied_dirty_formulas(self):
        images=[];dirty_not_ideal=0
        for value in range(256):
            bits=[(value>>i)&1 for i in range(8)];actual=bits.copy()
            actual[3]^=1;actual[4]^=1
            for controls,target in (((3,0),7),((7,1),2),((3,0),7),((3,0),1),((3,),0),((4,1),2),((4,),1),((5,),2)):
                flip=1
                for c in controls:flip &= actual[c]
                actual[target]^=flip
            actual[3]^=1;actual[4]^=1
            a0,a1,a2=bits[:3];s=sum(bits[3+i]<<i for i in range(3));b=s^3
            b0,b1,b2=((b>>i)&1 for i in range(3));w=bits[7]
            u=w^(b0&a0);v2=a2^(u&a1);v1=a1^(b0&a0)
            expected=[a0^b0,v1^b1,v2^(b1&v1)^b2,*bits[3:7],w]
            self.assertEqual(actual,expected)
            result=sum(actual[i]<<i for i in range(3));ideal=(value%8+b)%8
            if not w:self.assertEqual(result,ideal)
            elif result!=ideal:dirty_not_ideal+=1
            images.append(sum(bit<<i for i,bit in enumerate(actual)))
        self.assertEqual(len(set(images)),256);self.assertGreater(dirty_not_ideal,0)
    def test_prior_independent_negative_remains_immutable(self):
        with zipfile.ZipFile(BASE/'natural-source-v2-stage2-public6.zip') as z:
            self.assertEqual(SHA(z.read('topology-review.md')),'ef0700add43527c3d97b5f1622ffc0d0bafd2982f0cc9bdea02142e988237e57')
            finding=json.loads(z.read('typed-findings.json'))
            self.assertEqual(finding['verdict'],'REQUEST_CHANGES_SOURCE_COVERAGE_ONLY')
            self.assertEqual(finding['findings'][0]['status'],'OPEN')
if __name__=='__main__':unittest.main()
