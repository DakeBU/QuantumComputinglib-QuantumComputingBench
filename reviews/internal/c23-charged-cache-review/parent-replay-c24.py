"""Replay a frozen bounded internal review; never mutate prior evidence."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--root', type=Path, required=True)
parser.add_argument('--output', required=True)
args = parser.parse_args()
root = args.root.resolve()
here = root / 'reviews/internal/c23-charged-cache-review'
manifest_path = here / 'final-binding-manifest.json'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(manifest_path) == 'a6c300395e5b50e0b9e9a3e3feb1d8d804caea942473596d02b3c5d788ea1525'
manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
pins = {manifest_path: sha(manifest_path)}
for key in ('artifact_hashes', 'private_failure_and_raw_evidence_hashes'):
    pins.update({here / name: expected for name, expected in manifest[key].items()})
pins.update({root / name: expected for name, expected in manifest['stable_reviewed_sources'].items()})
state_path = here / '.cache/source-replay-v1/private-state.json'
state = json.loads(state_path.read_text(encoding='utf-8'))
pins[state_path] = sha(state_path)
pins.update({Path(name): expected for name, expected in state['pins'].items()})
def verify():
    for path, expected in pins.items():
        assert path.is_file() and sha(path) == expected, 'Frozen input drift'
verify()
for name in manifest['artifact_hashes']:
    data = (here / name).read_text(encoding='utf-8')
    assert not re.search(r'(?i)\b[A-Z]:[\\/]|file:[/]{2}|github_pat_[A-Za-z0-9_]+|ghp_[A-Za-z0-9]+', data), 'Public privacy failure'
source = here / 'IndependentConsumer.lean'
env = os.environ.copy()
env['LEAN_PATH'] = state['env_path']
binary = state['binary']
version = subprocess.run([binary, '--version'], cwd=root, env=env, capture_output=True, text=True, encoding='utf-8', check=True)
assert 'version 4.33.0' in version.stdout
deps = subprocess.run([binary, '--deps', source.relative_to(root).as_posix()], cwd=root, env=env, capture_output=True, text=True, encoding='utf-8', check=True)
selected = [Path(line.strip()).resolve() for line in deps.stdout.splitlines() if line.strip().endswith('.olean')]
private = here / '.cache/source-replay-v1'
for module in ('ChargedSourceCache', 'QuantumBlockEncoding/StoredHermiteCoefficients'):
    expected = (private / (module + '.olean')).resolve()
    assert expected in selected and sha(expected) == pins[expected]
proc = subprocess.run([binary, source.relative_to(root).as_posix()], cwd=root, env=env, capture_output=True, text=True, encoding='utf-8', timeout=180)
raw = proc.stdout + proc.stderr
reports = re.findall(r'depends on axioms: \[([^\]]*)\]', raw)
assert proc.returncode == 0, 'Consumer failed; no acceptance emitted'
assert len(reports) == 22
assert all(set(re.findall(r'[A-Za-z_][\w.]*', item)) <= {'propext', 'Classical.choice', 'Quot.sound'} for item in reports)
verify()
output = root / args.output
assert output.resolve().is_relative_to(here.resolve()) and not output.exists()
record = {
    'status': 'PARENT_FROZEN_REVIEW_AND_CONSUMER_REPLAY_PASS',
    'review_manifest_sha256': sha(manifest_path),
    'review_verdict': manifest['verdict'],
    'source': source.relative_to(root).as_posix(),
    'source_sha256': sha(source),
    'lean_version': version.stdout.strip(),
    'command': 'lean reviews/internal/c23-charged-cache-review/IndependentConsumer.lean (explicit frozen provider path; no output cache)',
    'exit_code': proc.returncode,
    'ordinary_axiom_reports': len(reports),
    'bound_inputs_stable_pre_post': len(pins),
    'direct_selected_providers_match_frozen_review': True,
    'public_artifact_count': len(manifest['artifact_hashes']),
    'public_privacy_scan': 'pass',
    'boundary': 'Fresh consumer elaboration only. Frozen reviewed providers and transitive caches inherited and pinned; not clean transitive rebuild, publication/source-blind admission, finite-bit runtime, main migration or scientific ROOT.',
}
output.write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8', newline='\n')
print(json.dumps(record, indent=2))
