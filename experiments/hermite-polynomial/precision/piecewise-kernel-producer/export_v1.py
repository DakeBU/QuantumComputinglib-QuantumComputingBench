"""Save the actual returned local stored chain, not an enumerated statevector."""
import json
from pathlib import Path
from fractions import Fraction as Q
from producer import produce,materialize_and_close

obj=materialize_and_close(produce(1,3,Q(2),Q(2)))
def encode(x):
    if isinstance(x,Q):
        return str(x)
    if isinstance(x,tuple):
        return [encode(y) for y in x]
    return x
packet={
    'semantic_layer':'FINITE_EXACT_RATIONAL_STORED_OBJECT_NOT_LEAN_OR_RUNTIME_CERTIFICATE',
    'inputs':{'k':1,'width':3,'R':'2','delta':'2'},
    'dimension':obj.source.dimension,
    'T':obj.source.cutoff,
    'd':obj.source.degree,
    'm':obj.source.middle_degree,
    'cuts_including_N':obj.source.cuts,
    'core_layout':'bit-major column bit*r+b; chronological q0 LSB',
    'stored_local_tables':encode(obj.tables),
    'left_boundary':encode(obj.source.left),
    'right_boundary':encode(obj.source.right),
    'same_returned_closed_chain':encode(obj.chain),
    'generation_schedule_counts':obj.source.cost,
    'same_object_generation_materialization_closure_counts':obj.cost,
    'omitted_costs':['uniform count proof','rational numerator/denominator/GCD/bit work','input encoding','Python/container/hash/index bookkeeping','peak RAM','QR/normalization/angles/gates/physical synthesis'],
}
Path(__file__).with_name('stored-object-v1.json').write_text(json.dumps(packet,separators=(',',':'))+'\n',encoding='utf-8')
print('Saved actual k1,width3,R2,delta2 stored object: D90, signed source; no dense all-word table.')
