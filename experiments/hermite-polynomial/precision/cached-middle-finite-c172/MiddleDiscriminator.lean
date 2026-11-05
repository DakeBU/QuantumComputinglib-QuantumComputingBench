import CachedPrimitivesProof

open HermiteCachedPiecewiseStored

def probeInputs : List Rat := [-2,-(1/3),0,1/2,2]
def probeDeltas : List Rat := [-1,0,1/4,1,2,4]

def probeVector (k mode : Nat) : Vector Rat (k+1) := Vector.ofFn fun i =>
  match mode with
  | 0 => 0
  | 1 => (i.val+1 : Nat)
  | 2 => (-1 : Rat)^i.val / (i.val+1 : Nat)
  | _ => ((Int.ofNat ((5*i.val+3)%7)-3 : Int) : Rat)

def genericChecks : List (String × Bool) := (List.range 7).flatMap fun k =>
  probeInputs.flatMap fun e => (List.range 4).flatMap fun mode =>
    let a := probeVector k mode
    let out := (middleFromCache k e a).value
    (List.finRange (2*k+2)).map fun j =>
      (s!"generic k={k},e={e},mode={mode},j={j.val}",
       decide (out[j.val] = middleExpr k e a j))

def actualChecks : List (String × Bool) := (List.range 7).flatMap fun k =>
  probeDeltas.flatMap fun delta =>
    let a := (HermiteChargedSourceCache.produceSourceCache k).value
    let out := (middleFromCache k (HermiteFiniteMiddleSource.expMidpoint delta) a).value
    (List.finRange (2*k+2)).map fun j =>
      (s!"actual k={k},delta={delta},j={j.val}",
       decide (out[j.val] = HermitePiecewiseAssembly.middleCoeffQ k delta j.val))

#eval do
  let generic := genericChecks
  let actual := actualChecks
  IO.println s!"GENERIC_COUNT={generic.length}"
  IO.println s!"ACTUAL_COUNT={actual.length}"
  IO.println s!"GENERIC_PASS={generic.all (fun row => row.2)}"
  IO.println s!"ACTUAL_PASS={actual.all (fun row => row.2)}"
  for row in generic ++ actual do
    if !row.2 then IO.println ("COUNTEREXAMPLE=" ++ row.1)
