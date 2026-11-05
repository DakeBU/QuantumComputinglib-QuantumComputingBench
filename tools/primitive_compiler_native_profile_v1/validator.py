"""Strict diagnostic stream partition/binding validation, never axiom policy."""
import json
import re

KINDS = {'axiomInfo', 'defnInfo', 'thmInfo', 'opaqueInfo', 'quotInfo',
         'inductInfo', 'ctorInfo', 'recInfo'}
SOURCE_KINDS = {'def': {'defnInfo'}, 'theorem': {'thmInfo'}, 'lemma': {'thmInfo'},
                'abbrev': {'defnInfo'}, 'structure': {'inductInfo'},
                'inductive': {'inductInfo'}, 'opaque': {'opaqueInfo', 'axiomInfo'},
                'axiom': {'axiomInfo'}, 'instance': {'defnInfo'}}
NO_ACCEPT = dict(sourceAgreement=None, axiomPolicyPass=None, publicationBinding=None,
                 scientificAcceptance=False, nativeAccepted=False, trustClosure=False)
TAGS = ('C31_BINDING_JSON', 'C31_ROOT_JSON', 'C31_GENERATED_JSON', 'C31_SUMMARY_JSON')


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def no_accept(row):
    for key, value in NO_ACCEPT.items():
        require(key in row and row[key] is value, 'forbidden or missing claim ' + key)
    for key in ('authorBinding', 'scientific_ROOT', 'wholeTargetTrustClosed'):
        require(row.get(key) is None or row.get(key) is False, 'forbidden legacy claim')


def strings(value, label):
    require(isinstance(value, list) and all(type(x) is str and x for x in value), label)
    require(len(set(value)) == len(value), 'duplicate ' + label)
    return value


def integer(value, label):
    require(type(value) is int and value >= 0, label)
    return value


def parse(stdout):
    found = {t: [] for t in TAGS}
    terminal = False
    for line in stdout.splitlines():
        if not line.strip():
            continue
        require(not terminal, 'output after terminal summary')
        tag, sep, payload = line.partition(' ')
        # Unexpected output is not silently discarded, including Lean warnings/errors.
        require(sep and tag in found, 'unexpected or malformed output line')
        def unique_pairs(pairs):
            result = {}
            for key, value in pairs:
                require(key not in result, 'duplicate JSON object key')
                result[key] = value
            return result
        row = json.loads(payload, object_pairs_hook=unique_pairs)
        require(type(row) is dict, 'record is not an object')
        no_accept(row)
        found[tag].append(row)
        terminal = tag == 'C31_SUMMARY_JSON'
    require(terminal, 'missing terminal summary')
    return found


def check_observation(row):
    name = row.get('actualName')
    require(type(name) is str and name, 'missing actual name')
    require(row.get('actualKind') in KINDS, 'unknown actual kind')
    require(row.get('kernelRootPresent') is True and
            row.get('kernelTypeAndUniversesAgree') is True, 'kernel observation missing')
    require(row.get('kernelKind') == row['actualKind'], 'kernel kind mismatch')
    text = row.get('typePrettyExplicit')
    require(type(text) is str and text.strip() and not any(x in text for x in ('⋯', '…')),
            'empty or truncated actual type')
    require(row.get('typeTextScope') == 'ACTUAL_META_PPEXPR_NOT_LOSSLESS_EXPR_SERIALIZATION',
            'missing pretty-print boundary')
    for key in ('universeParameters', 'axioms'):
        strings(row.get(key), key)
    for key in ('actualPrivate', 'isUnsafe', 'actualHasValueAllowOpaque', 'selfOccursInAxioms',
                'actualOpaqueInfo', 'actualAxiomInfo', 'sourceOpaque', 'valueTextRequested'):
        require(type(row.get(key)) is bool, 'missing boolean ' + key)
    require(type(row.get('userNameViaActualAPI')) is str and row['userNameViaActualAPI'],
            'actual user-name API observation absent')
    require(row['selfOccursInAxioms'] == (name in row['axioms']), 'self-axiom inconsistency')
    require(row['actualOpaqueInfo'] == (row['actualKind'] == 'opaqueInfo') and
            row['actualAxiomInfo'] == (row['actualKind'] == 'axiomInfo'), 'opaque/axiom inconsistency')
    require(row['actualHasValueAllowOpaque'] is
            (row['actualKind'] in ('defnInfo', 'thmInfo', 'opaqueInfo')),
            'actual kind/value availability mismatch')
    if row['actualKind'] == 'axiomInfo':
        require(row['selfOccursInAxioms'] is True, 'axiomInfo missing its actual self dependency')
    require(row['valueTextRequested'] is False and 'valuePrettyExplicitAllowOpaque' in row
            and row['valuePrettyExplicitAllowOpaque'] is None, 'unrequested/fabricated value text')
    expected = ('NOT_REQUESTED_VALUE_AVAILABLE' if row['actualHasValueAllowOpaque']
                else 'NOT_REQUESTED_NO_VALUE_AVAILABLE')
    require(row.get('valueObservation') == expected, 'incorrect value observation')
    require(row.get('axiomCollection') ==
            'ACTUAL_LEAN_COLLECT_AXIOMS_IMPORTED_EXTENSION_AND_LOCAL_BODIES', 'axiom method absent')
    return name


def validate_profile(profile):
    require(profile.get('schema') == 'C31_NATIVE_PROFILE_V1', 'profile schema')
    modules = profile.get('modules')
    require(isinstance(modules, list) and len(modules) == 3, 'C31 needs three modules')
    module_names = strings([m['module'] for m in modules], 'profile module names')
    roots = profile.get('roots')
    require(isinstance(roots, list) and len(roots) == 87, 'C31 root vector not 87')
    identities = [(r['module'], r['sourceUserName']) for r in roots]
    require(len(set(identities)) == 87, 'duplicate profile root')
    require(sum(r['sourcePrivate'] is True for r in roots) == 8, 'C31 private vector not eight')
    require(all(type(r['sourcePrivate']) is bool and r['sourceKind'] in SOURCE_KINDS and
                r['module'] in module_names for r in roots), 'invalid profile root')
    for module in modules:
        require(re.fullmatch('[0-9a-f]{64}', module['rawSHA256']) is not None, 'bad module SHA')
        part = [r for r in roots if r['module'] == module['module']]
        require(len(part) == module['sourceRoots'] and len(part) > 0, 'module root count')
        require(sum(r['sourcePrivate'] for r in part) == module['privateRoots'], 'module private count')
    require(profile.get('valuesRequested') is False and profile.get('ppDeepTerms') is True
            and profile.get('ppMaxSteps') == 2000000 and profile.get('maxRecDepth') == 10000,
            'profile diagnostic options')
    no_accept(profile)


def validate(profile, stdout, exit_code, *, timed_out, profile_sha, cohort_id, expected_oleans):
    require(type(exit_code) is int and exit_code == 0 and timed_out is False,
            'nonzero/missing/timeout native exit')
    validate_profile(profile)
    records = parse(stdout)
    bindings = records['C31_BINDING_JSON']
    roots = records['C31_ROOT_JSON']
    generated = records['C31_GENERATED_JSON']
    require(len(bindings) == 3 and len(roots) == 87 and len(records['C31_SUMMARY_JSON']) == 1,
            'partial or duplicate record family')
    modules = [m['module'] for m in profile['modules']]
    require([b.get('module') for b in bindings] == modules, 'binding module vector/order')
    require([r.get('module') for r in roots] == [r['module'] for r in profile['roots']],
            'whole source root vector module order')
    actual = []
    for row in roots + generated:
        require(row.get('module') in modules, 'unknown owner module')
        actual.append(check_observation(row))
    require(len(set(actual)) == len(actual), 'duplicate/colliding actual identity')
    for module, binding in zip(modules, bindings):
        require(binding.get('profileSHA256') == profile_sha and binding.get('cohortID') == cohort_id,
                'raw profile or cohort binding drift')
        require(binding.get('resolvedOleanPath') == expected_oleans[module] and
                binding.get('freshOleanPathComparisonPassed') is True, 'fresh olean path drift')
        require(binding.get('ownershipMethod') == 'ENVIRONMENT_MODULE_INDEX_NOT_NAME_PREFIX',
                'ownership guessed from names')
        require(binding.get('ppDeepTerms') is True and binding.get('ppMaxSteps') == 2000000
                and binding.get('maxRecDepth') == 10000, 'pp configuration drift')
        owned = strings(binding.get('ownedNames'), 'owned names')
        require(len(owned) > 0 and integer(binding.get('ownedCount'), 'owned count') == len(owned),
                'empty/incorrect owned inventory')
        expected = [r for r in profile['roots'] if r['module'] == module]
        got = [r for r in roots if r['module'] == module]
        require(binding.get('expectedRoots') == len(expected) and len(got) == len(expected),
                'module explicit count')
        for ordinal, (spec, row) in enumerate(zip(expected, got), 1):
            require(integer(row.get('moduleOrdinal'), 'source ordinal') == ordinal, 'source vector ordinal')
            require(type(row.get('sourcePrivate')) is bool, 'source private flag type')
            for key in ('sourceUserName', 'sourcePrivate', 'sourceKind'):
                require(row.get(key) == spec[key], 'source vector drift ' + key)
            require(row['actualPrivate'] is spec['sourcePrivate'], 'private resolution mismatch')
            require(row['userNameViaActualAPI'] == spec['sourceUserName'], 'private API identity drift')
            if not spec['sourcePrivate']:
                require(row['actualName'] == spec['sourceUserName'], 'public identity drift')
            require(row['actualKind'] in SOURCE_KINDS[spec['sourceKind']], 'source/actual kind drift')
            require(row['sourceOpaque'] == (spec['sourceKind'] == 'opaque'), 'source opaque drift')
        extra = [r for r in generated if r['module'] == module]
        require(all(r.get('includedInExplicitRootCount') is False and r['sourceOpaque'] is False
                    for r in extra), 'generated/explicit conflation')
        emitted = {r['actualName'] for r in got + extra}
        require(emitted == set(owned) and len(got) + len(extra) == len(owned),
                'incomplete actual ownership partition')
        structures = binding.get('structures')
        require(isinstance(structures, list), 'missing actual structures')
        strings([s['actualName'] for s in structures], 'structure identities')
        by_name = {r['actualName']: r for r in got + extra}
        required_structs = {r['sourceUserName']: r.get('structureFields') for r in expected
                            if r['sourceKind'] == 'structure'}
        require(set(required_structs) <= {s['actualName'] for s in structures}, 'source structure absent')
        for structure in structures:
            name = structure['actualName']
            require(name in by_name and by_name[name]['actualKind'] == 'inductInfo', 'structure owner')
            fields = strings(structure.get('fieldNames'), 'structure field names')
            metadata = structure.get('fields')
            require(isinstance(metadata, list) and len(metadata) == len(fields), 'missing structure fields')
            require(set(strings([f['fieldName'] for f in metadata], 'field metadata')) == set(fields),
                    'field metadata partition')
            if name in required_structs:
                require(fields == required_structs[name], 'source field vector drift')
            strings([f['projection'] for f in metadata], 'projection names')
            for field in metadata:
                projection = field['projection']
                require(projection in by_name and by_name[projection]['actualKind'] == field['actualKind'],
                        'field projection not fully observed')
            ctors = strings(structure.get('constructors'), 'constructor names')
            require(len(ctors) > 0 and all(c in by_name and by_name[c]['actualKind'] == 'ctorInfo'
                                          for c in ctors), 'constructor not fully observed')
    summary = records['C31_SUMMARY_JSON'][0]
    require(summary.get('profileSHA256') == profile_sha and summary.get('cohortID') == cohort_id,
            'terminal binding drift')
    require(summary.get('status') == 'FORMAL_DIAGNOSTIC_COMPLETE_NOT_ACCEPTANCE' and
            summary.get('allNamesResolvedUniquely') is True, 'terminal status')
    for field, wanted in [('modulesCompleted', 3), ('rootsCompleted', 87), ('privateCompleted', 8),
                          ('generatedCompleted', len(generated)), ('ownedCompleted', len(actual))]:
        require(integer(summary.get(field), field) == wanted, 'terminal count ' + field)
    # Source structure ensures some generated observations exist, but no guessed baseline.
    require(len(generated) > 0, 'C31 structure-generated inventory empty')
    return dict(status='STREAM_BINDING_PARTITION_COMPLETE_NOT_ACCEPTANCE', roots=87, private=8,
                generated=len(generated), owned=len(actual),
                observedUnsafe=sum(r['isUnsafe'] for r in roots + generated),
                observedSelfAxioms=sum(r['selfOccursInAxioms'] for r in roots + generated),
                observedAxiomUnion=sorted({a for r in roots + generated for a in r['axioms']}),
                **NO_ACCEPT)
