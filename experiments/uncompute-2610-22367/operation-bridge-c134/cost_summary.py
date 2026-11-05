"""Read-only accounting of a recorded trajectory, not an efficiency ablation."""
import hashlib,json,math
from pathlib import Path
from zipfile import ZipFile

HERE=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()

def duration(row):
    value=row['seconds']
    if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value) or value<0:
        raise ValueError('Missing/invalid elapsed observation; never substitute zero')
    if isinstance(row['exit_code'],bool) or not isinstance(row['exit_code'],int):
        raise ValueError('Only actual terminal exit codes enter this recorded subset')
    return value

def summarize():
    rows=[]
    def observed(name,raw,scope):
        row=json.loads(raw)
        rows.append(dict(id=name,record_sha256=sha(raw),source_sha256=row['source_sha256'],
            exit_code=row['exit_code'],observed_wrapper_seconds=duration(row),
            timing_scope=scope,memory_limit_MiB=row['memory_cap_MiB'],
            observed_peak_memory_MiB=None,CPU_seconds=None,provider_calls=None,
            exact_input_tokens=None,exact_output_tokens=None))
    observed('typing-only',(HERE.parent/'operation-bridge-c128/signature-only-observation.json').read_bytes(),
        'Parent monotonic time around subprocess.run; not CPU or provider/internal timing')
    index=json.loads((HERE/'failed-attempts-index.json').read_bytes())
    archive=HERE/'failed-attempts-original.zip'
    if sha(archive.read_bytes())!=index['sha256']:raise ValueError('Failed-attempt archive mismatch')
    with ZipFile(archive) as z:
        for i in range(1,4):
            name=f'attempt-{i}/attempt-{i}.json';raw=z.read(name)
            if sha(raw)!=index['members'][name]['sha256']:raise ValueError('Failure record mismatch')
            observed(f'failed-whole-proof-{i}',raw,
                'Parent monotonic time around subprocess.run; failed work remains included')
    for name,path in [('isolated-diagnosis-probe','controlled-leaf-result.json'),
        ('controlled-whole-integration','compile-observation.json'),
        ('own-output-type-axiom-audit','root-audit-observation.json')]:
        observed(name,(HERE/path).read_bytes(),
            'Parent monotonic wrapper elapsed includes subprocess plus raw-log/feedback recording before sample')
    if len({r['id'] for r in rows})!=len(rows):raise ValueError('Duplicate observations')
    return dict(schema='C141_RECORDED_TRAJECTORY_COST_NOT_ABLATION_V1',
        trajectory='C126 typing; C128 failures1-3; C132 isolated diagnosis; C134 integration and own-output audit',
        observations=rows,recorded_observations=len(rows),
        sum_recorded_wrapper_seconds=round(sum(r['observed_wrapper_seconds'] for r in rows),3),
        failed_whole_proof_wrapper_seconds=round(sum(r['observed_wrapper_seconds'] for r in rows if r['exit_code']!=0),3),
        count_recorded_failed_whole_proofs=sum(r['exit_code']!=0 for r in rows),
        complete_workflow_wall_seconds=None,total_model_calls=None,total_provider_internal_calls=None,
        model_tokens=None,total_CPU_seconds=None,peak_memory_MiB=None,
        stale_or_cancelled_work_total=None,user_or_parent_reconciliation_cost=None,
        observation_sum_is_complete_cost=False,observation_sum_is_full_workflow_latency=False,
        matched_endpoint_ablation=False,independent_repeated_trials=False,
        randomized_arms=False,efficiency_winner=None,
        interpretation='One sequential adaptive trajectory. Failure cost included. No proof-first/screen-first/dual superiority, speedup, best strategy or quantum-resource conclusion.',
        acceptance='Experimental finite-linear root proved_locally in inherited context; scientific/SPBE/Hermite/source admission still open.',
        unknown_policy='Unavailable telemetry is null, never zero, estimated from Goal totals, or silently omitted.',
        production_scheduler_or_scoring_changed=False)

if __name__=='__main__':print(json.dumps(summarize(),indent=2))
