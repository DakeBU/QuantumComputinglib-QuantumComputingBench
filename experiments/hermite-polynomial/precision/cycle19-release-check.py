"""Select frozen checkpoint files, not active workers/user dirt or private receipts."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[3]
PREFIX = 'experiments/hermite-polynomial/precision/'
PACKETS = [PREFIX + 'literal-complex-review-c18', PREFIX + 'piecewise-kernel-producer']
DECODER = 'reviews/publication/stored-tensor-train/'
DECODER_FILES = ['decoder-artifact.json', 'decoder-evidence.json',
                 'decoder-c19-v3-public-receipt.json', 'decoder-privacy-c19-v3-public.json',
                 'decoder-probe-c19-v1.lean', 'decoder-probe-c19-v2.lean',
                 'decoder-probe-c19-v3.lean', 'decoder-runner-c19-v3.py',
                 'decoder-public-receipt-c19.py']
PATH = re.compile(r'(?<![A-Za-z0-9_])[A-Za-z]:[\\/]')
SECRET = re.compile(r'github_pat_[A-Za-z0-9_]+|ghp_[A-Za-z0-9]+')


def main():
    result = subprocess.run(['git', 'ls-files', '--others', '--exclude-standard', '--'] + PACKETS,
                            cwd=ROOT, check=True, capture_output=True, text=True)
    files = result.stdout.splitlines()
    files += [DECODER + name for name in DECODER_FILES]
    files += [p.relative_to(ROOT).as_posix()
              for p in (ROOT / PREFIX).glob('cycle19-parent-checkpoint*') if p.is_file()]
    # Original file is ignored only because its standalone entry point records
    # private commands. unittest discovery is pure and the source has no paths.
    files += [PREFIX + 'literal-complex-review-c18/finite_checks.py']
    files += [PREFIX + 'cycle19-release-check.py']
    files += [PREFIX + 'cycle19-staging-result.json',
              'proof-obligations/SP-HERMITE-POLY-002.md',
              'candidate-populations/SP-HERMITE-POLY-002.md']
    issues = []

    def scan(value, filename, key):
        if isinstance(value, dict):
            for k, v in value.items():
                scan(k, filename, key + '.<key>')
                scan(v, filename, key + '.' + str(k))
        elif isinstance(value, list):
            for i, v in enumerate(value):
                scan(v, filename, key + '.' + str(i))
        elif isinstance(value, str):
            if PATH.search(value) or SECRET.search(value):
                issues.append({'file': filename, 'field': key})
            # Decode nested machine-readable Lean messages as well.
            if key.endswith('.stdout') or key.endswith('.stderr'):
                for line in value.splitlines():
                    try:
                        nested = json.loads(line)
                    except (ValueError, TypeError):
                        continue
                    scan(nested, filename, key + '.decoded')

    pins = {}
    for filename in sorted(set(files)):
        path = ROOT / filename
        if not path.is_file():
            raise SystemExit('Missing selected file: ' + filename)
        raw = path.read_bytes()
        pins[filename] = hashlib.sha256(raw).hexdigest()
        text = raw.decode('utf-8-sig')
        if path.suffix == '.json':
            scan(json.loads(text), filename, '$')
        else:
            scan(text, filename, '$text')
    print(json.dumps({'passed': not issues, 'selected_sha256': pins,
                      'issues': issues, 'raw_private_receipts_selected': False,
                      'active_c20_workers_selected': False}, indent=2))
    return 0 if not issues else 1


if __name__ == '__main__':
    raise SystemExit(main())
