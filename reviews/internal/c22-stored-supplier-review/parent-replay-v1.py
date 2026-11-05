"""Re-elaborate the independent consumer without modifying frozen evidence."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

here = Path(__file__).resolve().parent
root = here.parents[2]
manifest_path = here / "final-bindings.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
pins = {**manifest["source_bindings"], **manifest["review_owned_artifacts"]}
pins[manifest_path.relative_to(root).as_posix()] = hashlib.sha256(manifest_path.read_bytes()).hexdigest()


def verify():
    for name, expected in pins.items():
        path = root / name
        assert path.is_file(), "Missing bound review input"
        assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, "Changed review input: " + name


verify()
env = os.environ.copy()
env["LEAN_PATH"] = os.pathsep.join(str(root / "experiments/hermite-polynomial/precision" / name / ".cache")
                                 for name in ("piecewise-kernel-stored-c22", "piecewise-kernel-assembly-c21",
                                              "piecewise-kernel-producer", "piecewise-kernel-uniform-c20"))
source = here / "IndependentConsumer.lean"
run = subprocess.run(["lake", "env", "lean", source.relative_to(root).as_posix()],
                     cwd=root, env=env, capture_output=True, text=True, encoding="utf-8")
output = (run.stdout + run.stderr).replace(str(root), ".").replace(root.as_posix(), ".")
log = here / "parent-replay-v1.log"
assert not log.exists(), "Never overwrite an existing replay"
log.write_text(output, encoding="utf-8", newline="\n")
reports = re.findall(r"depends on axioms: \[([^\]]*)\]", output)
ordinary = all(set(re.findall(r"[A-Za-z_][\w.]*", r)) <=
               {"propext", "Classical.choice", "Quot.sound"} for r in reports)
verify()
receipt = {"exit": run.returncode, "named_symbolic_axiom_reports": len(reports),
           "ordinary_axioms_only": ordinary, "pins_checked_pre_post": len(pins),
           "source_sha256": pins[source.relative_to(root).as_posix()],
           "frozen_review_manifest_sha256": pins[manifest_path.relative_to(root).as_posix()],
           "log_sha256": hashlib.sha256(log.read_bytes()).hexdigest(),
           "scope": "Independent internal consumer, including supporting native_decide finite screenings; inherited bound imports, not clean transitive rebuild",
           "scientific_ROOT": False, "full_runtime_certified": False, "public_sourceblind_admission": False}
target = here / "parent-replay-v1.json"
assert not target.exists()
target.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8", newline="\n")
print(json.dumps(receipt, indent=2))
assert run.returncode == 0 and ordinary and len(reports) == 7
