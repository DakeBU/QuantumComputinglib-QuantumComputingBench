# Public-export privacy layer for successor-v4

AUTHOR_WIP_NOT_ADMITTED. This is export privacy only, not a mathematical repair, new source version, independent approval or admission.

Only derive-successor-v4.py and worker-handoff-v4.md have derived public copies here. Each replaces exactly one private absolute repository-root path by the logical placeholder REPOSITORY_ROOT. They are NOT raw-byte aliases. exact-redaction-receipt.json records original and derived digests, precise UTF-8 byte offsets, removed-span digest/length and replacement bytes; the private host path itself is intentionally not repeated.

The derivative script changes only the embedded HANDOFF command's repository-root text. Every function/class AST, including verify, is identical to the original. Supply your actual repository root as a runtime CLI argument; REPOSITORY_ROOT is a placeholder, not an existing directory. The original frozen script hash does NOT equal the derivative script hash.

public-safe-allowlist.json is the explicit transport list. Exact other successor-v4 artifacts and all eight predecessor artifacts remain hash-pinned references; none has been regenerated or modified. The original freeze and original manifest remain valid evidence about the private originals, not manifests of this derivative export. Never silently substitute the derivative for a private original while claiming its original hash. Raw transport of the two listed private originals is forbidden.

Verification behavior: derivative --verify must receive --out pointing at the original sealed successor-v4 package and --predecessor at its unchanged predecessor. It still checks the original freeze against the original files. It does not equate the public derivative's self hash with the sealed original. A stand-alone public transport containing only derivatives cannot claim to pass that original private-byte verification. Parent runs original verification privately and separately compares the graph; same original source-first reviewer remains pending.

Example schematic command (replace each logical placeholder with your own location):

```powershell
python PUBLIC_EXPORT/derive-successor-v4.py --verify --repo REPOSITORY_ROOT --predecessor ORIGINAL_PREDECESSOR --out SEALED_SUCCESSOR_V4
```

No original successor/freeze byte was overwritten. No Lean, Git, network, decoder/reviewer/CI result reading, source change, theorem-premise change, canonical write, scientific ROOT, main admission or PURIFIED status is claimed.
