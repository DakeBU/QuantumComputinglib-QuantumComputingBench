namespace Fixture
axiom supplied : True
def exposed : Nat := 1
private theorem hidden : True := supplied
opaque sealed : Nat := 2
structure Pair where
  x : Nat
end Fixture
