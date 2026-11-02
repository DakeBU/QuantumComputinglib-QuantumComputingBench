"""Publish the reuse guide and exact license downloads; no proof/scoring changes."""
from pathlib import Path
import shutil

from website.scripts import build_site

ROOT = Path(__file__).resolve().parents[2]
DOWNLOADS = {
    "MIT.txt": "LICENSE",
    "Apache-2.0.txt": "LICENSES/Apache-2.0.txt",
    "NOTICE.md": "NOTICE.md",
    "Third-party-notices.md": "LICENSES/THIRD-PARTY-NOTICES.md",
    "MathJax-LICENSE.txt": "website/static/vendor/mathjax@3.2.2/LICENSE",
}


def publish(root: Path, coverage: dict, gate: dict, context: dict) -> None:
    # Validate all inputs before emitting a partial guide or empty download.
    sources = {name: ROOT / relative for name, relative in DOWNLOADS.items()}
    body = (ROOT / "website/licensing.html").read_text(encoding="utf-8")
    for source in sources.values():
        if not source.is_file() or not source.stat().st_size:
            raise ValueError("Required license or notice is missing: " + source.name)
    page = build_site.page_template(title="Licenses and reuse", route="licensing/",
                                    current="", body=body, coverage=coverage,
                                    gate=gate, context=context)
    build_site.write_page(root, "licensing", page)
    destination = root / "licenses"
    destination.mkdir(parents=True, exist_ok=True)
    for name, source in sources.items():
        shutil.copyfile(source, destination / name)
