"""Publish distinct train-reference and question-only Lean course artifacts."""
import hashlib
import json
import subprocess
from pathlib import Path


def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + '\n').encode('utf-8')


def payloads():
    # The caller's publisher has initialized benchmark imports. These loaders
    # validate recorded evidence without executing Lean or a model.
    from qcb_course_registry import load_course_registry
    from qcb_course_training import export_training, reference_records
    from qcb_evaluation_registry import export_views
    views, qualification = load_course_registry()
    artifacts = {'train-references.json': export_training(views, qualification, reference_records())}
    for split in ('train', 'dev', 'test_public'):
        artifacts[split + '-inputs.json'] = export_views(views, qualification, split=split)
    return qualification, artifacts


def expected_downloads():
    qualification, artifacts = payloads()
    root = Path(__file__).resolve().parents[2]
    sources = ('website/scripts/qcb_lean_downloads.py',
               'benchmarks/quantumcomputingbench/src/qcb_course_registry.py',
               'benchmarks/quantumcomputingbench/src/qcb_course_training.py',
               'benchmarks/quantumcomputingbench/scripts/lean_training.py',
               'benchmarks/quantumcomputingbench/scripts/evaluate_agentic.py')
    manifest = {'schema_version': 'qcb.lean_course_downloads.v1',
                'source_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip(),
                'producer_sources_sha256_lf': {p: hashlib.sha256((root / p).read_bytes().replace(b'\r\n', b'\n')).hexdigest()
                                               for p in sources},
                'suite_id': qualification['suite_id'], 'registry_digest': qualification['registry_digest'],
                'reference_exposure': 'public_authored_references; not_a_blind_test',
                'model_performance_measured': False, 'training_launched': False,
                'candidate_execution': 'ENV_BLOCKED; accepted isolation required',
                'artifacts': {name: {'sha256': hashlib.sha256(encoded(value)).hexdigest(),
                                     'bytes': len(encoded(value)),
                                     'contains_references': name == 'train-references.json'}
                              for name, value in artifacts.items()}}
    return {**artifacts, 'manifest.json': manifest}


def write_downloads(folder):
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    records = expected_downloads()
    for name, value in records.items():
        (folder / name).write_bytes(encoded(value))
    return records['manifest.json']


def check_downloads(folder, summary):
    folder = Path(folder)
    records = expected_downloads()
    if summary != records['manifest.json'] or {p.name for p in folder.iterdir()} != set(records):
        raise ValueError('Lean course downloads have stale identities or unexpected files')
    for name, value in records.items():
        if (folder / name).read_bytes() != encoded(value):
            raise ValueError('Lean course download differs from its exact qualified projection: ' + name)
