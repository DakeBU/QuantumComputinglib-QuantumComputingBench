"""Execute sealed replay/tests, then freeze an immutable local result packet."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(HERE))
from saved_action import (audit_fixture, independent_saved_replay, parse_saved,
                          finite_trig as measured_trig, MeasuredWork)
from qr_residual import read_rational, rational_text


def freeze():
    output = HERE/'result-v1.json'
    if output.exists():
        raise ValueError('refuse overwriting frozen result')
    bindings = json.loads((HERE/'provider-binding-v1.json').read_text())['bindings']
    for row in bindings:
        if hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest() != row['sha256']:
            raise ValueError('finite trig provider binding changed')
    sys.path.insert(0, str(HERE.parent/'finite-trig'))
    from finite_trig import at_degree, dyadic_outward
    fixture = HERE/'fixture-n3-k1-L1'
    start = time.perf_counter()
    result, qchain, dchain = audit_fixture(fixture)
    result['measured_saved_action_seconds'] = time.perf_counter()-start
    result['independent_saved_replay'] = independent_saved_replay(fixture,qchain,dchain)
    manifest = json.loads((fixture/'manifest.json').read_text())
    gates,_ = parse_saved((fixture/'saved.qasm').read_bytes(),manifest,MeasuredWork())
    unique = sorted({g[1]/2 for g in gates if g[0]=='ry'})
    supplier_work = MeasuredWork()
    for x in unique:
        sine,cosine,radius = measured_trig(x,supplier_work)
        external = at_degree(x,96)
        if (radius != external.radius
                or (sine.lo,sine.hi) != dyadic_outward(external.sin_bounds,80)
                or (cosine.lo,cosine.hi) != dyadic_outward(external.cos_bounds,80)):
            raise AssertionError('separately frozen Taylor producer mismatch')
    result['finite_trig_supplier_crosscheck'] = {
        'unique_actual_halfangles': len(unique), 'all_rounded_endpoints_exactly_equal': True,
        'degree':96, 'grid_bits':80, 'provider_bindings':bindings,
        'scope':'finite exact formula agreement, mathematical membership supplier separately compiled; Python/Lean refinement OPEN',
        'work':vars(supplier_work)}
    producer = json.loads((fixture/'producer.json').read_text())
    qr = producer['qr_residual_packet']
    saved = read_rational(result['saved_decimal_to_literal_D_bound_candidate'])
    qr_bound = read_rational(qr['normalized_stored_TT_error_upper'])
    result['same_return_triangle_candidate'] = {
        'saved_decimal_to_literal_D':rational_text(saved),
        'same_D_to_normalized_stored_C_QR_packet':rational_text(qr_bound),
        'saved_decimal_to_normalized_stored_C_candidate':rational_text(saved+qr_bound),
        'candidate_float_diagnostic':float(saved+qr_bound),
        'not_ideal_Hermite_source_bound':True, 'Python_and_gate_refinement_open':True}
    result['producer_observed_calls'] = producer['observed_calls']
    result['producer_QR_certificate_work'] = qr['work']
    result['producer_source_metadata_work'] = {
        'cutoff_pi_terms':producer['source_metadata']['cutoff_pi_terms'],
        'nonpolynomial_decimal_digits':producer['source_metadata']['nonpolynomial_decimal_digits'],
        'core_scalars':producer['source_metadata']['core_scalars'],
        'polynomial_certificates':producer['source_metadata']['polynomial_certificates']}
    test_cmd = [sys.executable,str(HERE/'test_saved_action.py')]
    start = time.perf_counter()
    tested = subprocess.run(test_cmd,cwd=ROOT,capture_output=True,text=True)
    result['consumer_test_execution'] = {
        'command':'.venv/Scripts/python.exe experiments/hermite-polynomial/precision/saved-action/test_saved_action.py',
        'exit_code':tested.returncode,'stdout':tested.stdout,'stderr':tested.stderr,
        'measured_seconds':time.perf_counter()-start}
    if tested.returncode != 0:
        raise AssertionError('sealed consumer tests failed')
    result['authoring_test_corrections'] = [
        'Initial asserted stage counts were corrected against actual immutable manifest184/168/104; no producer output changed.',
        'An adjacent order swap commuted on the tested action and did not discriminate; changed to whole first-stage reversal, which discriminates. No false mathematical route retirement.',
        'Wrong-readout adversary initially had a malformed nested-list index; repaired its own test construction to a dimension-valid endian swap, which discriminates.']
    result['scope_and_handoff'] = {
        'objective':'same-actual-plan-full-garbage-saved-action-compact-TT-diagnostic',
        'delta':'previous DESIGN_ONLY saved-action/full-terminal-TT residual path implemented and actually replayed for OffsetSource n3k1L1',
        'failure_class':'NONE after local test construction corrections',
        'caps':'n<=3,B<=16,<=50000savedprimitives; no moderate/wide claim',
        'all_frozen_inputs_unchanged':True,'per_worker_tokens':'unknown',
        'public_accepted_root':False,'source_blind_review':'not performed',
        'purification':'pending, no PURIFIED claim','live_handles':[],
        'worker_git_mutations':False,'parent_owns_checkpoint_push_review_and_full_repository_gates':True,
        'current_parent_checkpoint':'667cc30e3f52be2fe64233a27d40e24a9864413b',
        'boundary':'Real Taylor membership supplier is separately proved, but concrete Python program, decoder/parser, interval operations, local stage action, readout and uniform source/cost refinement remain OPEN.'}
    source_names = ['saved_action.py','generate_fixture.py','test_saved_action.py','freeze_result.py',
                    'statement-seal-v1.json','consumer-seal-v1.json','provider-binding-v1.json']
    result['source_bindings'] = [{'path':(HERE/name).relative_to(ROOT).as_posix(),
                                  'sha256':hashlib.sha256((HERE/name).read_bytes()).hexdigest()}
                                 for name in source_names]
    encoded = json.dumps(result,indent=2,allow_nan=False)+'\n'
    # Publication leakage is checked before writing the normal producer output.
    if str(ROOT).replace('\\','\\\\') in encoded or 'D:\\\\Users' in encoded:
        raise AssertionError('absolute working path leak')
    output.write_text(encoded,encoding='utf-8',newline='\n')
    return {'status':'FROZEN_FINITE_FULL_SAVED_ACTION_DIAGNOSTIC',
            'result_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),
            'candidate_bound':result['candidate_bound_float_diagnostic'],
            'tests_exit_code':tested.returncode,'source_bindings':result['source_bindings'],
            'scientific_root_closed':False}


if __name__=='__main__':
    print(json.dumps(freeze(),indent=2))
