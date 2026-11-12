import unittest
import assessment as a


class DeltaTests(unittest.TestCase):
    def test_nested_comments_and_string_data(self):
        raw=b'/- import Bad /- nested -/ -/\nimport A B\ndef s := "import Preserved"\n'
        self.assertEqual(a.imports(raw),['A','B'])
        self.assertIn(b'"import Preserved"',a.masked(raw))
        self.assertEqual(len(raw),len(a.masked(raw)))
    def test_public_multimodule_import(self):
        self.assertEqual(a.imports(b'module\npublic import A B.C\n'),['A','B.C'])
    def test_missing_project_import(self):
        with self.assertRaises(ValueError):a.graph({'QuantumBlockEncoding/X.lean':b'import QuantumBlockEncoding.Missing\n'})
    def test_unknown_import_syntax(self):
        with self.assertRaises(ValueError):a.imports(b'import A; import B\n')
    def test_transitive_changed_import(self):
        g,_=a.graph({'QuantumBlockEncoding/A.lean':b'import QuantumBlockEncoding.B\n',
                     'QuantumBlockEncoding/B.lean':b'import QuantumBlockEncoding.CubicStatePreparation\n',
                     'QuantumBlockEncoding/CubicStatePreparation.lean':b'def x:=1\n'})
        self.assertIn('QuantumBlockEncoding/CubicStatePreparation.lean',a.closure(g,'QuantumBlockEncoding/A.lean'))
    def test_cycle_termination(self):
        self.assertEqual(a.closure({'A':['B'],'B':['A']},'A'),['A','B'])
    def test_data_change_rejected(self):
        with self.assertRaises(ValueError):a.proof_delta(b'def x:=1\ntheorem p:=by native_decide\n',b'def x:=2\ntheorem p:=by decide +kernel\n')
    def test_proof_revert_suffix_preserved(self):
        self.assertEqual(len(a.proof_delta(b'theorem p:=by native_decide +revert\n',b'theorem p:=by decide +kernel +revert\n')),1)
    def test_suffix_drop_rejected(self):
        with self.assertRaises(ValueError):a.proof_delta(b'theorem p:=by native_decide +revert\n',b'theorem p:=by decide +kernel\n')
    def test_duplicate_json(self):
        with self.assertRaises(ValueError):a.parse('{"x":1,"x":2}')
    def test_docs_catalog_excluded(self):
        self.assertFalse(a.formal_path('docs/lesson.md'));self.assertFalse(a.formal_path('website/research/sources.json'))
        self.assertTrue(a.formal_path('QuantumBlockEncoding/X.lean'));self.assertTrue(a.formal_path('lakefile.lean'))
    def test_no_path_escape(self):
        with self.assertRaises(ValueError):a.safe_path('../reviewer.json')


if __name__=='__main__':unittest.main(verbosity=2)
