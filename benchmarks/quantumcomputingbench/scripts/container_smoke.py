#!/usr/bin/env python3
"""Execute only reviewed CPU fixtures in the portable student/grader containers."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if sys.platform != 'linux':
        parser.error('The actual Docker acceptance gate runs on a Linux Docker host.')
    bundle, output = args.bundle.resolve(), args.output.resolve()
    if output.exists():
        parser.error('Preserve existing evidence; choose a fresh output directory.')
    output.mkdir(parents=True)
    manifest = json.loads((bundle / 'grader/manifest.json').read_text())
    commands = []

    def run(argv, *, expected=0, timeout=180):
        started = time.monotonic()
        proc = subprocess.run(argv, capture_output=True, text=True, timeout=timeout, check=False)
        n = len(commands) + 1
        (output / f'{n:02d}.stdout.txt').write_text(proc.stdout, encoding='utf-8')
        (output / f'{n:02d}.stderr.txt').write_text(proc.stderr, encoding='utf-8')
        commands.append({'argv': argv, 'exit_code': proc.returncode, 'elapsed_seconds': time.monotonic()-started})
        (output / 'commands.json').write_text(json.dumps(commands, indent=2)+'\n')
        if proc.returncode != expected:
            raise RuntimeError(f'Command {n} returned {proc.returncode}, expected {expected}; inspect recorded stdout/stderr.')
        return proc.stdout

    version = json.loads(run(['docker', 'version', '--format', '{{json .Server}}']))
    suffix = hashlib.sha256((bundle / 'grader/manifest.json').read_bytes()).hexdigest()[:12]
    student_image, grader_image = 'qcb-student-smoke:' + suffix, 'qcb-grader-smoke:' + suffix
    run(['docker', 'build', '-t', student_image, str(bundle / 'environment')], timeout=300)
    run(['docker', 'build', '-t', grader_image, str(bundle / 'grader')], timeout=300)
    image_ids = [json.loads(run(['docker', 'image', 'inspect', image]))[0]['Id'] for image in (student_image, grader_image)]
    artifacts = bundle / 'run/output'
    artifacts.mkdir(parents=True, exist_ok=True)
    limits = ['--rm', '--network', 'none', '--read-only', '--cap-drop', 'ALL',
              '--security-opt', 'no-new-privileges:true', '--cpus', '1', '--memory', '1g', '--pids-limit', '128',
              '--user', f'{os.getuid()}:{os.getgid()}']
    # The student receives only its build context and a writable output directory.
    fixed_student = (
        'from pathlib import Path;import json,shutil;'
        'assert not Path("/grader").exists() and not Path("/solution").exists();'
        'rows=[json.loads(s) for s in Path("/workspace/tasks.jsonl").read_text().splitlines()];'
        'assert rows and all(set(r)=={"schema_version","task_id","task_hash","input"} for r in rows);'
        'assert all(r["schema_version"]=="qcb.student_task.v1" for r in rows);'
        'assert all("reference" not in r and "gold" not in r for r in rows);'
        'shutil.copyfile("/workspace/responses.template.jsonl","/output/student.jsonl");print("STUDENT_WORKSPACE_OK")')
    student = run(['docker', 'run', *limits, '--mount', f'type=bind,src={artifacts},dst=/output',
                   student_image, 'python', '-c', fixed_student])
    if 'STUDENT_WORKSPACE_OK' not in student:
        raise RuntimeError('Student fixture did not establish its workspace checks.')
    # The oracle is a maintainer fixture outside the student image/mount.
    oracle = run([sys.executable, str(bundle / 'solution/oracle.py')])
    (artifacts / 'oracle.jsonl').write_text(oracle, encoding='utf-8')
    rows = [json.loads(s) for s in oracle.splitlines() if s.strip()]
    wrong = json.loads(json.dumps(rows))
    for row in wrong:
        row['answer']['decision'] = {'holds': 'refuted', 'refuted': 'holds'}[row['answer']['decision']]
    (artifacts / 'wrong.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in wrong), encoding='utf-8')
    tampered = json.loads(json.dumps(rows))
    tampered[0]['task_hash'] = '0' * 64
    (artifacts / 'tampered.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in tampered), encoding='utf-8')

    def grade(name, expected=0):
        return run(['docker', 'run', *limits, '--mount', f'type=bind,src={artifacts},dst=/artifacts,readonly',
                    grader_image, '/artifacts/' + name], expected=expected)

    oracle_score = json.loads(grade('oracle.jsonl'))
    wrong_score = json.loads(grade('wrong.jsonl'))
    empty_score = json.loads(grade('student.jsonl'))
    grade('tampered.jsonl', expected=1)
    if (oracle_score['decision_accuracy_over_planned'] != 1 or wrong_score['decision_accuracy_over_planned'] != 0
            or wrong_score['pair_joint_accuracy_over_selected_pairs'] != 0
            or empty_score['decision_accuracy_over_planned'] != 0
            or any(s['aggregate_semantic_score'] is not None or s['formal_proof_score'] is not None
                   for s in (oracle_score, wrong_score, empty_score))):
        raise RuntimeError('The oracle/negative controls or independent score dimensions failed.')
    summary = {'schema_version': 'qcb.portable_environment_smoke.v1', 'execution_status': 'passed', 'passed': True,
               'registry_hash': manifest['registry_hash'], 'source_commit': manifest['source_commit'],
               'docker_server_version': version['Version'], 'student_image_id': image_ids[0], 'grader_image_id': image_ids[1],
               'resource_profile': {'network': 'none', 'read_only': True, 'cap_drop': ['ALL'],
                                    'no_new_privileges': True, 'cpus': 1, 'memory_bytes': 1073741824, 'pids_limit': 128},
               'student_workspace_verified': True, 'oracle_decision_accuracy': 1,
               'wrong_decision_accuracy': 0, 'not_run_decision_accuracy': 0, 'tampered_task_rejected': True,
               'semantic_score': None, 'formal_score': None, 'fixture_kind': 'reviewed_authored_reference_and_negative_controls',
               'model_calls': 0, 'lean_calls': 0, 'model_performance_measured': False}
    (output / 'public-summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
