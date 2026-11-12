"""WIP two-signature-only supplement. No local Lean success is claimed."""
import json
import os
from pathlib import Path
import shutil

NAMES = [
    'QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalFourSquareBranchVector_unit._proof_1_1',
    'QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalFourSquareBranchVector_unit._proof_1_1',
]
TAGS = ('C29_TWO_BINDING_JSON', 'C29_TWO_TYPE_JSON', 'C29_TWO_SUMMARY_JSON')


def no_accept(row):
    for key in ('sourceAgreement', 'publicationBinding', 'axiomPolicyPass'):
        if key not in row or row[key] is not None:
            raise ValueError('supplement made acceptance/policy claim: ' + key)
    if row.get('nativeAccepted') is not False:
        raise ValueError('supplement made native acceptance claim')
    if row.get('scientific_ROOT', False) is not False or row.get('authorBinding') is not None:
        raise ValueError('supplement made ROOT/author binding claim')


def validate_supplement(stdout, exit_code, expected_fresh_path):
    if exit_code != 0:
        raise ValueError('nonzero native exit; partial two-signature stream rejected')
    rows = {tag: [] for tag in TAGS}
    for line in stdout.splitlines():
        for tag in TAGS:
            if line.startswith(tag + ' '):
                rows[tag].append(json.loads(line[len(tag) + 1:]))
    if list(map(len, rows.values())) != [1, 2, 1]:
        raise ValueError('need exactly one fresh binding, two signatures, one terminal summary')
    binding, types, summary = rows[TAGS[0]][0], rows[TAGS[1]], rows[TAGS[2]][0]
    if binding.get('schema') != 'C29_TWO_SIGNATURES_V1' or summary.get('schema') != 'C29_TWO_SIGNATURES_V1':
        raise ValueError('supplement schema mismatch')
    if binding.get('targetModule') != 'QuantumBlockEncoding.CubicStatePreparation':
        raise ValueError('wrong target module')
    if binding.get('freshOleanPathComparisonPassed') is not True:
        raise ValueError('Lean fresh artifact comparison failed')
    if os.path.normcase(str(Path(binding['actualResolvedOleanPath']).resolve())) != os.path.normcase(str(Path(expected_fresh_path).resolve())):
        raise ValueError('supplement did not import the same fresh artifact')
    if binding.get('expectedNames') != NAMES:
        raise ValueError('supplement expected-name binding mismatch')
    if binding.get('ppDeepTerms') is not True or binding.get('ppMaxSteps') != 2000000 or binding.get('maxRecDepth') != 10000:
        raise ValueError('supplement PP option binding changed')
    for i, row in enumerate(types, 1):
        if row.get('ordinal') != i or row.get('actualName') != NAMES[i - 1]:
            raise ValueError('supplement exact signature identity/order changed')
        if row.get('actualKind') != 'thmInfo' or row.get('kernelRootPresent') is not True:
            raise ValueError('supplement signature kind/kernel membership failed')
        text = row.get('typePrettyExplicit')
        if not isinstance(text, str) or not text.strip() or any(glyph in text for glyph in ('⋯', '…', '...')):
            raise ValueError('supplement signature text still omitted/truncated/missing')
        for key in ('universeParameters', 'axioms'):
            values = row.get(key)
            if not isinstance(values, list) or not all(isinstance(v, str) and v for v in values) or len(set(values)) != len(values):
                raise ValueError('invalid supplement actual string array: ' + key)
        if type(row.get('isUnsafe')) is not bool or type(row.get('selfOccursInAxioms')) is not bool:
            raise ValueError('supplement flags absent')
        if row['selfOccursInAxioms'] != (row['actualName'] in row['axioms']):
            raise ValueError('supplement self axiom mismatch')
        if row.get('valuesPrinted') is not False or 'valuePrettyExplicitAllowOpaque' in row:
            raise ValueError('supplement exceeded two-type-only scope')
        no_accept(row)
    if summary.get('completed') != 2 or summary.get('valuesPrinted') is not False or summary.get('scope') != 'TWO_PRETTY_SIGNATURES_ONLY_NOT_AXIOM_POLICY':
        raise ValueError('supplement terminal scope/count mismatch')
    no_accept(binding); no_accept(summary)
    return dict(status='TWO_PRETTY_SIGNATURE_TEXTS_OBSERVED_WITHOUT_OMISSION_GLYPH_NOT_ACCEPTANCE',
                signatures=types, targetFreshOleanSame=True, valuesPrinted=False,
                losslessExprSerialization=False, wholeTargetTrustClosed=False,
                sourceAgreement=None, publicationBinding=None, authorBinding=None,
                axiomPolicyPass=None, scientific_ROOT=False, nativeAccepted=False)


def run_supplemental(package, driver, private, env, lean, fresh_olean,
                     native_call, sha, verify_pins, write_json):
    """Called ONLY after actual successful v5 validation; uses the same fresh namespace.

    Host functions are passed from the existing runner; no alternate native wrapper.
    No target recompile, existing validator mutation or provider cache write occurs.
    """
    package, driver, private, fresh_olean = map(Path, (package, driver, private, fresh_olean))
    pins = json.loads((package / 'supplemental-pins-v1.json').read_text(encoding='utf-8'))
    verify_pins(package, pins['supplementalFiles'])
    verify_pins(package, pins['unchangedBaselineFiles'])
    if pins['exactNames'] != NAMES or pins['targetRawSHA256'] != 'd125f8c239bca1c15e6e4fa6e788df6dd8984394630cb2dcc9be8946c4cbcb55':
        raise ValueError('supplement input direction/source binding drift: RESEAL')
    if env.get('QBE_EXPECT_FRESH_OLEAN') != str(fresh_olean):
        raise ValueError('supplement requires existing same-fresh environment binding')
    if not fresh_olean.is_file():
        raise FileNotFoundError('supplement fresh target olean absent')
    before = sha(fresh_olean)
    destination = driver / 'SupplementalTypes-v1.lean'
    if destination.exists():
        raise FileExistsError('supplement source output already exists; no retry/overwrite')
    shutil.copyfile(package / 'SupplementalTypes-v1.lean', destination)
    if sha(destination) != pins['supplementalFiles']['SupplementalTypes-v1.lean']:
        raise ValueError('supplement source copy pin mismatch')
    write_json(private / 'supplemental-two-types-input.json', dict(
        targetFreshOleanSHA256=before, exactNames=NAMES,
        supplementalFiles=pins['supplementalFiles'], unchangedBaselineFiles=pins['unchangedBaselineFiles'],
        targetRawSHA256=pins['targetRawSHA256'], threads=1, memoryMiB=3072,
        sourceAgreement=None, publicationBinding=None, axiomPolicyPass=None, nativeAccepted=False))
    result = native_call(private, '07-supplemental-two-types-v1',
        [str(lean), '--threads=1', '--memory=3072', 'SupplementalTypes-v1.lean'], driver, env)
    if sha(fresh_olean) != before:
        raise ValueError('supplement fresh artifact changed: RESEAL')
    checked = validate_supplement(
        (private / '07-supplemental-two-types-v1.stdout.raw').read_text(encoding='utf-8', errors='strict'),
        result['exitCode'], fresh_olean)
    verify_pins(package, pins['supplementalFiles'])
    verify_pins(package, pins['unchangedBaselineFiles'])
    checked.update(targetFreshOleanSHA256=before, nativePID=result['PID'], nativeExitCode=result['exitCode'])
    write_json(private / 'supplemental-two-types-completeness.json', checked)
    return checked
