"""Trusted authored reference control; this is not a model baseline."""
import json
from pathlib import Path

root = Path(__file__).resolve().parent.parent
registry = json.loads((root / "grader/registry.json").read_text(encoding="utf-8"))
manifest = json.loads((root / "grader/manifest.json").read_text(encoding="utf-8"))
chosen = {t["task_id"] for t in manifest["tasks"]}
for task in registry["tasks"]:
    if task["task_id"] not in chosen:
        continue
    answer = {"explanation": task["reference"]["answer"]}
    if task["track"] == "semantic":
        answer["decision"] = task["reference"]["decision"]
    print(json.dumps({"schema_version": "qcb.response.v1", "run_id": manifest["run_id"],
                      "task_id": task["task_id"], "task_hash": task["task_hash"],
                      "status": "answered", "answer": answer}, ensure_ascii=True))
