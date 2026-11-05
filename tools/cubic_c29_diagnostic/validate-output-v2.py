"""Generated actual-field diagnostic, layered on immutable original 319 validator.

No axiom whitelist or acceptance policy. The CI2 set pins identity/kind, not axioms.
Pretty expressions are actual Meta.ppExpr output, not lossless Expr serialization.
"""
import importlib.util
import json
from pathlib import Path
import sys

SCOPE = 'ACTUAL_GENERATED_TYPE_VALUE_AXIOMS_POLICY_UNASSESSED'
KINDS = {'axiomInfo', 'defnInfo', 'thmInfo', 'opaqueInfo', 'quotInfo',
         'inductInfo', 'ctorInfo', 'recInfo'}


def records(stdout):
    tags = ('C29_BINDING_JSON', 'C29_ROOT_JSON', 'C29_GENERATED_JSON', 'C29_SUMMARY_JSON')
    result = {tag: [] for tag in tags}
    for line in stdout.splitlines():
        for tag in tags:
            if line.startswith(tag + ' '):
                result[tag].append(json.loads(line[len(tag) + 1:]))
    return result


def no_accept(row):
    for key in ('sourceAgreement', 'publicationBinding', 'axiomPolicyPass'):
        if key not in row or row[key] is not None:
            raise ValueError('generated diagnostic made acceptance/policy claim: ' + key)
    if row.get('nativeAccepted') is not False:
        raise ValueError('generated diagnostic made native acceptance claim')
    for key in ('scientific_ROOT', 'authorBinding'):
        if key in row and row[key] not in (None, False):
            raise ValueError('generated diagnostic made forbidden extra acceptance claim')


def validate_generated(rows, expected_rows, explicit_names, summary,
                       explicit_count_field='includedIn319ExplicitRootCount'):
    expected_names = [row['actualName'] for row in expected_rows]
    if len(set(expected_names)) != len(expected_names):
        raise ValueError('duplicate expected generated identity')
    expected_kind = {row['actualName']: row['actualKind'] for row in expected_rows}
    actual_names = [row['actualName'] for row in rows]
    if len(set(actual_names)) != len(rows) or set(actual_names) != set(expected_names):
        raise ValueError('generated exact observed identity set/count changed: RESEAL')
    if set(actual_names) & set(explicit_names):
        raise ValueError('generated identity conflated with explicit root')
    for row in rows:
        name = row['actualName']
        if row['actualKind'] not in KINDS or row['actualKind'] != expected_kind[name]:
            raise ValueError('generated actual kind changed: RESEAL')
        if row.get('kernelRootPresent') is not True:
            raise ValueError('generated constant absent from checked kernel environment')
        if row.get('typeAxiomAuditScope') != SCOPE:
            raise ValueError('generated metadata-only or unknown audit scope')
        if not isinstance(row.get('typePrettyExplicit'), str) or not row['typePrettyExplicit'].strip():
            raise ValueError('generated actual type missing')
        for key in ('universeParameters', 'axioms', 'structureParents'):
            values = row.get(key)
            if not isinstance(values, list) or not all(isinstance(v, str) and v for v in values):
                raise ValueError('invalid generated string array: ' + key)
            if len(set(values)) != len(values):
                raise ValueError('duplicate generated array entry: ' + key)
        for key in ('isUnsafe', 'actualPrivate', 'actualHasValueAllowOpaque', 'selfOccursInAxioms'):
            if type(row.get(key)) is not bool:
                raise ValueError('generated missing boolean: ' + key)
        if row['selfOccursInAxioms'] != (name in row['axioms']):
            raise ValueError('generated self axiom observation inconsistent')
        has_value = row['actualKind'] in ('defnInfo', 'thmInfo', 'opaqueInfo')
        if row['actualHasValueAllowOpaque'] != has_value:
            raise ValueError('generated actual value availability/kind inconsistent')
        if 'valuePrettyExplicitAllowOpaque' not in row:
            raise ValueError('generated actual value observation missing')
        value = row['valuePrettyExplicitAllowOpaque']
        if has_value:
            if not isinstance(value, str) or not value.strip():
                raise ValueError('generated actual available value text absent')
        elif value is not None:
            raise ValueError('generated no-value kind has fabricated value')
        if row.get('valueTextScope') != 'ACTUAL_META_PPEXPR_NOT_LOSSLESS_EXPR_SERIALIZATION':
            raise ValueError('generated value pretty-print boundary missing')
        opaque = ('GENERATED_ACTUAL_OPAQUE_INFO' if row['actualKind'] == 'opaqueInfo'
                  else 'GENERATED_NOT_OPAQUE_INFO')
        if row.get('opaqueClassification') != opaque:
            raise ValueError('generated opaque observation inconsistent')
        if row.get(explicit_count_field) is not False:
            raise ValueError('generated merged into source explicit count')
        for key in ('classification', 'userNameViaActualAPI'):
            if not isinstance(row.get(key), str) or not row[key]:
                raise ValueError('generated metadata context absent: ' + key)
        no_accept(row)
    if summary.get('generatedAuditSchema') != 'C29_GENERATED_AUDIT_V2':
        raise ValueError('generated audit terminal schema missing')
    if summary.get('generatedTypeValueAxiomAuditCompleted') != len(rows):
        raise ValueError('generated actual-field completion count mismatch')
    no_accept(summary)
    return dict(generatedActualFieldsCollected=len(rows),
                generatedAxiomInfoCount=sum(r['actualKind'] == 'axiomInfo' for r in rows),
                generatedUnsafeObserved=sum(r['isUnsafe'] for r in rows),
                generatedSelfAxiomObserved=sum(r['selfOccursInAxioms'] for r in rows),
                generatedAxiomUnion=sorted({a for r in rows for a in r['axioms']}),
                axiomPolicyPass=None, sourceAgreement=None, publicationBinding=None,
                nativeAccepted=False, wholeTargetTrustClosed=False)


def validate(expected, stdout, exit_code, generated_expected=None):
    if exit_code != 0:
        raise ValueError('native subprocess failed; partial generated data is not complete')
    package = Path(__file__).parent
    spec = importlib.util.spec_from_file_location('c29_immutable_original_validator', package / 'validate-output.py')
    original = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(original)
    checked = original.validate(expected, stdout, exit_code)
    if generated_expected is None:
        generated_expected = json.loads((package / 'expected-generated-ci2.json').read_text(encoding='utf-8'))
    if generated_expected['targetRawSHA256'] != 'd125f8c239bca1c15e6e4fa6e788df6dd8984394630cb2dcc9be8946c4cbcb55':
        raise ValueError('expected generated source binding mismatch')
    if generated_expected['leanVersion'] != '4.33.0' or len(generated_expected['generated']) != 450:
        raise ValueError('expected generated Lean/count binding mismatch')
    parsed = records(stdout)
    for row in parsed['C29_BINDING_JSON'] + parsed['C29_ROOT_JSON']:
        if row.get('sourceAgreement', 'MISSING') is not None or row.get('nativeAccepted') is not False:
            raise ValueError('binding/explicit diagnostic made acceptance claim')
        for key in ('publicationBinding', 'authorBinding', 'axiomPolicyPass'):
            if key in row and row[key] is not None:
                raise ValueError('binding/explicit made extra acceptance/policy claim')
        if 'scientific_ROOT' in row and row['scientific_ROOT'] is not False:
            raise ValueError('binding/explicit made ROOT claim')
    if parsed['C29_BINDING_JSON'][0]['targetModule'] != generated_expected['targetModule']:
        raise ValueError('generated target module binding mismatch')
    extra = validate_generated(parsed['C29_GENERATED_JSON'], generated_expected['generated'],
                               [r['actualName'] for r in parsed['C29_ROOT_JSON']],
                               parsed['C29_SUMMARY_JSON'][0])
    checked.update(extra)
    return checked


if __name__ == '__main__':
    expected = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
    stdout = Path(sys.argv[2]).read_text(encoding='utf-8', errors='strict')
    print(json.dumps(validate(expected, stdout, int(sys.argv[3])), ensure_ascii=False))
