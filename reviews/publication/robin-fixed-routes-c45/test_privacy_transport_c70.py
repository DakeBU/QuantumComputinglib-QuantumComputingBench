"""Ordinary publication transport scan: URLs and one sealed math type aren't paths."""
import ast,hashlib,json,re,unittest
from pathlib import Path
BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
LESSON='docs/lessons/robin-nine-local-natural-source-v2.md'
LESSON_SHA='10681db8c6f62818bcdd8d6eef787027983b010540e86c547afbaacc34031790'
def scan_public_transport(name,raw):
    text=raw.decode('utf-8-sig')
    def strings(obj):
        if isinstance(obj,dict):
            for k,v in obj.items():yield k;yield from strings(v)
        elif isinstance(obj,list):
            for v in obj:yield from strings(v)
        elif isinstance(obj,str):yield obj
    values=list(strings(json.loads(text))) if name.endswith('.json') else [text]
    if name.endswith('.py'):values += [n.value for n in ast.walk(ast.parse(text)) if isinstance(n,ast.Constant) and isinstance(n.value,str)]
    secret=re.compile(r'(?:github_pat_|ghp_)[A-Za-z0-9_]{20,}')
    drive=re.compile(r'(?<![A-Za-z0-9])[A-Za-z]:[\\/]')
    linux='/'+'/'.join(('home','runner'))+'/'
    known_math=name==LESSON and hashlib.sha256(raw).hexdigest()==LESSON_SHA
    typed='w:'+chr(92)+'mathrm{Fin}'
    skipped=0
    assert not secret.search(text),name
    for value in values:
        assert not secret.search(value) and linux not in value,name
        for hit in drive.finditer(value):
            # This exact frozen statement w:Fin k -> Fin q is mathematical.
            # No unpinned file, modified lesson, other drive or other span skips.
            if known_math and value.startswith(typed,hit.start()):skipped+=1;continue
            raise AssertionError(name)
    if known_math:assert skipped==1
    return skipped
class PrivacyTransportTests(unittest.TestCase):
    def test_https_urls_are_not_drive_suffixes(self):
        self.assertEqual(scan_public_transport('link.json',json.dumps({'url':'https://github.com/DakeBU/Quantum-Computing-Block-Encoding'}).encode()),0)
    def test_raw_and_JSON_encoded_absolute_drives_are_rejected(self):
        drive=chr(67)+':'+chr(92)+'example'+chr(92)+'file'
        for raw in (json.dumps({'path':drive}).encode(),('{"path":"'+chr(92)+'u0043:'+chr(92)+'u005c'+'example"}').encode()):
            with self.assertRaises(AssertionError):scan_public_transport('input.json',raw)
    def test_exact_sealed_mathematical_type_has_one_bounded_exception(self):
        self.assertEqual(scan_public_transport(LESSON,(ROOT/LESSON).read_bytes()),1)
    def test_modified_or_renamed_lesson_cannot_inherit_math_exception(self):
        raw=(ROOT/LESSON).read_bytes()
        for name,data in ((LESSON,raw+bytes([10])),('other.md',raw)):
            with self.assertRaises(AssertionError):scan_public_transport(name,data)
    def test_real_paths_and_raw_or_encoded_credentials_still_fail(self):
        items=[('x.md',('/'+'/'.join(('home','runner'))+'/secret').encode()),
          ('x.md',('w:'+chr(92)+'example').encode()),
          ('x.json',json.dumps({'secret':'github_'+'pat_'+'x'*25}).encode())]
        for name,raw in items:
            with self.assertRaises(AssertionError):scan_public_transport(name,raw)
if __name__=='__main__':unittest.main()
