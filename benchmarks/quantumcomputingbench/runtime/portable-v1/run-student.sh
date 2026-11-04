#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
docker build -t qcb-question-workspace ./environment
mkdir -p run/output
docker run --rm --network none --read-only --cap-drop ALL --security-opt no-new-privileges \
  --cpus 1 --memory 1g --pids-limit 128 --tmpfs /tmp:rw,noexec,nosuid,size=64m \
  --user "$(id -u):$(id -g)" --mount "type=bind,src=$PWD/run/output,dst=/output" \
  qcb-question-workspace "$@"
