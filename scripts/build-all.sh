#!/usr/bin/env bash

set -euo pipefail

if [[ "${QBE_AGENT_INNER_CYCLE:-0}" == "1" ]]; then
  echo "build-all is disabled inside an ASPBE agent cycle; use the controller gate" >&2
  exit 64
fi

python3 -m unittest tools.test_hermite_artifacts tools.test_technical_lemma_registry tools.test_verso_windows_compat tools.test_powershell_builds website.scripts.test_proof_inputs website.scripts.test_hermite_case website.scripts.test_lean_publication_gate
python3 tools/check_hermite_artifacts.py
python3 tools/qbe.py harness-check
python3 tools/check_process_memory.py check
python3 tools/check_public_figure_style.py
python3 tools/test_proof_trust.py
python3 tools/check_proof_trust.py
python3 tools/check_technical_lemma_registry.py
python3 -m unittest website.scripts.test_site_contracts tools.test_case_memory tools.test_robin_export tools.test_replay_public_cases
python3 website/scripts/run_lean_gate.py
python3 executable-exports/SP-HERMITE-001/qiskit/export.py --self-test
python3 executable-exports/SP-HERMITE-001/qiskit/replay.py
python3 tools/replay_public_cases.py
python3 tools/export_robin_evolution.py --task QBE-ROBIN-BE-WARM-001 --arm warm
python3 -m unittest tools.test_blueprint_catalog
python3 scripts/generate-aspbe-catalog.py
python3 scripts/generate-aspbe-catalog.py --check
python3 scripts/test-sanitize-blueprint-paths.py
bash scripts/build-blueprint.sh
bash scripts/build-website.sh
