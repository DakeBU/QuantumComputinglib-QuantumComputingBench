# Frozen runtime input transport follow-up

No working-tree verifier, Lake configuration, mathematical source, frozen
packet, scoring or historical log bytes were edited by this follow-up.

The final reviewer packet records actual raw inputs. Pre-commit inspection
found that Git still stored LF versions of two of those already reviewed
inputs, while the original run used CRLF/mixed bytes. The context explanation
was LF but would also be changed by an autocrlf checkout. Leaving this alone
would make actual-layout checks fail on another machine, not justify rehashing
or weakening those checks.

Three scoped `-text` rules now preserve the original runtime/configuration
and migration explanation bytes. Explicit `git add --renormalize --` on
only these paths was necessary: ordinary `git add` reused unchanged stat
entries and initially left the old index blobs. The exact staged hashes now
equal the immutable final input packet:

| Path | Original and staged SHA256 |
| --- | --- |
| lakefile.lean | f6637c3a2467fdeee6b2de72505d0581c4a49793388197bd8e9e7df3f5817fc1 |
| website/scripts/check_research_publications.py | f8f6d7232376b5bc19a480b7e0ef549a5fafa8d66017e07482f7e6999962f8ad |
| reports/lean-433-migration/c25-cf77-context.md | 247786522c905fc8dca0ea22f2b7224cd988354bfd9b697aff3b3e63bcfc9b33 |

The first two Git blob diffs are exclusively line-ending storage differences;
`git diff --cached --ignore-space-at-eol --exit-code --` for all three paths
returns zero. Local working bytes remain the exact bytes independently
reviewed. No acceptance implementation or binding recipe is changed.
The actual proof input digest remains
`5a8f47f8d0afd1d4f957e55babde52a9e9c01babf05c481b988e99ebca2f7758`.

Tests: the real Git transport suite now includes mixed/CRLF fixtures and the
three actual frozen runtime inputs, checking exact bytes under autocrlf true,
false and input. Publication/atlas/transport regressions total 46 PASS; ten
packet checks and six HCR checks PASS. Missing files and corrupt bytes are
still rejected. No test normalizes a frozen packet or silently refreshes its
hash. An initial staging-hash assertion correctly failed before explicit
reindexing; no push was attempted with the mismatched index.

Default `git diff --check` flags the deliberately preserved CRLF as trailing
whitespace. A separate per-command CR-at-EOL-aware whitespace check is used;
this is not a verifier/test waiver or a claim the default whitespace check
passed. No global Git setting is changed.

Rollback is the three scoped attribute rules and the matching raw transport
storage plus tests, performed together only with an honest replacement review
context. Do not normalize or rehash the immutable old packet in place. Main,
reader, purification and scientific ROOT remain gated independently.
