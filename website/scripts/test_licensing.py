"""License text, exact downloads and no-JavaScript entry regression checks."""
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from website.scripts import build_site, publish_licensing as licensing
from website.scripts.sidebar_navigation import render_navigation, replace_navigation

ROOT = Path(__file__).resolve().parents[2]
APACHE_SHA = "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30"


class LinkParser(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.links.append(dict(attrs).get("href", ""))


class LicensingTests(unittest.TestCase):
    def test_complete_standard_license_is_exact_and_MIT_remains_default(self):
        raw = (ROOT / "LICENSES/Apache-2.0.txt").read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), APACHE_SHA)
        self.assertIn(b"APPENDIX: How to apply the Apache License", raw)
        self.assertIn(b"Copyright [yyyy] [name of copyright owner]", raw)
        self.assertTrue((ROOT / "LICENSE").read_text().startswith("MIT License"))

    def test_scope_is_not_blanket_relicensing_or_new_MIT_conditions(self):
        body = (ROOT / "website/licensing.html").read_text(encoding="utf-8")
        for marker in ("default license is MIT", "does not make this an Apache-licensed repository",
                       "MathJax 3.2.2", "not permission to copy", "patent conditions",
                       "NOTICE content", "not an additional MIT license condition",
                       "Sho Sonoda", "Verso Blueprint"):
            self.assertIn(marker, body)

    def test_actual_page_and_all_downloads_are_published_exactly(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            context = build_site.git_context()
            licensing.publish(out, {"publicDeclarationCount": 0}, {"passed": True}, context)
            body = (out / "licensing/index.html").read_text(encoding="utf-8")
            self.assertIn('<h1>Reuse with the right license and attribution</h1>', body)
            self.assertIn('data-site-root="../"', body)
            for name, source in licensing.DOWNLOADS.items():
                self.assertEqual((out / "licenses" / name).read_bytes(), (ROOT / source).read_bytes())
            for href in LinkParser(body).links:
                if href.startswith("../licenses/"):
                    self.assertTrue((out / "licensing" / href).resolve().is_file(), href)

    def test_missing_or_empty_license_fails_before_partial_publication(self):
        for empty in (False, True):
            with self.subTest(empty=empty), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                (root / "website").mkdir()
                (root / "website/licensing.html").write_text("<h1>Fixture</h1>")
                if empty:
                    (root / "LICENSE").touch()
                out = root / "output"
                with patch.object(licensing, "ROOT", root), self.assertRaises(ValueError):
                    licensing.publish(out, {}, {}, {})
                self.assertFalse(out.exists())

    def test_native_sidebar_and_footer_work_at_every_depth_and_are_idempotent(self):
        papers = json.loads((ROOT / "website/papers.json").read_text(encoding="utf-8"))
        for prefix in ("./", "../", "../../", "../../../"):
            with self.subTest(prefix=prefix):
                nav = render_navigation(prefix, "licensing/index.html", papers, [])
                self.assertEqual(nav.count('href="' + prefix + 'licensing/index.html"'), 1)
                self.assertIn('aria-current="page">Licenses and reuse', nav)
                page = nav + '<footer class="site-footer"><nav aria-label="Footer"><a href="attribution/">Attribution</a></nav></footer>'
                result = replace_navigation(page, prefix, "licensing/index.html", papers, [])
                self.assertEqual(result.count('data-license-link="1"'), 1)
                self.assertIn('data-license-link="1" href="' + prefix + 'licensing/index.html"', result)
                self.assertEqual(replace_navigation(result, prefix, "licensing/index.html", papers, []), result)

    def test_extension_pipeline_publishes_before_its_search_rebuild(self):
        source = (ROOT / "website/scripts/publish_extensions.py").read_text(encoding="utf-8")
        self.assertLess(source.index("publish_licensing.publish("), source.index("    rebuild_search_and_metadata(root,"))
        self.assertIn('"kind": "licensing"', source)
        for script in ("scripts/build-website.sh", "scripts/build-website.ps1"):
            self.assertIn("publish_extensions.py", (ROOT / script).read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
