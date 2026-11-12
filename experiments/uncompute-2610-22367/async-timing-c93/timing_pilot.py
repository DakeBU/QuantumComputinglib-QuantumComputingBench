"""Standalone synthetic telemetry pilot; never grants scientific acceptance."""
import hashlib
import json
import platform
from pathlib import Path
import subprocess
import sys
import time


PLAN = {
    "schema": "ASPBE_SYNTHETIC_TIMING_PLAN_V1",
    "task": "synthetic-observation-lag-only",
    "candidate_revision": 1,
    "durations_seconds": [0.7, 0.05],
    "arm_order": ["launch-order", "ready-first", "ready-first", "launch-order"],
    "arm_budget_seconds": 5,
    "poll_seconds": 0.005,
    "model_calls": 0,
    "mathematical_acceptance": False,
}


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def binding():
    return {"plan_sha256": digest(json.dumps(PLAN, sort_keys=True).encode()),
            "workflow_sha256": digest(Path(__file__).read_bytes()),
            "candidate_revision": PLAN["candidate_revision"]}


def validate_child(payload, expected, index):
    """Validate measurement shape, not a theorem, circuit, or trusted success."""
    if set(payload) != {"binding", "index", "work_start_ns", "work_finish_ns", "cpu_ns"}:
        raise ValueError("unexpected measurement fields")
    if (type(payload["binding"]) is not dict or payload["binding"] != expected
            or any(type(payload["binding"][key]) is not type(value) for key, value in expected.items())
            or type(payload["index"]) is not int or payload["index"] != index):
        raise ValueError("stale or mismatched measurement")
    for field in ("work_start_ns", "work_finish_ns", "cpu_ns"):
        if type(payload[field]) is not int or payload[field] < 0:
            raise ValueError("invalid timestamp or CPU measurement")
    if payload["work_finish_ns"] < payload["work_start_ns"]:
        raise ValueError("reversed work timestamps")
    return payload


def cleanup(processes):
    """Only processes created by this call, with no shells or grandchildren."""
    for process in processes:
        if process.poll() is None:
            process.kill()
        process.communicate(timeout=2)


def collect(processes, mode, deadline, clock=time.monotonic, sleep=time.sleep):
    """Observation order is independent of launch-order final reporting."""
    if mode not in ("launch-order", "ready-first"):
        raise ValueError("unknown collection arm")
    pending = list(range(len(processes)))
    observations = []
    try:
        while pending:
            if clock() >= deadline:
                raise TimeoutError("fixed arm budget exhausted")
            eligible = pending[:1] if mode == "launch-order" else pending[:]
            collected = False
            for index in eligible:
                process = processes[index]
                code = process.poll()
                if code is not None:
                    observed = time.monotonic_ns()
                    stdout, stderr = process.communicate(timeout=1)
                    observations.append((index, code, observed, stdout, stderr))
                    pending.remove(index)
                    collected = True
            if pending and not collected:
                sleep(PLAN["poll_seconds"])
        return observations
    finally:
        cleanup(processes)


def run_arm(mode):
    start, cpu_start = time.monotonic_ns(), time.process_time_ns()
    deadline = time.monotonic() + PLAN["arm_budget_seconds"]
    processes, launches = [], []
    try:
        for index in range(2):
            launches.append(time.monotonic_ns())
            processes.append(subprocess.Popen(
                [sys.executable, "-B", str(Path(__file__).resolve()), "--child", str(index)],
                stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0))
        raw = collect(processes, mode, deadline)
        rows = []
        seen = set()
        for index, code, observed, stdout, stderr in raw:
            if index in seen or code != 0 or stderr:
                raise ValueError("duplicate, failed or diagnostic-only child")
            seen.add(index)
            payload = validate_child(json.loads(stdout), binding(), index)
            if not launches[index] <= payload["work_start_ns"] <= payload["work_finish_ns"] <= observed:
                raise ValueError("cross-process timestamp ordering failed")
            rows.append({"index": index, "exit_code": code,
                "launch_offset_ns": launches[index] - start,
                "work_start_offset_ns": payload["work_start_ns"] - start,
                "work_finish_offset_ns": payload["work_finish_ns"] - start,
                "parent_observed_offset_ns": observed - start,
                "child_work_ns": payload["work_finish_ns"] - payload["work_start_ns"],
                "child_cpu_ns": payload["cpu_ns"],
                "finish_to_observation_ns": observed - payload["work_finish_ns"],
                "parent_elapsed_ns": observed - launches[index]})
        return {"mode": mode, "observation_order": [row["index"] for row in rows],
            "workers": sorted(rows, key=lambda row: row["index"]),
            "wall_ns": time.monotonic_ns() - start,
            "parent_cpu_ns": time.process_time_ns() - cpu_start,
            "child_work_sum_ns": sum(row["child_work_ns"] for row in rows),
            "child_cpu_sum_ns": sum(row["child_cpu_ns"] for row in rows)}
    finally:
        cleanup(processes)


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--child":
        index = int(sys.argv[2])
        expected = binding()
        start, cpu_start = time.monotonic_ns(), time.process_time_ns()
        time.sleep(PLAN["durations_seconds"][index])
        finish, cpu_finish = time.monotonic_ns(), time.process_time_ns()
        print(json.dumps({"binding": expected, "index": index, "work_start_ns": start,
                          "work_finish_ns": finish, "cpu_ns": cpu_finish - cpu_start}))
        return
    if len(sys.argv) != 1:
        raise SystemExit("Only the frozen plan or its two fixed children may run")
    arms = [run_arm(mode) for mode in PLAN["arm_order"]]
    result = {"schema": "ASPBE_SYNTHETIC_TIMING_OBSERVATION_V1", "plan": PLAN,
        "binding": binding(), "python_version": platform.python_version(),
        "platform": sys.platform, "clock": vars(time.get_clock_info("monotonic")),
        "arms": arms, "model_calls": 0, "Lean_calls": 0, "Qiskit_calls": 0,
        "tokens": None, "mathematical_acceptance": False,
        "production_scheduler_changed": False,
        "limitations": ["synthetic sleeps, not quantum tasks or model workers",
            "finish_to_observation includes child serialization, exit and parent polling",
            "child work excludes interpreter/import startup; parent elapsed includes it",
            "CPU deltas cover sampled intervals, not full process lifetime",
            "no exact OS exit timestamp, queue time, memory peak or provider token data",
            "two repetitions per arm; feasibility only, no general efficiency claim"]}
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
