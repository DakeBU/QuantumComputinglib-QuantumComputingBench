import unittest
from replay import ROOTS,check_positive,observations

def output():
    return '\n'.join("'"+n+"' depends on axioms: [propext,\n Classical.choice, Quot.sound]" for n in ROOTS)+'\n'

class ObservationTests(unittest.TestCase):
    def test_multiline_exact_roots(self):self.assertEqual(len(check_positive(output())),3)
    def test_empty(self):
        with self.assertRaises(ValueError):check_positive('')
    def test_missing_root(self):
        with self.assertRaises(ValueError):check_positive(output().split("'"+ROOTS[-1])[0])
    def test_wrong_case(self):
        with self.assertRaises(ValueError):check_positive(output().replace(ROOTS[0],ROOTS[0].lower()))
    def test_extra_axiom(self):
        with self.assertRaises(ValueError):check_positive(output().replace('propext','sorryAx',1))
    def test_duplicate_axiom(self):
        with self.assertRaises(ValueError):check_positive(output().replace('propext','propext, propext',1))
    def test_unexpected_warning(self):
        with self.assertRaises(ValueError):check_positive('unexpected warning\n'+output())
    def test_trailing_text(self):
        with self.assertRaises(ValueError):check_positive(output()+'unparsed')
    def test_duplicate_root(self):
        with self.assertRaises(ValueError):check_positive(output()+output())
    def test_negative_requires_exact_name(self):
        with self.assertRaises(ValueError):observations("'wrong' depends on axioms: [sorryAx]",['expected'])

if __name__=='__main__':unittest.main()
