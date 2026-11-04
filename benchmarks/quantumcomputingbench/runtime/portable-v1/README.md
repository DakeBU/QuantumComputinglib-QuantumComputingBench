# Portable question and response workspace

This QCB bundle separates agent inputs, response artifacts, reference control
and grading. It is a CPU question workspace, with Python stdlib and no model
client or Lean compiler. It uses its own portable format; Harbor TaskConfig
compatibility is not claimed.

On Linux with Docker, `bash run-student.sh` prints the instructions. Pass a
trusted installed agent executable and its arguments after the script name;
install that agent in a separately reviewed image first. The base image is
pinned by its official registry manifest digest; also record the built image ID.
The source-generated `task.json` records that image execution has not yet run;
CI/operator execution evidence is separate.

Without Docker, inspect `environment/workspace/` and produce
`run/output/responses.jsonl` with an external model or a human. Keep `grader/`
and `solution/` unavailable to the student. The Docker build context is
`environment/`, not the entire bundle or repository.

Trusted reference control:

```sh
python solution/oracle.py > run/output/oracle.jsonl
python grader/grade.py run/output/oracle.jsonl
python grader/grade.py run/output/responses.template.jsonl
```

Independent container grader:

```sh
docker build -t qcb-response-grader ./grader
docker run --rm --network none --read-only --cap-drop ALL \
  --security-opt no-new-privileges --cpus 1 --memory 1g --pids-limit 128 \
  --mount "type=bind,src=$PWD/run/output,dst=/artifacts,readonly" \
  qcb-response-grader /artifacts/oracle.jsonl
```

The oracle score and try-none control test the decision protocol. Ordinary NL
answers and explanations require actual rubric review, even when the response
copies a reference answer. Use the repository's `bench.py review-template` to
prepare bound reviewer records. Model-generated Lean execution uses the
separate registered prover harness and its accepted isolation gate.
