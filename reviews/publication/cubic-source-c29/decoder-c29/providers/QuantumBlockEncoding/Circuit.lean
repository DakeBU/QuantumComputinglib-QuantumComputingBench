import QuantumBlockEncoding.Resources

   
                  

                                                                            
                                                                              
                                                    
  

namespace QuantumBlockEncoding

inductive Gate where
  | oneQubit (name : String) (target : Nat)
  | rotationY (target : Nat) (angleLabel : String)
  | rotationZ (target : Nat) (angleLabel : String)
  | cnot (control target : Nat)
  | swap (left right : Nat)
  | multiControlled (controls : List (Nat × Bool)) (body : Gate)
  | oracleCall (name : String)
deriving Repr, DecidableEq

abbrev Circuit := List Gate

namespace Gate

   
                                                             
                                                                             
                                 
  
def resource : Gate -> Resource
  | oneQubit _ _ => Resource.ofCounts 1 0 0
  | rotationY _ _ => Resource.ofCounts 1 0 0
  | rotationZ _ _ => Resource.ofCounts 1 0 0
  | cnot _ _ => Resource.ofCounts 0 1 0
  | swap _ _ => Resource.ofCounts 0 3 0
  | oracleCall _ => Resource.ofCountsWithDepth 0 0 1 0 1
  | multiControlled controls body =>
      body.resource + Resource.ofCounts
        (16 * controls.length) (12 * controls.length) controls.length

end Gate

   
                                                                             
                                                                           
                                                      
  
abbrev CircuitLayer := List Gate

namespace CircuitLayer

def resource (layer : CircuitLayer) : Resource :=
  layer.foldl (fun acc gate => Resource.parallel acc gate.resource) 0

end CircuitLayer

                                                                    
abbrev LayeredCircuit := List CircuitLayer

namespace LayeredCircuit

def resource : LayeredCircuit → Resource
  | [] => 0
  | layer :: rest => CircuitLayer.resource layer + resource rest

def depth (circuit : LayeredCircuit) : Nat :=
  (resource circuit).depth

end LayeredCircuit

namespace Circuit

def resource : Circuit -> Resource
  | [] => 0
  | gate :: rest => Gate.resource gate + resource rest

@[simp] theorem resource_nil : resource [] = 0 := rfl

@[simp] theorem resource_cons (gate : Gate) (rest : Circuit) :
    resource (gate :: rest) = Gate.resource gate + resource rest := rfl

def depth (circuit : Circuit) : Nat :=
  (resource circuit).depth

end Circuit

end QuantumBlockEncoding
