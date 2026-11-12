"""Finite decoder evidence binding checks; no source equivalence or admission oracle."""
import hashlib
from pathlib import PurePosixPath
import re

IDENTITY='/root/primitive_compiler_formal_decoder_c31'
PACKET='reviews/publication/primitive-compiler-c31/decoder-c31/source-formal-seal.json'
PACKET_SHA='0fd3e599c0532c6e308dbb87b26b420f939886d9d39de89c419692946f40cd68'
ARTIFACT='reviews/publication/primitive-compiler-c31/decoder-actual-two-module-addendum-v1-public.zip'
ARTIFACT_SHA='c4ce553fa7bacfe01e067dac38a939145ef266c9f8fed94fa7a10932f2e7c705'
LABELS={
    'QuantumBlockEncoding.PrimitiveMacros':'a5cd337cfc829f09e9247871004e20c1bcec29ebfe13a8ac7550f107638e1e4a',
    'QuantumBlockEncoding.UniformlyControlledRy':'0c0083d8d20df25d3bd5589e0c45b3edd7622700abcb8967dbd8065f2cfb8817'}
FORBIDDEN_KEYS={'nativeAccepted','native_accepted','scientificROOT','scientific_ROOT','PURIFIED','purified','main','axiomPolicyPass','publicationBinding'}


def sha(data): return hashlib.sha256(data).hexdigest()


def require(condition,message):
    if not condition: raise ValueError(message)


def no_unsupported_claims(value):
    if isinstance(value,dict):
        require(not FORBIDDEN_KEYS.intersection(value),'unsupported status field')
        for child in value.values(): no_unsupported_claims(child)
    elif isinstance(value,list):
        for child in value: no_unsupported_claims(child)


def validate(row):
    require(row.get('schema')=='C31_TWO_MODULE_DECODER_FINAL_EVIDENCE_V1','schema')
    require(row.get('role')=='decoder' and row.get('identity')==IDENTITY,'role/actual identity')
    require(type(row.get('run_id')) is str and re.fullmatch(r'c31-formal-decoder/two-module-final-evidence-v1/\d{8}T\d{6}Z-pid\d+',row['run_id']), 'auditable local run label')
    require(row.get('module') in LABELS and row.get('binding_sha256')==LABELS[row['module']],'opaque binding label')
    for path_key,sha_key,path,expected in [('packet_path','packet_sha256',PACKET,PACKET_SHA),
        ('artifact_path','artifact_sha256',ARTIFACT,ARTIFACT_SHA)]:
        require(row.get(path_key)==path and row.get(sha_key)==expected,'exact packet/artifact file binding')
        p=PurePosixPath(row[path_key]); require(not p.is_absolute() and '..' not in p.parts,'unsafe logical path')
    require(row.get('source_blind') is True and row.get('source_blind_scope')=='ORIGINAL_FORMAL_ONLY_RECONSTRUCTION_NO_AUTHOR_NATURAL_OR_REVIEWER_CONTEXT','bounded blindness')
    require(type(row.get('reconstruction')) is str and len(row['reconstruction'])>200,'substantive reconstruction reference')
    disclosure=row.get('later_context_disclosure',{})
    require(disclosure.get('own_actual_formal_CI_read_after_original_seal') is True and
        disclosure.get('own_runtime_and_kernel_proof_technical_work_after_original_seal') is True and
        disclosure.get('parent_opaque_labels_received_after_addendum_seal') is True and
        disclosure.get('author_natural_source_read') is False and disclosure.get('author_candidate_packet_read') is False and
        disclosure.get('source_first_reviewer_result_read') is False,'missing honest later scope disclosure')
    opaque=row.get('late_opaque_context',{})
    require(opaque.get('label_only') is True and opaque.get('recomputed_by_decoder') is False and
        opaque.get('semantic_identity_inferred') is False,'opaque label promoted to semantics')
    require(row.get('source_semantic_agreement') is None and row.get('admission')=='NOT_PERFORMED_PARENT_AND_DISTINCT_REVIEWER_OWNED','no self-admission')
    no_unsupported_claims(row)
    return True
