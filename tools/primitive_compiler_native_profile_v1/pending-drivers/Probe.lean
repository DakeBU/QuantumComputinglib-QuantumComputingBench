import QuantumBlockEncoding.PrimitiveMacros
import QuantumBlockEncoding.UniformlyControlledRy
import QuantumBlockEncoding.CubicAmplitudePrimitive
import Profile
set_option pp.deepTerms true
set_option pp.proofs true
set_option pp.explicit true
set_option pp.universes true
set_option pp.fullNames true
set_option pp.privateNames true
set_option pp.funBinderTypes true
set_option pp.piBinderTypes true
set_option pp.notation false
set_option pp.maxSteps 2000000
set_option maxRecDepth 10000
set_option maxHeartbeats 20000000
run_cmd C31Native.collect C31Native.targets C31Native.roots
