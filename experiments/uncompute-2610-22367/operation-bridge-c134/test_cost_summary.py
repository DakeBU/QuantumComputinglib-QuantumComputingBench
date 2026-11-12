import importlib.util,json,unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('local_cost_summary',HERE/'cost_summary.py')
cost=importlib.util.module_from_spec(spec);spec.loader.exec_module(cost)

class CostSummary(unittest.TestCase):
    def test_recomputes_delivered_records(self):
        self.assertEqual(cost.summarize(),json.loads((HERE/'retrospective-cost-observation.json').read_bytes()))

    def test_failed_work_is_not_omitted(self):
        row=cost.summarize()
        self.assertEqual(row['recorded_observations'],7)
        self.assertEqual(row['count_recorded_failed_whole_proofs'],3)
        self.assertEqual(row['failed_whole_proof_wrapper_seconds'],191.985)
        self.assertEqual(row['sum_recorded_wrapper_seconds'],362.375)

    def test_unknown_is_not_zero_or_a_cap(self):
        row=cost.summarize()
        for field in ['model_tokens','total_model_calls','total_CPU_seconds','peak_memory_MiB','stale_or_cancelled_work_total','complete_workflow_wall_seconds']:
            self.assertIsNone(row[field])
        for event in row['observations']:
            self.assertEqual(event['memory_limit_MiB'],3072)
            self.assertIsNone(event['observed_peak_memory_MiB'])

    def test_no_strategy_or_acceptance_promotion(self):
        row=cost.summarize()
        for field in ['observation_sum_is_complete_cost','observation_sum_is_full_workflow_latency','matched_endpoint_ablation','independent_repeated_trials','randomized_arms','production_scheduler_or_scoring_changed']:
            self.assertFalse(row[field])
        self.assertIsNone(row['efficiency_winner'])

    def test_invalid_missing_duration_and_nonterminal_code_fail(self):
        for value in [None,True,-1,float('nan'),float('inf'),'1']:
            with self.assertRaises(ValueError):cost.duration(dict(seconds=value,exit_code=0))
        with self.assertRaises(KeyError):cost.duration(dict(exit_code=0))
        for code in [None,True,'0']:
            with self.assertRaises(ValueError):cost.duration(dict(seconds=1,exit_code=code))

if __name__=='__main__':unittest.main()
