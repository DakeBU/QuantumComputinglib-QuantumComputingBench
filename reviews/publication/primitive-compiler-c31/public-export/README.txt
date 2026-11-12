PUBLICSAFE C31 AUTHOR/WIP projection

public-allowlist.json is the explicit export allowlist. EXACT_ORIGINAL_REFERENCE entries refer to sibling originals that were privacy-screened and retain exactly their recorded bytes/hashes; a transport may materialize only those named originals. No wildcard export is authorized.

handoff.public.txt is a path-only derivative, NOT an alias for handoff.txt. Its original/derived hashes and exact byte-edit receipt are separate. The original handoff is intentionally withheld. Never substitute the derivative under the original filename or original digest.

Original outputs-manifest/metadata-freeze/supplement-manifest and every publication binding are unchanged. Those historical manifests describe original inputs; the public projection is not a new seal and does not assert all private-original bytes are present. In particular the original supplement's handoff hash does not match this derivative.

verify-author-package.py v1 remains a recorded failure artifact, not the run recipe. verify-author-package-v2.py retains only its previously recorded process-local path adapter. Public export does not modify either script. Full author integrity replay requires original exact artifacts and the pinned REPOSITORY_ROOT; public bytes alone do not verify withheld originals or all historical provenance.

Privacy replay: python verify-public-export.py --export PUBLIC_EXPORT_DIRECTORY
Original author-integrity replay, only when exact original manifest inputs and pinned repository are available: python verify-author-package-v2.py --repo REPOSITORY_ROOT --out AUTHOR_PACKAGE_DIRECTORY

This export performs no decoder/reviewer/CI work, new mathematics, Lean, Git, network or canonical writes. Every result remains AUTHOR/WIP; admission, native verification, ROOT and PURIFIED are not claimed.
