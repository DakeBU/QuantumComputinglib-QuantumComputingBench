# Same-cap fresh-target serial-elaboration diagnostic

The previous actual CI3 parser succeeded (220 headers, 37 project modules), but
fresh RealAmplitudePreparation aborted with a Lean internal memory exception.
Only fresh target commands now add `-DElab.async=false`: memory3072MiB,
threads1, target600s and whole2100s are unchanged. The exact 57-root profile,
220 source candidates, imports, parser, collector and validator are unchanged.
This tests a scheduling hypothesis; it does not establish memory savings.
No inherited target artifact, missing node, weaker trust rule, retry or budget
increase is permitted. Diagnostics remain non-admission evidence.

The original sealed CI3 packet and actual failure remain intact. The parent
launcher is the exact CI3 launcher with only new archive/seal/member-count,
output-directory and receipt-schema identities. The shared diagnostic logger
remains pinned. Roll back by selecting the retained CI3 launcher in the optional
workflow, keeping both historical artifacts. No production source is changed.
