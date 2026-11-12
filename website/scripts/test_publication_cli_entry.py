"""Isolated child CLI regression; real code/files, ONLY Git replies mocked."""
from pathlib import Path
import json,subprocess,sys,tempfile,unittest

HERE=Path(__file__).resolve().parent
CANDIDATE=HERE

class CLITests(unittest.TestCase):
    def invoke(self,changed):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'synthetic-repo';scripts=root/'website/scripts';scripts.mkdir(parents=True)
            for name in ('check_research_publications.py','check_toolchain_maintenance.py'):
                (scripts/name).write_bytes((CANDIDATE/name).read_bytes())
            research=root/'website/research';research.mkdir()
            (research/'publications.json').write_text('{"schema_version":1,"records":[]}',encoding='utf-8')
            wrapper='''import json,runpy,subprocess,sys
from pathlib import Path
from unittest.mock import patch
script=Path(sys.argv[1]);changed=json.loads(sys.argv[2])
sys.path[:]=[str(script.parent)]+[p for p in sys.path if p and p!=str(script.parents[2])]
sys.argv=[str(script),'--root',str(script.parents[2]),'--base','SYNTHETIC_BASE']
def fake_git(command,**kw):
    assert command[0]=='git',command
    if command[1]=='rev-parse':out='0'*40+'\\n'
    else:
        assert command[1:3]==['diff','--name-only'],command
        out='\\n'.join(changed)
    return subprocess.CompletedProcess(command,0,out,'')
with patch.object(subprocess,'run',side_effect=fake_git):
    runpy.run_path(str(script),run_name='__main__')
'''
            result=subprocess.run([sys.executable,'-I','-B','-c',wrapper,str(scripts/'check_research_publications.py'),json.dumps(changed)],
                                  cwd=tmp,capture_output=True,text=True,timeout=20)
            return result

    def test_cold_foreign_directory_cli_loads_only_trusted_sibling_package(self):
        result=self.invoke([])
        self.assertEqual(result.returncode,0,result.stderr)
        obj=json.loads(result.stdout)
        self.assertEqual(obj['accepted_module_packets'],0)
        self.assertEqual(obj['compatibility_maintenance_module_packets'],0)
        self.assertIs(obj['natural_language_equivalence_proved'],False)

    def test_missing_record_still_fails_in_real_entry(self):
        result=self.invoke(['QuantumBlockEncoding/SyntheticMissing.lean'])
        self.assertNotEqual(result.returncode,0)
        self.assertIn('lack reviewed publication records',result.stderr)
        self.assertNotIn('ModuleNotFoundError',result.stderr)

if __name__=='__main__':unittest.main()
