"""Relative full-source replay; immutable records sanitize diagnostics before creation."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
REL = HERE.relative_to(ROOT).as_posix()


def digest(path):
    return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()


def sanitize(text):
    for p in [str(ROOT),str(ROOT).replace('\\','/'),str(ROOT).replace('/','\\')]:
        text = text.replace(p,'<repo>')
    return re.sub(r'[A-Za-z]:[\\/][^\r\n\'\"<>]*', '<private-path>',text)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--record', choices=['v1'])
    args = parser.parse_args()
    outputs = [HERE/f'gate-v1-{i}.log' for i in range(4)] + [HERE/'result-v1.json']
    if args.record and any(p.exists() for p in outputs):
        raise SystemExit('Refusing to overwrite an immutable evidence record.')
    inputs = sorted([p.relative_to(ROOT).as_posix() for p in HERE.iterdir()
        if p.is_file() and p.suffix in ['.lean','.json','.py','.ps1'] and not p.name.startswith('result')])
    inputs += [
        f'{REL}/.gitignore','lean-toolchain','lake-manifest.json',
        'experiments/hermite-polynomial/precision/finite-trig/FiniteTrig.lean',
        'experiments/hermite-polynomial/precision/saved-action/saved_action.py',
        'experiments/hermite-polynomial/precision/saved-action/statement-seal-v1.json',
        'experiments/hermite-polynomial/precision/qr-residual/qr_residual.py',
        'experiments/hermite-polynomial/precision/saved-action/fixture-n3-k1-L1/saved.qasm',
        'experiments/hermite-polynomial/precision/saved-ry-interval/result-v2.json',
        'experiments/hermite-polynomial/precision/nonunitary-transport/result.json']
    before = {p:digest(p) for p in inputs}
    (HERE/'.cache').mkdir(exist_ok=True)
    env = os.environ.copy()
    env['LEAN_PATH'] = str(HERE/'.cache') + os.pathsep + env.get('LEAN_PATH','')
    commands = [
        ['lake','env','lean','-o',f'{REL}/.cache/FiniteTrig.olean',
            'experiments/hermite-polynomial/precision/finite-trig/FiniteTrig.lean'],
        ['lake','env','lean','-o',f'{REL}/.cache/SavedRounding.olean',f'{REL}/SavedRounding.lean'],
        ['lake','env','lean',f'{REL}/ConsumerChecks.lean'],
        ['.venv/Scripts/python.exe',f'{REL}/test_saved_rounding.py','-v']]
    gates = []
    for i,command in enumerate(commands):
        start = time.perf_counter()
        completed = subprocess.run(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace')
        elapsed = time.perf_counter()-start
        log = sanitize(completed.stdout)
        print(log,end='',flush=True)
        item = {'command':command,'exit_code':completed.returncode,'measured_seconds':elapsed}
        if args.record:
            outputs[i].write_text(log,encoding='utf-8')
            item.update(log=outputs[i].relative_to(ROOT).as_posix(),log_sha256=digest(outputs[i].relative_to(ROOT).as_posix()))
        gates.append(item)
        if completed.returncode:
            print('Focused replay failed; no success result emitted.',flush=True)
            return completed.returncode
    after = {p:digest(p) for p in inputs}
    if before!=after:
        raise SystemExit('Bound source changed during replay; no success result emitted.')
    result = {
        'schema_version':1,'evidence_class':'C_INTERNAL_PROVIDER','status':'PROVED_LOCAL_FOCUSED',
        'objective':'Actual outward-rounded saved RY row interval semantics',
        'mathematical_delta':'Signed integer numerator/denominator floor/ceil formulas, strict <2^-bits outward widening, four-corner real enclosure, unconditional FiniteTrig-to-rounded RY row enclosure, chronological SAME ROW PAIR fold, and end-only midpoint entry radius.',
        'effect_on_root_frontier':'Closes analytic literal interval-row provider. Does not close actual full saved stage or eta operator supplier.',
        'namespace':'HermiteSavedRounding',
        'roots':['scaled_floor_num','scaled_ceil_num','outward_widening','outward_mem','times_mem','sine_mem','cosine_mem','ryRow_mem','rowTrace_mem','midpoint_error','actual_first_saved_ry','literal_column_trace','final_column_center_error'],
        'scope_warning':'rowTrace always acts on the SAME TWO ROWS. It is NOT variable-target/CX full-stage scheduling. The finite CX stage test is diagnostic only.',
        'real_saved_action_link':'saved_action.py computes the identical four corner times, signed row0 c*u-s*v and row1 s*u+c*v, signed // outward after each output, and only then endstage midpoint. Independent exact tests import this immutable producer.',
        'assumptions':'Initial entry enclosures are local row invariants, discharged by literal singleton inputs in column consumers; Taylor sine/cosine enclosure is PRODUCED, not a Valid premise. No surrogate unitarity or operator bound assumed.',
        'conventions':'Signed exact rational decimal half-angle. No phase alignment/quotient, no garbage projection, no dimension or physical q0-LSB change claimed. Row provider is scalar and does not identify physical routing.',
        'downstream_transport':'NonunitaryTransport remains conditional; this package does not yet prove its actual matrix difference norm <= size*entry_radius or nominal-stage contraction.',
        'execution':gates,'bindings_sha256':before,'bound_inputs_unchanged':True,
        'axioms_expected_union':['propext','Classical.choice','Quot.sound'],
        'new_axioms':False,'new_sorry':False,'new_native_decide':False,
        'finite_tests':'4 unittest methods: signed decimals / bits0 / dyadic boundaries, product sign quadrants and cancellation, independent Taylor and row formulas, actual finite CX-interleaved stage center/radius/eta comparison.',
        'failure_class':'NONE',
        'authoring_obstructions':['IMPLEMENTATION_FAILED: real recurrence needed noncomputable; corrected without changing executable rational definitions.','IMPLEMENTATION_FAILED: widening required cancellation of inverse grid and product enclosure required explicit commuted endpoint types; corrected.','API_BLOCKED retrieval probe unknown Rat.divInt_self; use existing Rat.num_div_den instead. This did not refute mathematics.','IMPLEMENTATION_FAILED: decide did not reduce opaque Rat operations; replaced finite kernel checks with norm_num. No native_decide used.'],
        'salvage_audit':'All kept helpers serve actual rounded-row roots; no fake Valid closure. Ignored probe is not evidence.',
        'process_memory_ids':['QBE-PM-LOW-TOKEN-CONTROL-PLANE','QBE-PM-VERIFIER-SEMANTIC-LEVEL','QBE-PM-DENSE-CHECK-SMALL-INSTANCE'],
        'direction_fingerprint':'outward-stage-not-uniform-exp-degree',
        'expected_information_gain':'Resolve actual floor/ceil and signed interval arithmetic instead of repeating raw Taylor midpoint norm bound.',
        'parallel_admission':'Parent assigned independent actual interval uncertainty; no worker subdelegation.',
        'independent_review':'PENDING','common_blind_spot_audit':'Parent-owned pending',
        'default_verified_route':'Literal interval row semantics; no alternative operator-norm route selected.',
        'purification':'Internal helper reachability inspected; public purification and Exposition Seal not claimed.',
        'source_lean_expansion':'Taylor bounds -> signed integer outward formulas -> interval product/sum -> rounded actual RY pair -> chronological SAME PAIR -> end midpoint.',
        'remaining':['Formal Python Fraction/Int // parser/runtime refinement','Variable-target row-pair routing and CX interleaving to actual saved matrix entries','Stage-end matrix midpoint and max-entry-radius, dimension size and Euclidean operator eta bound','Saved stage partition/data-first TT/readout with all garbage','Uniform Hermite family, finite-bit runtime including Fraction GCD and physical synthesis'],
        'recommended_next':'Freeze a physical-index row update/CX instruction semantics and induct its full matrix entry enclosure; derive size*max-entry-radius opnorm before applying NonunitaryTransport.',
        'full_repository_gate':'Parent reports production/Tests and 50 tests passed; not rerun by worker. Focused provider is outside production import graph.',
        'source_anchor_admission':False,'scientific_root_closed':False,'uniform_finite_bit_certificate':False,
        'surrogate_unitarity_assumed':False,'phase_quotient':False,
        'worker_git_mutations':False,'parent_owns_checkpoint':True,
        'context_digest':'5a8f47f8d0afd1d4f957e55babde52a9e9c01babf05c481b988e99ebca2f7758',
        'per_worker_tokens':'unknown'}
    if args.record:
        outputs[-1].write_text(json.dumps(result,indent=2,ensure_ascii=True)+'\n',encoding='utf-8')
        print('Immutable result-v1 SHA256: '+digest(outputs[-1].relative_to(ROOT).as_posix()),flush=True)
    return 0


if __name__=='__main__':
    raise SystemExit(main())
