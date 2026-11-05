"""Versioned SP evidence packaging checks; independent verdicts remain separate."""
import copy,hashlib,importlib.util,json,pathlib,unittest,zipfile
ROOT=pathlib.Path(__file__).resolve().parents[3];HERE=pathlib.Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def archive(name):
    with zipfile.ZipFile(HERE/name) as z:return {n:z.read(n) for n in z.namelist()}
def data(name,member):return json.loads(archive(name)[member])
class FoundationSuccessor(unittest.TestCase):
    def test_exact_19_author_successor_and_all_original_seals(self):
        packet=archive('author-v2-frozen-successor.zip');self.assertEqual(len(packet),19)
        self.assertEqual(sha(packet['final-seal.json']),'ae171c7e679d3dbbfd2289dbde73c7c1aaa0feda3111b1a9bc80dc1072d2feb9')
        for x in json.loads(packet['final-seal.json'])['artifacts']:self.assertEqual(sha(packet[x['path']]),x['sha256'])
        self.assertEqual(set(json.loads(packet['allowlist.json'])['files']),set(packet))
    def test_207_raw_inputs_still_match_frozen_original(self):
        pins=data('author-v1-frozen-wip.zip','raw-input-seals.json')['rows'];self.assertEqual(len(pins),207)
        for x in pins:self.assertEqual(sha((ROOT/x['path']).read_bytes()),x['sha256'])
    def test_source_successor_is_exactly_one_editorial_count_edit(self):
        old=archive('author-v1-frozen-wip.zip')['natural-source.md']
        p=data('author-v2-frozen-successor.zip','editorial-proposal.json')
        before=p['exact_before'].encode();after=p['exact_after'].encode();self.assertEqual(old.count(before),1)
        expected=old.replace(before,after,1);actual=(ROOT/'docs/lessons/finite-sp-foundations-v2.md').read_bytes()
        self.assertEqual(actual,expected);self.assertEqual(sha(actual),p['new_source_sha256'])
    def test_all_103_complete_commands_bind_actual_raw_source_slices(self):
        rows=data('author-v2-frozen-successor.zip','declaration-inventory-v2.json')['declarations']
        self.assertEqual(len(rows),103);self.assertEqual(sum(x['private'] for x in rows),5)
        for x in rows:
            raw=(ROOT/x['source']).read_bytes();a,b=x['source_command_byte_offsets']
            self.assertEqual(sha(raw),x['source_module_raw_sha256'])
            self.assertEqual(sha(raw[a:b]),x['source_command_raw_sha256'])
            self.assertEqual(raw[a:b].decode(),x['source_command_raw'])
            self.assertEqual(x['source_command_raw'],x['header_raw']+x['body_separator']+x['body_raw'])
    def test_four_cost_and_21_record_header_repairs_are_complete(self):
        rows=data('author-v2-frozen-successor.zip','declaration-inventory-v2.json')['declarations'];by={x['source_name']:x for x in rows}
        findings=data('source-first-phase3-changes-required.zip','findings-and-erratum.json')['findings']
        cost=next(x for x in findings if x['id']=='I-COST-SIGNATURE-TRUNCATION')
        self.assertEqual(len(cost['affected_and_proposed_complete_signature']),4)
        for x in cost['affected_and_proposed_complete_signature']:
            header=by[x['name']]['signature_or_structure_fields'];self.assertIn('oracleCalls := 0 }',header)
            self.assertEqual(header.strip(),x['complete_signature'].strip())
        record=next(x for x in findings if x['id']=='I-RECORD-HEADER-SUFFIX')
        self.assertEqual(len(record['affected_lexical_names']),21)
        for name in record['affected_lexical_names']:
            row=next(x for x in rows if x['source_name'].endswith('.'+name))
            self.assertEqual(row['body_separator'],'where');self.assertNotIn('where',row['signature_or_structure_fields'])
    def test_parent_graph_successor_changes_no_mathematical_edges(self):
        old=data('author-v2-frozen-successor.zip','source-and-graph-v2.json')
        new=json.loads((HERE/'source-and-graph-v3.json').read_bytes())
        self.assertEqual(len(new['source_construction_hyperedges']),37)
        for k in old:
            if k not in ('comparison_object_separation','version'):self.assertEqual(new[k],old[k])
        self.assertEqual(new['comparison_object_separation']['source'],'natural-source-v2.md')
        self.assertTrue(new['comparison_object_separation']['proposed_repair'].startswith('EDITORIAL_CENSUS_ONLY:'))
        self.assertEqual(new['metadata_successor']['prior_graph_sha256'],sha(archive('author-v2-frozen-successor.zip')['source-and-graph-v2.json']))
        self.assertEqual(new['version'],3)
    def test_actual_current_bindings_and_old_30_records(self):
        spec=importlib.util.spec_from_file_location('foundations_successor_gate',ROOT/'website/scripts/check_research_publications.py')
        gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
        context=json.loads((HERE/'final-context-c43-v3.json').read_bytes())
        for r in context['records']:self.assertEqual(gate.binding_digest(ROOT,r),r['binding_sha256'])
        inventory={r['fullName']:r for r in json.loads((ROOT/'web/library/declarations.json').read_bytes())['declarations']}
        records=json.loads((ROOT/'website/research/publications.json').read_bytes())['records'];self.assertGreaterEqual(len(records),30)
        for r in records[:30]:gate.validate_record(ROOT,r,inventory)
    def test_public_resolver_retains_exact_all_19_logical_artifacts(self):
        context=json.loads((HERE/'final-context-c43-v3.json').read_bytes())
        resolver=context['logical_artifact_resolver'];self.assertEqual(len(resolver),19)
        for name,row in resolver.items():
            self.assertTrue(name.startswith('hermite-export-work/sp-foundations-c42-author-successor/'))
            with zipfile.ZipFile(ROOT/row['archive']) as z:self.assertEqual(sha(z.read(row['member'])),row['member_sha256'])
if __name__=='__main__':unittest.main()
