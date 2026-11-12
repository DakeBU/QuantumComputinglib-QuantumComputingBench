import unittest
from axiom_list_parser import parse_axiom_list,ordinary_only

class PrintedAxiomList(unittest.TestCase):
    def test_plain(self):
        self.assertEqual(parse_axiom_list('propext, Classical.choice, Quot.sound'),['propext','Classical.choice','Quot.sound'])
    def test_universes(self):
        self.assertEqual(parse_axiom_list('propext,\n Classical.choice.{u},\n Quot.sound.{u}'),['propext','Classical.choice','Quot.sound'])
        self.assertEqual(parse_axiom_list('Some.unknown.{u, v}'),['Some.unknown'])
    def test_unknown_never_disappears(self):
        for name in ['sorryAx','Lean.ofReduceBool','Lean.trustCompiler','Classical.choice.fake']:
            self.assertFalse(ordinary_only(parse_axiom_list('propext, '+name+'.{u}')))
    def test_malformed_fails(self):
        for s in ['propext; Lean.ofReduceBool','propext,','propext garbage','propext.{u','propext.{u};sorryAx','[propext]']:
            with self.assertRaises(ValueError):parse_axiom_list(s)
    def test_empty_is_not_forged_theorem_output(self):
        self.assertEqual(parse_axiom_list(' '),[])
        self.assertFalse(ordinary_only(['u','Classical.choice.']))

if __name__=='__main__':unittest.main()
