"""Actual Lean replay of inspected, hash-allowlisted protocol fixtures only.

This is deliberately not a candidate executor. The proving model cannot provide
the allowlist, task, imports, runtime, source template, or execution policy.
"""
from __future__ import annotations

import asyncio
import hashlib
import os
import secrets
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
from copy import deepcopy
from pathlib import Path

from qcb_core import digest, read_json
from qcb_lean import evaluate_report
from qcb_proof_session import bound_reply, proof_sha, validate_task

R = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(R / "website/scripts"))
from proof_inputs import lean_module_targets, proof_input_digest


def _git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], text=True, timeout=10).strip()


def _stop(process):
    if os.name == "nt":
        if process.poll() is None:
            subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5, check=False)
    else:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass


def _run_reference(command, cwd, timeout, cap=65536):
    process = subprocess.Popen(command, cwd=cwd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, start_new_session=os.name != "nt")
    output = bytearray()
    overflow = threading.Event()

    def read():
        while True:
            try:
                chunk = os.read(process.stdout.fileno(), 4096)
            except OSError:
                break
            if not chunk:
                break
            available = max(0, cap - len(output))
            output.extend(chunk[:available])
            if len(chunk) > available:
                overflow.set()
                _stop(process)
                break

    reader = threading.Thread(target=read, daemon=True)
    reader.start()
    failure = None
    try:
        process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        failure = "timeout"
        _stop(process)
        process.wait(timeout=5)
    finally:
        reader.join(timeout=3)
        if reader.is_alive():
            failure = "incomplete_output_cleanup"
            _stop(process)
        process.stdout.close()
    if overflow.is_set():
        failure = "output_cap"
    return process.returncode, output.decode("utf-8", errors="replace"), failure


class AuthoredReferenceVerifier:
    execution_class = "trusted_local_authored_reference"
    isolated = False

    def __init__(self, task, allowed_proofs, build_root, *, source_root=R):
        self.task = validate_task(task)
        self.task_hash = digest(self.task)
        self.build_root, self.source_root = Path(build_root).resolve(), Path(source_root).resolve()
        self.input_digest = proof_input_digest(self.source_root)
        if proof_input_digest(self.build_root) != self.input_digest:
            raise ValueError("authored replay requires identical production proof inputs")
        if _git(self.build_root, "status", "--porcelain", "--untracked-files=no"):
            raise ValueError("authored reference checkout must have no tracked changes")
        self.revision = _git(self.build_root, "rev-parse", "HEAD")
        if self.revision != self.task["library_revision"]:
            raise ValueError("task pin differs from actual reference runtime checkout")
        self.lake = shutil.which("lake")
        if not self.lake:
            raise ValueError("authored replay needs an already installed lake executable")
        self.lean_version = subprocess.check_output(
            [self.lake, "env", "lean", "--version"], cwd=self.build_root, text=True, timeout=15).strip()
        expected = (self.build_root / "lean-toolchain").read_text().strip().split(":v")[-1]
        if "version " + expected + "," not in self.lean_version:
            raise ValueError("actual compiler version differs from pinned toolchain")
        gate = read_json(self.build_root / "_out/lean-gate.json")
        if (gate.get("passed") is not True or gate.get("proofInputsSha256") != self.input_digest
                or gate.get("compiledModules") != lean_module_targets(self.source_root)):
            raise ValueError("matching complete repository Lean gate required")
        self.nodes = {n["id"]: n for n in self.task["nodes"]}
        if set(allowed_proofs) != set(self.nodes):
            raise ValueError("each authored obligation needs an explicit proof-hash allowlist")
        self.allowlist = {}
        for key, proofs in allowed_proofs.items():
            if not isinstance(proofs, list) or not proofs or any(not isinstance(p, str) or len(p) > 16000 for p in proofs):
                raise ValueError("invalid authored fixture proof allowlist")
            self.allowlist[key] = frozenset(proof_sha(p) for p in proofs)
        self.pipeline_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        self.replays = []

    def _source(self, request, nonce):
        imports = "\n".join("import " + module for module in self.task["imports"])
        universes = self.task.get("universe_parameters", [])
        universe_line = "universe " + " ".join(universes) + "\n" if universes else ""
        nodes = []
        for key in request["dependency_order"]:
            node = request["dependencies"][key]
            if (key not in self.nodes or node["target"] != self.nodes[key]["target"]
                    or proof_sha(node["proof"]) not in self.allowlist[key]):
                raise ValueError("dependency proof is not an inspected authored fixture")
            nodes.append(f"set_option maxHeartbeats 400000 in\ntheorem qcb_step_{key} : {node['target']} :=\n{node['proof']}\n")
        name = "qcbAuthored_" + nonce
        nodes.append(f"set_option maxHeartbeats 400000 in\ntheorem {name} : {request['target']} :=\n{request['proof']}\n")
        declarations = "\n".join(nodes)
        return f'''import Lean
{imports}
{universe_line}open scoped BigOperators
{declarations}
open Lean Elab Command in
elab "qcbAuthoredReport" : command => do
  let axioms ← liftCoreM (Lean.collectAxioms `{name})
  let names := axioms.toList.map Lean.Name.toString
  let sorrySeen := names.any (fun n => n == "sorryAx")
  let flag := if sorrySeen then "true" else "false"
  logInfo s!"QCB_AXIOM_REPORT|{nonce}|{{flag}}|{{String.intercalate "," names}}"
qcbAuthoredReport
'''

    def _verify(self, request):
        key, proof = request.get("node_id"), request.get("proof")
        if (request.get("task_hash") != self.task_hash or key not in self.nodes
                or request.get("target") != self.nodes[key]["target"]
                or request.get("imports") != self.task["imports"]
                or request.get("universe_parameters") != self.task.get("universe_parameters", [])
                or request.get("library_revision") != self.revision):
            raise ValueError("authored replay request differs from fixed task")
        if not isinstance(proof, str) or proof_sha(proof) not in self.allowlist[key]:
            return bound_reply(request, status="api_error", execution_id=secrets.token_hex(16),
                               diagnostics="Proof is not on the inspected authored-fixture allowlist; not executed.")
        if (proof_input_digest(self.build_root) != self.input_digest
                or proof_input_digest(self.source_root) != self.input_digest
                or _git(self.build_root, "rev-parse", "HEAD") != self.revision
                or hashlib.sha256(Path(__file__).read_bytes()).hexdigest() != self.pipeline_hash):
            raise ValueError("reference inputs or pipeline changed during the session")
        nonce = secrets.token_hex(16)
        source = self._source(request, nonce)
        started = time.monotonic()
        remaining = request["deadline_monotonic"] - time.monotonic()
        if remaining <= 0:
            return bound_reply(request, status="timeout", execution_id=nonce, diagnostics="Authored replay deadline expired.")
        with tempfile.TemporaryDirectory(prefix="qcb-authored-session-") as directory:
            path = Path(directory) / "Authored.lean"
            path.write_text(source, encoding="utf-8", newline="\n")
            code, diagnostic, failure = _run_reference(
                [self.lake, "env", "lean", str(path)], self.build_root, remaining)
        if code < 0 or code in {125, 126, 127, 137, 143}:
            failure = failure or "runtime_exit"
        if (proof_input_digest(self.build_root) != self.input_digest
                or proof_input_digest(self.source_root) != self.input_digest
                or _git(self.build_root, "rev-parse", "HEAD") != self.revision
                or hashlib.sha256(Path(__file__).read_bytes()).hexdigest() != self.pipeline_hash):
            failure = "proof_input_drift"
        if failure:
            status = "timeout" if failure == "timeout" else "verifier_error"
            outcome = {"status": status, "reason": failure}
        else:
            outcome = evaluate_report(code, diagnostic, "", nonce)
            status = {"certified": "verified", "rejected": "compile_error", "blocked": "verifier_error"}[outcome["status"]]
        reply = bound_reply(request, status=status, execution_id=nonce, kernel_checked=status == "verified",
                            axioms=outcome.get("axioms", []), diagnostics=diagnostic[-4000:])
        self.replays.append({"node_id": key, "request_hash": digest(request), "execution_id": nonce,
                             "final_replay": request["final_replay"], "proof_sha256": proof_sha(proof),
                             "source_sha256": hashlib.sha256(source.encode()).hexdigest(),
                             "runtime_checkout_commit": self.revision, "proof_inputs_sha256": self.input_digest,
                             "actual_lean_version": self.lean_version,
                             "pipeline_sha256": self.pipeline_hash, "exit_code": code,
                             "status": status, "axioms": outcome.get("axioms", []), "failure": failure,
                             "elapsed_seconds": time.monotonic() - started,
                             "execution_class": self.execution_class, "isolated": False})
        return reply

    async def verify(self, request):
        # The native subprocess also enforces the caller's deadline and cleans
        # its own process tree; coroutine cancellation is not a sandbox.
        worker = asyncio.create_task(asyncio.to_thread(self._verify, deepcopy(request)))
        try:
            return await asyncio.shield(worker)
        except asyncio.CancelledError:
            # wait_for cancellation must not release the session lock while a
            # native worker is still executing or cleaning up its process tree.
            try:
                await asyncio.shield(worker)
            finally:
                raise
