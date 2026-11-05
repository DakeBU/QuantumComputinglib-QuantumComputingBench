# Active-walk recovery: independently checked evidence checkpoint

Status: a bounded integer theorem with an independently reconstructed and
source-compared interface, exact source/formal/build binding, and an independently
observed focused root elaboration. **Not production-admitted, PROOF_SEALED,
whole-paper formalized, circuit/resource certified, or PURIFIED.**

This is an additive successor to `../active-walk-c88/`. Nothing in that historical
checkpoint is rewritten. Its pending-review statements were correct at capture
time. The exact statement remains
`ASPBE.Uncompute.recover_zWalk_active`: along the actual active integer walk,
recover the incoming swap flag and parity from the successor. It does not
recover the entire predecessor or specify a finite-width reversible circuit.

## What changed in the evidence

1. A fresh source-blind decoder reconstructed the complete small target, its
   public/private binders, total decoder, invariant producer and guarded cases.
2. A distinct source-first reviewer sealed its own mathematics before seeing
   that decoder, then separately compared the actual packet. Both agree on the
   complete small target, with no excess public assumption or missing supplier
   found. The source-domain generalization and internal off-domain definition
   remain explicitly disclosed. The decoder transcription omits exactly two
   blank masked lines; it is not represented as byte-identical input.
3. The three author provider files and the ASPBE composition were bound to
   exact Git blobs, exact comment-redacted review inputs and actual staged
   compiler inputs. A bounded independent redactor and nine tests are included;
   neither is advertised as a general Lean lexer proof.
4. Four staged redacted modules compiled with Lean 4.33.0. A distinct reviewer
   then independently elaborated the root into a new output, checked local
   import resolution and matched the exact root type/axiom stdout and C91 root
   artifact. The ordinary axiom set is `propext`, `Classical.choice`, `Quot.sound`.
5. An additive metadata review checked all 59 records of the upstream decoder's
   context overlay. It resolves namespace/ambient temporal ambiguity for new
   consumers, without pretending the original ambiguous fields were exact.

Each archive preserves its actor's original bytes and seal. `packet-index.json`
binds every archive member. Hashes and identity labels are procedural evidence,
not a theorem of reviewer independence or an external immutable timestamp.
The parent supplies no rewritten accepted-review wrapper or module admission.

## Reproduce the bounded checks

From the repository root:

```sh
python -B -m unittest discover -s experiments/uncompute-2610-22367/reviewed-walk-c94 -p 'test*.py'
```

These tests replay evidence integrity and file-specific masking, not compilation.
`reviewed-formal-inputs-original.zip` contains the exact four masked modules,
three configuration inputs and their original inventory. The parent checkpoint's
original upstream archive retains raw author sources and Apache-2.0/MIT licenses.
The masked sources are attributed derivatives, not new ASPBE-authored proofs.

For a new focused compile, prepare an isolated tree from the reviewed inputs;
use the exact Lean/toolchain/Mathlib context bound by `execution-observation.json`.
Compile `Hddivsteps590/Defs`, `NumberTheory`, `Recovery`, then `WalkRecovery`,
in order with `lake env lean -M1536 -j1`, writing outputs to that isolated tree.
Put only that tree first on `LEAN_PATH`; use `--deps` to verify its local chain.
Check memory before each run, retaining at least 2048 MiB beyond the compiler cap.
The observation is a path-free selected-field derivative of retained raw logs,
not a raw log with its meaning silently changed. Original raw-log hashes remain
distinct from the derivative's bytes.

## Exact remaining boundary

The reviewer directly witnessed its own fresh root output, but did not witness
the historical initial emptiness of the earlier C91 directory. Cached Lean and
Mathlib are reused; neither independent provider rebuilding nor a clean TCB audit
is claimed. A dirty cached Verso warning and the author's style warning remain
disclosed. The first failed C88 proof, including failed elaboration's `sorryAx`,
remains a failure and is not rescued by a printed type.

Full repository integration, production module admission, finite signed-word
overflow, coherent/relative-phase/measurement-feedback/cleanup semantics,
actual circuits and resources, A.3 external590/primality, the paper's remaining
constructions and Hermite's finite-bit root remain open. See the original review
packets for narrower qualifications; no SP/BE speedup is inferred.

## Next source-first supplier

The Gaussian archive is separately **SOURCE_ONLY_FROZEN_UNREVIEWED**. It pins
the finite-function source contract, construction graph and unresolved witnesses
before code access. It is not a Gaussian state-preparation or diagonal-BE
certificate. An independent raw-source review is in progress; its eventual
comparison must be a new sealed packet. Do not turn its reported finite error
or Toffoli/qubit counts into a local theorem or a uniform family result.

Credit: [Gu, Kemeny, Yelin and Lukin, arXiv:2610.22367v1](https://arxiv.org/abs/2610.22367v1)
and [their pinned original implementation](https://github.com/andigu/uncompute/tree/64b5a13aa249f1360846657392e6c66817b26d0f).
No raw paper figures/pages are redistributed or relicensed. These new audit
records do not establish novelty of the authors' mathematics for ASPBE.
