# QuantumComputingBench question workspace

Read `/workspace/tasks.jsonl`. Preserve every mathematical assumption and
convention. Write one JSON object per line to `/output/responses.jsonl`, using
`/workspace/responses.template.jsonl` as the record schema. Preserve the exact
`task_id`, `task_hash` and `run_id`.

For an answered semantic question, set `status` to `answered` and `answer` to
an object with `decision` (`holds` or `refuted`) and `explanation` (your argument
or precise counterexample). For an ordinary mathematical question, `answer`
contains only `explanation`. For abstention, set `status=abstained` and
`answer=null`. Use `env_blocked`, `not_run` or `budget_exhausted` only when
that outcome actually occurred.

Outputs are graded independently. Mathematical explanation quality requires
the bound rubric review; matching a reference string is not the grading rule.
