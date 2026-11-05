# C375 exact typed-maintenance policy review

Verdict: **accepted-for-compatibility-only**, confined to the exact five policy-candidate files in `W/c373-typed-policy-successor/` and the compatibility-only boundary of the two C372 drafts listed below. No required code change found within this bounded review. This is not installation approval by itself, admission of a real maintenance record, main/release admission, source assimilation, BE-root closure or TCB clearance.

Reviewer: `/root/robin_compatibility_review_c364`, not the policy author. Prior C364/C365/C371 freezes remain unchanged. `R/` and `W/` are logical repository/work roots; no local absolute paths are included.

## Exact read/binding extent

| Input | Bytes | SHA256 |
| --- | ---: | --- |
| W/c373-typed-policy-successor/check_toolchain_maintenance.py | 13339 | `f178ba5a2475086b7714076f3867f2c06c96ca412401500a78315fdf56338ea0` |
| W/c373-typed-policy-successor/test_toolchain_maintenance.py | 17047 | `94081fee920cd36a78656ba02c0dc4679f020902f61398821387c7f79a49a738` |
| W/c373-typed-policy-successor/check_research_publications.py | 11374 | `c97f4da5fc7ca47c866ee4514a3c23e299b7117bb8993d2ad57575397aac10ad` |
| W/c373-typed-policy-successor/publication-integration.patch | 1934 | `912c293c8fa63d9f1142fca91ecbc0f4defdfe6fbdc07dadfbc29d60143f5029` |
| W/c373-typed-policy-successor/README.md | 1215 | `f533ea44dcf2255308df44a6ad04d2cbc7220d3c4c49d287cb220a39329e2b0b` |
| W/c372-maintenance-protocol-addendum.md | 2968 | `a33d8811a6292535a824b69fbb2d8294fe44f7e15534d31c44f84e75c8a2e17b` |
| W/c372-robin-maintenance-lesson.md | 2579 | `4ea2384889a01681ac463aae856966b7678735a6029cf5774b2b823245e6d5d2` |

The maintenance checker, README and both drafts were newly read completely. The publication checker and integration patch exactly match the files completely read during C365/C371; their complete reading is mechanically reused under the matching hashes. Successor test lines 1-278 were byte-compared with the unchanged, previously fully read C367 test prefix; lines 279-301 were newly read completely. The old test's complete SHA256 remains `7930cce93c728ff65eba85c12efc51adad7d9391ad45d34eef7b415d5c8d76d5`. Thus no unseen changed region is covered merely by a summary.

The ordinary test class at `R/website/scripts/test_research_atlas.py:227-325` was extracted and executed again; whole-file hash remains `cd189d96c8dbed7722cd06d1f9eb07842937a5e294abcfe6fa21f009e30582f8` (19930 bytes). No full atlas-module import or new semantic reading of other classes is claimed. Real historical seals/actors, actual eleven-input manifests, CI artifacts, declaration exports, Lean/paper content, C366 and later candidates were not reviewed here.

## Integrity result and independent regressions

The common root commits `expected_fields`, receipt paths and explicit artifact identities. Each actual receipt's stable fields are now compared using deterministic JSON with sorted keys, compact separators, `ensure_ascii=False` and `allow_nan=False` (checker lines 131-138). This distinguishes JSON booleans, integers and floats recursively. The receipt's own root field and resulting file SHA remain outside that stable payload and are checked separately, so no recursive hash cycle is introduced. The existing stale-root and recomputed-root/old-receipt tests still pass.

I reran the failure recipes on fresh real temporary fixtures, using the actual validator. Baselines were validated before tampering. Each single-wrapper probe rewrote only that receipt and its own outer SHA, without changing root-bound expectations, the common root or the other five receipt files:

- C365 F1-A/B/C: unrelated original seal, actor/run substitution and runtime/native-disclosure substitution all reject with receipt-semantics mismatch.
- C371 F2: an accepted baseline with workflow ID JSON number `1` cannot be replaced by JSON `true`.
- Twelve independent nested dict/list probes reject every ordered substitution within `{true, 1, 1.0}` and `{false, 0, 0.0}`.
- NaN, positive infinity and negative infinity each reject both as receipt-only substitutions and as newly root-bound expected/actual nested metadata. All six fail with `ValueError: Out of range float values are not JSON compliant`; the publication entry point treats ValueError as gate failure.

That is **22 independently run probes, all rejected as required**: 3 F1 + 1 exact F2 + 12 nested + 6 nonfinite. The 19 receipt-only probes retained the original root and byte-identical other five receipts; the three deliberately fully rebound nonfinite cases instead test invalid metadata rejection even after complete fixture rebinding. No genuine acceptance record or official runtime result was generated.

Additional actual runs: successor suite **33 tests, 20.256 s, OK**; original ordinary publication class against this candidate **12 tests, 0.803 s, OK**; **5/5** actual dispatcher scenarios passed (separate counts, missing record, mixed lanes, unknown changed module, ordinary experimental rejection). Only fixture case constants/Git responses, changed-module selection and maintenance leaf import were substituted; the ordinary validator was not mocked. These are distinct suites/scenarios, not claims of independent human reviews or complete state-space testing.

## Scope and draft assessment

The ordinary validator/dispatcher are unchanged exact bytes. Ordinary experimental source still rejects, lane mixing and missing records fail, and compatibility counts remain separate from source-assimilation counts. Case-sensitive Lean-name handling is retained. The fixed eleven-input historical raw scope remains separate from the larger local compiler context; original seals, actor/run provenance and runtime/native disclosures cannot be changed by the demonstrated own-wrapper attacks. Root commitment does not authenticate those facts or human honesty. Real actors/artifacts and raw-to-formal associations still need their own exact evidence review.

Both C372 drafts fit this limited policy: they retain experimental status, UNKNOWN historical formalizer, no scientific promotion, explicit old raw-fold refutation and conditional prepared compression, full physical operator/adjoint/unitarity/extraction/resource gaps, native/axiom debt, and separate executable/site/reader/CI gates before main. BE is the paper-research scope; unrelated PDE results are excluded, not invented release prerequisites. This accepts their boundary wording, not their case-specific historical/CI assertions as newly verified facts.

The code permits the compatibility and policy reviewer identities to coincide, but neither may be the maintainer/decoder/whole-module reviewer as specified by its separation checks. The drafts' distinct policy review is understood as a separate independent review role/artifact, not an additional code-enforced identity different from the compatibility reviewer. No broader identity rule is certified. The 395-export and historical coverage metadata were not independently regenerated here.

## Disposition

F1 and F2 are closed for the reproduced integrity attacks in these exact bytes. No required change remains for this bounded policy-code objective. Any changed checker, protocol/lesson content, receipt expectations, source/config bytes or real case needs the corresponding fresh bindings and admission checks; this review is not a waiver or a real-case verdict. Existing scientific and trust debt remains unchanged.

Only the new C375 three-file packet and automatically cleaned synthetic temporary fixtures were written. No candidate/production/old packet edit, installation, Git, network, Lean or children occurred; no permission escalation was needed. Failure class: NONE for this code review. STOP after freeze.
