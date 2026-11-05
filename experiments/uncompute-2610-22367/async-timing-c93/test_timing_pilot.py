import copy
import unittest
from unittest.mock import patch

import timing_pilot as pilot


class FakeProcess:
    def __init__(self, clock, end, code=0):
        self.clock, self.end, self.code = clock, end, code
        self.killed = False
        self.drained = False

    def poll(self):
        return self.code if self.killed or self.clock[0] >= self.end else None

    def kill(self):
        self.killed = True

    def communicate(self, timeout):
        if self.poll() is None:
            raise AssertionError("communicate on running child")
        self.drained = True
        return b"{}", b""


class MeasurementTests(unittest.TestCase):
    def setUp(self):
        self.expected = pilot.binding()
        self.payload = {"binding": copy.deepcopy(self.expected), "index": 1,
                        "work_start_ns": 10, "work_finish_ns": 20, "cpu_ns": 1}

    def test_valid_measurement_has_no_acceptance(self):
        result = pilot.validate_child(self.payload, self.expected, 1)
        self.assertNotIn("accepted", result)
        self.assertFalse(pilot.PLAN["mathematical_acceptance"])

    def test_forged_success_rejected(self):
        for field in ("success", "accepted", "root_closed"):
            with self.subTest(field=field), self.assertRaises(ValueError):
                pilot.validate_child(dict(self.payload, **{field: True}), self.expected, 1)

    def test_stale_or_mismatched_binding(self):
        for field in self.expected:
            bad = copy.deepcopy(self.payload)
            bad["binding"][field] = "stale"
            with self.subTest(field=field), self.assertRaises(ValueError):
                pilot.validate_child(bad, self.expected, 1)

    def test_wrong_child(self):
        with self.assertRaises(ValueError):
            pilot.validate_child(self.payload, self.expected, 0)

    def test_boolean_revision_is_not_an_integer_revision(self):
        self.payload["binding"]["candidate_revision"] = True
        with self.assertRaises(ValueError):
            pilot.validate_child(self.payload, self.expected, 1)

    def test_bad_numeric_types_and_reversal(self):
        for field in ("work_start_ns", "work_finish_ns", "cpu_ns"):
            for value in (-1, 0.5, True, None):
                with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                    pilot.validate_child(dict(self.payload, **{field: value}), self.expected, 1)
        with self.assertRaises(ValueError):
            pilot.validate_child(dict(self.payload, work_start_ns=21), self.expected, 1)

    def test_missing_field(self):
        del self.payload["cpu_ns"]
        with self.assertRaises(ValueError):
            pilot.validate_child(self.payload, self.expected, 1)


class CollectionTests(unittest.TestCase):
    def run_fake(self, mode, ends=(3, 1), codes=(0, 0), deadline=10, interrupt=False):
        now = [0]
        processes = [FakeProcess(now, end, code) for end, code in zip(ends, codes)]
        def sleep(_):
            now[0] += 1
            if interrupt:
                raise KeyboardInterrupt()
        self.processes = processes
        with patch.object(pilot.time, "monotonic_ns", side_effect=lambda: now[0] * 100):
            return pilot.collect(processes, mode, deadline, clock=lambda: now[0], sleep=sleep)

    def test_launch_order_reproduces_observation_lag(self):
        rows = self.run_fake("launch-order")
        self.assertEqual([row[0] for row in rows], [0, 1])
        self.assertEqual(rows[1][2], 300)

    def test_ready_first_observes_fast_child_early(self):
        rows = self.run_fake("ready-first")
        self.assertEqual([row[0] for row in rows], [1, 0])
        self.assertEqual(rows[0][2], 100)

    def test_simultaneous_completions_not_duplicated(self):
        rows = self.run_fake("ready-first", ends=(1, 1))
        self.assertEqual([row[0] for row in rows], [0, 1])
        self.assertEqual(rows[0][2], rows[1][2])

    def test_failure_code_preserved_and_all_collected(self):
        rows = self.run_fake("ready-first", codes=(0, 7))
        self.assertEqual(rows[0][1], 7)
        self.assertTrue(all(p.drained for p in self.processes))

    def test_timeout_cleans_only_owned_children(self):
        with self.assertRaises(TimeoutError):
            self.run_fake("ready-first", ends=(20, 30), deadline=2)
        self.assertTrue(all(p.killed and p.drained for p in self.processes))

    def test_interruption_cleans_owned_children(self):
        with self.assertRaises(KeyboardInterrupt):
            self.run_fake("ready-first", interrupt=True)
        self.assertTrue(all(p.drained and p.poll() is not None for p in self.processes))
        self.assertTrue(self.processes[0].killed)
        self.assertFalse(self.processes[1].killed)  # Already exited: drain, don't kill.

    def test_unknown_mode_rejected(self):
        with self.assertRaises(ValueError):
            self.run_fake("arbitrary")


if __name__ == "__main__":
    unittest.main()
