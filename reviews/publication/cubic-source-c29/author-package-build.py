#!/usr/bin/env python3
"""C29 author-only serialization of already frozen whole-module mathematics.

No Lean, Git, network, canonical write or independent-result read. New files
are emitted exclusively through apply_patch, retaining partial output on
failure. --verify reads only. Trusted binding_digest is unchanged; no
validate_record, check or main entry point is called.
"""
from __future__ import annotations
import argparse
import base64
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
PREFIX = "reviews/publication/cubic-source-c29/"
LESSON = "docs/lessons/cubic-grid-rational-operators-and-contracts.md"
SOURCE_ID = "aspbe-local-cubic-grid-rational-operators"
TARGET = "QuantumBlockEncoding/CubicStatePreparation.lean"
TARGET_SHA = "d125f8c239bca1c15e6e4fa6e788df6dd8984394630cb2dcc9be8946c4cbcb55"
BASE = "f2cba045611a0d11c5995c29607569726bf1d6c5"
HEAD = "6d755d1"
WIP = "AUTHOR_WIP_NOT_ADMITTED"
ORIGINAL = {
    "source-only.md": "e3e594b40b44bd474a4c98cf61c052b5f2a42ec8082de8d6164bd4f1e1df3dc7",
    "author-private-coverage.md": "bf168e93e158ccd4df7fb5be86b1d078d53dedd2a8589ba15c1838c28ce100a9",
    "source-freeze.md": "d47efeee0d299663d95ea35accb9bacd38db280f78445ae0893368c688aca388",
}
ROOT_RE = re.compile(r"^(?:@\[[^\n]*?\]\s+)?(?P<private>private\s+)?(?P<noncomputable>noncomputable\s+)?(?P<kind>def|theorem|lemma|structure|opaque|abbrev|inductive|instance)\s+(?P<name>[\w'.]+)", re.M)
RESIDUAL = (
    "Retrospective local source; historical formalizer UNKNOWN. Distinct unnormalized rank-one O, diagonal D and linear X, exact Rat matrix carriers and scales N/1 retained. "
    "Four-square choice and 8D rational orthogonal direct sums establish matrix existence, not deterministic polynomial finite-bit preprocessing, gate/ancilla/depth or normalized SP. "
    "Multiplication of extracted clean matrices is not physical block-unitary composition. Generic cubic payload.A is not constrained to D; specific instance proves that equality. "
    "Primitive unitary/extraction and expanded cleanup/extraction predicates remain opaque conditional obligations; arbitrary Prop/resource/description fields are not circuit semantics. "
    "Generic cleanup contains only uncompute-after-compute; readonly signal basis function is not Ry amplitude semantics. Concrete rational all-vector Euclidean error transfer is not an approximation producer or scalar-extension theorem. "
    "Full rank-one denotation, normalized nonzero success/amplification, QSVT supplier/global phases, common-backend composition, finite-bit synthesis and family executable acceptance remain open."
)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def data_bytes(obj):
    return (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode()


def emit_raw(out, name, raw):
    """Exclusive new file, bounded argv patches, no shell redirection/writes."""
    destination = out / name
    assert destination.parent == out and not destination.exists(), name
    text = raw.decode()
    assert text.endswith("\n"), name
    lines = text.splitlines()
    chunks, block, length = [], [], 0
    for line in lines:
        if block and length + len(line) > 9500:
            chunks.append(block)
            block, length = [], 0
        assert len(line) < 12000, (name, "oversized line")
        block.append(line)
        length += len(line) + 2
    if block:
        chunks.append(block)
    exe = shutil.which("codex.exe")
    assert exe, "apply_patch host unavailable"
    prior = []
    for index, chunk in enumerate(chunks):
        if not index:
            patch = "*** Begin Patch\n*** Add File: " + name + "\n"
        else:
            patch = "*** Begin Patch\n*** Update File: " + name + "\n@@\n"
            # EOF anchor avoids duplicate JSON-line insertion. One line also
            # bounds Windows argv when raw-base64 context lines are 6000 chars.
            patch += " " + prior[-1] + "\n"
        patch += "".join("+" + line + "\n" for line in chunk)
        if index:
            patch += "*** End of File\n"
        patch += "*** End Patch"
        result = subprocess.run([exe, "--codex-run-as-apply-patch", patch],
                                cwd=out, capture_output=True, text=True)
        assert result.returncode == 0, (name, index, result.stdout, result.stderr)
        prior.extend(chunk)
    assert destination.read_bytes() == raw, (name, "emitted-byte mismatch")


def emit(out, name, obj):
    emit_raw(out, name, data_bytes(obj))


def file_record(path, relative, full=False):
    raw = path.read_bytes()
    rec = {"path": relative, "sha256": sha(raw), "bytes": len(raw)}
    if full:
        rec["full_source_lines"] = raw.decode().splitlines(keepends=True)
        encoded = base64.b64encode(raw).decode()
        rec["full_source_utf8_base64_chunks"] = [encoded[i:i+6000] for i in range(0, len(encoded), 6000)]
        assert "".join(rec["full_source_lines"]).encode() == raw
    return rec


def mask_comments(text):
    """Preserve source offsets/newlines, including nested Lean block comments."""
    chars, i, depth, quoted = list(text), 0, 0, False
    while i < len(text):
        if depth:
            if text.startswith("/-", i):
                chars[i:i+2] = "  "
                depth += 1
                i += 2
            elif text.startswith("-/", i):
                chars[i:i+2] = "  "
                depth -= 1
                i += 2
            else:
                if chars[i] not in "\r\n":
                    chars[i] = " "
                i += 1
        elif quoted:
            if text[i] == "\\":
                i += 2
            else:
                if text[i] == '"':
                    quoted = False
                i += 1
        elif text[i] == '"':
            quoted, i = True, i+1
        elif text.startswith("/-", i):
            chars[i:i+2] = "  "
            depth, i = 1, i+2
        elif text.startswith("--", i):
            end = text.find("\n", i)
            end = len(text) if end < 0 else end
            chars[i:end] = [" " if ch not in "\r\n" else ch for ch in text[i:end]]
            i = end
        else:
            i += 1
    assert depth == 0
    return "".join(chars)


def split_definition(text):
    stack, quoted, i = [], False, 0
    while i < len(text):
        ch = text[i]
        if quoted:
            if ch == "\\":
                i += 2
                continue
            if ch == '"':
                quoted = False
        elif ch == '"':
            quoted = True
        elif ch in "({[":
            stack.append(ch)
        elif ch in ")}]":
            if stack:
                stack.pop()
        elif not stack and (text.startswith(":=", i) or
                           re.match(r"where(?:\s|$)", text[i:])):
            return text[:i].rstrip(), text[i:]
        i += 1
    return text.rstrip(), ""


def imports(text):
    return re.findall(r"^(?:public\s+)?import\s+(\S+)\s*$", mask_comments(text), re.M)


def inventory(relative, raw):
    text = raw.decode()
    masked = mask_comments(text)
    matches = list(ROOT_RE.finditer(masked))
    scope_events = list(re.finditer(r"^(namespace\s+\S+|end(?:\s+\S+)?)\s*$", masked, re.M))
    roots = []
    for index, match in enumerate(matches):
        stack = []
        for event in scope_events:
            if event.start() >= match.start():
                break
            command = event[1]
            if command.startswith("namespace "):
                stack.append(command.split()[1])
            elif stack:
                stack.pop()
        end = matches[index+1].start() if index+1 < len(matches) else len(text)
        block = text[match.start():end]
        clean_block = masked[match.start():end]
        header, body = split_definition(clean_block)
        roots.append({
            "name": ".".join(stack + [match["name"]]), "module": relative,
            "kind": match["kind"], "private": bool(match["private"]),
            "noncomputable": bool(match["noncomputable"]),
            "lexical_local_name": match["name"], "line": text.count("\n", 0, match.start())+1,
            "source_end_line_before_next_declaration": text.count("\n", 0, end),
            "ambient_namespace_stack": stack, "exact_lexical_header": header,
            "source_block_sha256": sha(block.encode()), "source_block": block,
            "clean_definition_body": body,
        })
    return roots


def private_map(out):
    result = {}
    tick = chr(96)
    pattern = re.compile(rf"^\| (\d+) \| {tick}([^{tick}]+){tick} \| (public|private) (.*?) \| (\d+)–(\d+) \| (S\d\d) \| {tick}(.*){tick} \|$")
    for line in (out/"author-private-coverage.md").read_text(encoding="utf-8").splitlines():
        m = pattern.match(line)
        if m:
            assert m[2] not in result
            result[m[2]] = {"ordinal": int(m[1]), "visibility": m[3], "kind": m[4],
                           "source_region": m[7], "frozen_exact_header": m[8]}
    assert len(result) == 319
    return result


def paragraphs(raw):
    text = raw.decode()
    pieces = re.findall(r"[^\n](?:.*?)(?:\n[ \t]*\n+|\Z)|\n+", text, re.S)
    assert "".join(pieces) == text
    result, offset, line, section = [], 0, 1, None
    for index, piece in enumerate(pieces, 1):
        heading = re.match(r"## (S\d\d)\.", piece)
        if heading:
            section = heading[1]
        nav = piece.lstrip().startswith("#") or not piece.strip()
        intro = section is None
        excluded = nav or intro
        encoded = piece.encode()
        result.append({
            "id": f"paragraph:{index:03d}", "source_region": section,
            "source_lines": [line, line+piece.rstrip("\n").count("\n")],
            "start_utf8_byte": offset, "end_utf8_byte": offset+len(encoded),
            "exact_text": piece, "sha256": sha(encoded),
            "disposition": "EXCLUDED" if excluded else "NODE",
            "reason": "Navigation/blank separator." if nav else
                      "Retrospective provenance and role boundary, not mathematical inference." if intro else None,
            "node_kind": "process-metadata" if section == "S13" and not excluded else
                         "source-mathematics" if not excluded else "navigation-or-provenance",
            "counts_as_scientific_closure": False if excluded or section == "S13" else
                                           "Only stated mathematical scope; no automatic stronger consumer closure.",
            "source_nodes": [] if excluded else [f"source:{index:03d}"],
            "authority": "AUTHOR_PROVISIONAL",
        })
        offset += len(encoded)
        line += piece.count("\n")
    return result


def binder_audit(root):
    m = ROOT_RE.match(root["exact_lexical_header"])
    tail = root["exact_lexical_header"][m.end():].lstrip()
    groups = []
    while tail and tail[0] in "({[":
        stack, end = [], None
        for index, ch in enumerate(tail):
            if ch in "({[":
                stack.append(ch)
            elif ch in ")}]":
                stack.pop()
                if not stack:
                    end = index+1
                    break
        assert end, root["name"]
        group = tail[:end]
        names = group[1:-1].split(":", 1)[0].split()
        logical = any(re.match(r"^_?h", name) for name in names) or any(
            name in {"branchUnit", "branchClean", "branchNontrivial"} for name in names)
        bundle_names = [name for name in BUNDLE_NAMES if re.search(r"\b"+re.escape(name)+r"\b", group)]
        groups.append({
            "exact_lexical_binder": group, "classification": "SOURCE" if logical else "TYPING",
            "reason": "Explicit premise of this local conditional statement, not a premise of an unconditional user-target theorem."
                      if logical else "Supplied carrier/index/value/object data; recursive logical evidence is expanded below, not erased.",
            "expanded_project_bundles": bundle_names,
            "nested_logical_evidence": "SOURCE within supplied interface; all producer gaps retained." if bundle_names else None,
        })
        tail = tail[end:].lstrip()
    return groups


BUNDLE_NAMES = (
    "LinearDiagonalInputBEContract", "LinearDiagonalRationalCompletion",
    "CubicDiagonalRationalCompletion", "DiagonalRatOperatorNormBridge",
    "CubicDiagonalExactBEContract", "CubicQSVTLocalSideConditions",
    "CubicQSVTExternalSemantics", "StandardRyCleanEntryScalarTier",
    "ExpandedCubicArithmeticBackend", "ExpandedControlledRyWorkspaceReadonlyWitness",
    "ExpandedArithmeticCleanUncomputeWitness", "LinearDiagonalValueBackend",
    "LinearDiagonalValueCleanUncomputeWitness", "ExactCleanBlock", "LCUCertificate",
    "QSVTConsumerContract", "OperatorBlockEncodingCandidate", "VerifiedOperatorBlockEncoding",
)


class ShadowFile:
    def __init__(self, canonical, data):
        self.canonical, self.data = canonical, data
    def resolve(self):
        return self.canonical.resolve()
    def is_file(self):
        return True
    def read_bytes(self):
        return self.data
    def read_text(self, encoding="utf-8"):
        return self.data.decode(encoding)


class OverlayRoot:
    def __init__(self, repo, overlay):
        self.repo, self.overlay = repo, overlay
    def __fspath__(self):
        return str(self.repo)
    def resolve(self):
        return self.repo.resolve()
    def __truediv__(self, name):
        name = str(name)
        return ShadowFile(self.repo/name, self.overlay[name]) if name in self.overlay else self.repo/name


def binding_function(repo):
    relative = "website/scripts/check_research_publications.py"
    raw = (repo/relative).read_bytes()
    namespace = {"__file__": str(repo/relative), "__name__": "author_readonly_binding"}
    exec(compile(raw, namespace["__file__"], "exec"), namespace)
    return namespace["binding_digest"], sha(raw)


def ambient_files(repo):
    return [file_record(path, path.relative_to(repo).as_posix())
            for directory in ("QuantumBlockEncoding", "ABEISTests")
            for path in sorted((repo/directory).rglob("*.lean"))]


def assert_current(repo, pinned):
    for rec in pinned:
        raw = (repo/rec["path"]).read_bytes()
        assert sha(raw) == rec["sha256"] and len(raw) == rec["bytes"], (
            "ENV_STALE_INPUT_STOP_NO_RESEAL", rec["path"])


def graph_views(pars, roots, target, providers):
    nodes = [{"id": p["source_nodes"][0], "kind": p["node_kind"],
              "paragraph_id": p["id"], "source_region": p["source_region"],
              "sha256": p["sha256"], "status": "AUTHOR_PROVISIONAL"}
             for p in pars if p["disposition"] == "NODE"]
    premises = {
        "finite-rational": "N=2^n>0, exact rational finite function matrices, column-vector convention; n=0 permitted, not normalized zero state.",
        "rank-one-contract": "Scaled first column alpha*B[r,0]=a_r AND all other B[r,c]=0 for c!=0, both supplied.",
        "unit-branch": "Every supplied rational branch vector has dot8(v,v)=1 AND v[0]!=1.",
        "branch-value": "Supplied clean coordinate v_s[0]=q_s; q_s!=1 if not derived from a grid range.",
        "four-squares": "For every natural residual, four natural squares sum to it; imported theorem, not complexity theorem.",
        "entry-error": "epsilon>=0 AND every supplied q_j has |q_j-a_j|<=epsilon.",
        "primitive-contract": "Opaque primitive unitarity AND exists block with opaque extraction AND diagonal target entries.",
        "scalar-tier-law": "Supplied carrier/maps/clean-entry range law; descriptions do not enforce actual arccos/cos or injectivity.",
        "known-backend": "Clean-input backend count match AND preserved index AND exact amplitude reader value.",
        "qsvt-supplier": "Certified linear input AND output payload AND actual output orthogonality AND output target X^3 AND supplied global admissibility/cleanup/resource propositions.",
        "expanded-contract": "Transparent compute AND universal scalar-angle bookkeeping AND opaque route cleanup AND opaque extraction AND target equality; no unitarity field.",
    }
    nodes += [{"id": "premise:"+key, "kind": "SOURCE-conditional-interface",
               "formula": value, "not_a_produced_output": True,
               "status": "AUTHOR_PROVISIONAL"} for key, value in premises.items()]
    steps = [
        ("targets", ["premise:finite-rational"], "Distinct O=|v><0|, D=diag(a), X=diag(x), scales N/1.", ["S01"]),
        ("range-norm", ["result:targets"], "0<=x<1, 0<=a<1, sum a^2<=N<=N^2; exact finite diagnostics.", ["S02"]),
        ("threshold", ["result:range-norm"], "j^3<N^3; accepted finite threshold count j^3 and scaled ratio a_j/N=j^3/N^4.", ["S02"]),
        ("rank-one-adapter", ["premise:rank-one-contract","result:targets"], "Split input column zero/nonzero to obtain alpha B=O; premise is not supplied by adapter.", ["S03"]),
        ("label-accounting", [], "Literal 7/10/8 label transcripts/layouts and declared counts; no denotation.", ["S03","S13"]),
        ("reflection", ["premise:unit-branch"], "d=2(1-v0)!=0; H00=v0; exact row AND column orthogonality.", ["S04"]),
        ("fiber", ["premise:finite-rational"], "(b,s)->bN+s with quotient/remainder inverse; filter zero terms, nodup fiber permutation.", ["S05"]),
        ("directsum", ["result:reflection","result:fiber","premise:unit-branch"], "Branchwise rational orthogonality lifts to whole controlled direct sum.", ["S05"]),
        ("clean-diagonal", ["result:reflection","result:fiber","premise:unit-branch","premise:branch-value"], "Clean embedding (0,s) gives diag(q), no circuit/resource link; whole-U orthogonality is separately produced.", ["S05"]),
        ("completion-linear", ["premise:four-squares","result:range-norm"], "Residual N^2-j^2 gives a rational unit family with clean coordinate x.", ["S06"]),
        ("completion-cubic", ["premise:four-squares","result:range-norm"], "Residual N^6-j^6 gives a rational unit family with clean coordinate a.", ["S06"]),
        ("matrix-X", ["result:completion-linear","result:directsum","result:clean-diagonal"], "Existence/chosen exact rational orthogonal X dilation, 8N dimensions, scale1; one label metadata.", ["S06"]),
        ("matrix-D", ["result:completion-cubic","result:directsum","result:clean-diagonal"], "Existence/chosen exact rational orthogonal D dilation; generic payload target separately identified.", ["S06"]),
        ("diagonal-cube", ["result:targets"], "Unique-summand finite diagonal multiplication gives X^3=D; no controlled-direct-sum theorem is required.", ["S07"]),
        ("clean-product", ["result:matrix-X","result:diagonal-cube"], "Three extracted clean matrices multiply to D, not a composed block unitary.", ["S07"]),
        ("qsvt-local", ["result:range-norm"], "P(x)=x^3 is bounded on input grid; degree/parity labels do not certify phase synthesis.", ["S07"]),
        ("qsvt-consumer", ["result:diagonal-cube","result:qsvt-local","premise:qsvt-supplier"], "Identify supplied transformed output with D and package generic consumer.", ["S07"]),
        ("euclidean-error", ["premise:entry-error","result:targets"], "Diagonal action collapses to one term; squared scalar inequality summed gives rational all-vector Euclidean bound.", ["S08"]),
        ("circle-branch", ["premise:branch-value","premise:unit-branch","result:clean-diagonal"], "For q^2+r^2=1 and q!=1, supplied (q,r,0...) gives diag(q) clean block.", ["S08"]),
        ("primitive-adapter", ["premise:primitive-contract","result:targets"], "Extract supplied opaque unitary/block evidence; conditional verified-candidate packaging only.", ["S09"]),
        ("scalar-specialization", ["premise:scalar-tier-law","result:range-norm"], "Range law applies to a_j; universal transparent angle statement is bookkeeping, not a backend.", ["S10"]),
        ("fixed-payload", ["result:threshold"], "Finite 3n-bit payload j^3, reader w/2^(3n), clean-input overwrite computes a_j; not invertible.", ["S10"]),
        ("bridge-normal-form", ["premise:known-backend"], "Known premise -> opaque arithmetic route is equivalent to opaque route; not its witness.", ["S10"]),
        ("modular-cleanup", ["result:fixed-payload"], "Add payload modulo M and subtract payload modulo M; dirty workspace restored after compute; same linear-value route uses j,N.", ["S11"]),
        ("readonly-interface", [], "Only j/workspace preservation of a basis signal function is specified; no Ry action or existence theorem supplied.", ["S11"]),
        ("expanded-adapter", ["premise:expanded-contract","result:targets"], "Extract target equality already present in conjunction; no unitarity conclusion.", ["S12"]),
    ]
    edges = []
    for key, tails, formula, sections in steps:
        nid = "result:"+key
        nodes.append({"id": nid, "kind": "source-construction-step",
                      "formula": formula, "source_regions": sections,
                      "source_paragraphs": [p["id"] for p in pars if p["disposition"]=="NODE" and p["source_region"] in sections],
                      "status": "AUTHOR_PROVISIONAL_NOT_BUILD_EVIDENCE"})
        edges.append({"id": "construction:"+key, "logic": "AND", "tails": tails, "heads": [nid],
                      "status": "AUTHOR_PROVISIONAL", "scope": "All stated premises needed for this conditional interface; no consumer is silently completed.",
                      "empty_tail_meaning": "Literal definition/accounting/interface data, not physical existence." if not tails else None})
    gaps = {
        "NORMALIZED-SP": "Nonzero norm, first-column normalized state theorem, accepted probability and amplification costs; n=0 zero excluded.",
        "RANK-ONE-DENOTATION": "Actual coherent arithmetic/counting/Hadamard/reject/cleanup semantics and unitary clean-block root.",
        "FOUR-SQUARE-PRODUCER": "Uniform deterministic witness production, classical time/storage and precision/cost contract; choice is not an algorithm.",
        "CONTROLLED-GATE-SYNTHESIS": "Uniform controlled 8D matrices compiled with all logical gates, depth, ancillas, bit precision and no hidden table oracle.",
        "PRODUCT-PHYSICAL": "Actual unitary product construction with isolated clean intermediates, cleanup and denotation/resource theorem.",
        "QSVT-SUPPLY": "Real phase synthesis/global admissibility, certified transformed circuit and exact/finite-bit error/cost.",
        "APPROX-PRODUCER": "Choose q, prove entrywise epsilon, connect to complex/real physical norm if required and implement its dilation.",
        "COMMON-BACKEND-COMPOSITION": "Actual coherent rotation and same backend compute/readonly/uncompute composition; generic basis function insufficient.",
        "OPAQUE-CLEANUP-EXTRACTION": "Bridge transparent modular cleanup to actual route semantics and prove extraction AND unitarity; never assume target as closure.",
        "FAMILY-EXECUTABLE": "Independent uniformly reproducible executable family acceptance; finite diagnostics not symbolic certificate.",
    }
    gapids = ["SOURCE_GAP-"+key for key in gaps]
    nodes += [{"id": "SOURCE_GAP-"+key, "kind": "SOURCE_GAP", "formula": value,
               "status": "OPEN_STRONGER_CONSUMER_NOT_REFUTATION"} for key, value in gaps.items()]
    guards = [
        {"id":"rank-one-column","guards":["column=0","column!=0"],"routes":["first-column clause","all-other-columns-zero clause"],"both_branches_audited":True},
        {"id":"Householder-validity","guards":["dot(v,v)=1 AND v0!=1","outside this locus"],"routes":["reflection/clean-entry theorem","total Rat formula only; no reflection claim"]},
        {"id":"directsum-system","guards":["decoded systems equal","decoded systems unequal"],"routes":["same-branch fiber sum","every product term zero"]},
        {"id":"fiber-membership","guards":["decoded system=s","decoded system!=s"],"routes":["one of eight distinct product indices","discard only proved-zero summand"]},
        {"id":"four-square-target","guards":["linear X","cubic D"],"routes":["N^2-j^2 residual","N^6-j^6 residual"],"not_same_target_OR":True},
        {"id":"modular-wrap","guards":["w+p<M","M<=w+p<2M"],"routes":["no inner wrap","one inner wrap"],"range_guards":["w<M","p<M"]},
        {"id":"empty-cases","guards":["n=0","general vector dimension=0"],"routes":["N=M=1 and p=w=0; normalized v undefined","empty sums, epsilon>=0 still required"]},
        {"id":"physical-D-alternatives","guards":["chosen Householder gate compiler","expanded arithmetic rotation","external QSVT supplier"],"routes":["matrix existence + producer/synthesis gaps","actual common backend + cleanup/extraction/unitary gaps","all supplied global/phase/cost obligations"],"all_routes_physical_OPEN":True},
    ]
    for item in guards:
        item.update(join="OR", status="AUTHOR_PROVISIONAL", meaning="Guarded case or alternative route; do not split an AND tail into sufficient arrows.")
    transports = [
        ("rational-branch-to-diagonal", ["result:reflection","result:fiber","premise:unit-branch","premise:branch-value"], ["result:clean-diagonal"],
         "Orthogonal supplied branch -> direct-sum diagonal clean matrix.",
         "Exact branch unit/coordinate/nontrivial guards and ancilla-high flattening.",
         "No deterministic branch producer, finite-bit gate compiler or one-signal identification."),
        ("linear-to-cubic-algebra", ["result:matrix-X","result:diagonal-cube"], ["result:clean-product"],
         "Three already extracted clean matrices -> cubic diagonal target.",
         "Same rational carrier, scale1, actual diagonal X and finite-sum product.",
         "Not U^3 and not the physical product-block theorem."),
        ("entry-to-rational-euclidean", ["premise:entry-error","result:targets"], ["result:euclidean-error"],
         "Uniform scalar diagonal errors -> all-rational-vector squared Euclidean action bound.",
         "Diagonality AND nonnegative epsilon AND every actual entry bound.",
         "No chosen approximation algorithm or real/complex scalar-extension/hardware error theorem."),
        ("finite-value-to-cleanup", ["result:fixed-payload"], ["result:modular-cleanup"],
         "Finite payload fits M -> modular clean compute/uncompute witness.",
         "Same fixed index and payload, correct finite ranges and modular inverse direction.",
         "No opaque route bridge, amplitude rotation, multiplication circuit or charged gate costs."),
    ]
    return {"status":"AUTHOR_PROVISIONAL_NOT_INDEPENDENT_TOPOLOGY", "views":{
        "source-construction-graph":{"nodes":nodes,"AND_hyperedges":edges,"guarded_OR_cases":guards,"open_source_gap_ids":gapids,
            "independence":"Author reconstruction of already frozen source only; fresh independent topology still required.",
            "scope":"Existing source mathematical claims/interfaces, not compile acceptance or whole scientific root.",
            "proof_ingredient_policy":"Premises shown only on local conditional interfaces; final user-target consumers may not inherit convenient proof ingredients as SOURCE binders.",
            "constructor_local_discharge":[
                {"consumer":"result:matrix-X","produced_by":["result:completion-linear","result:range-norm"],
                 "discharges":["premise:unit-branch","premise:branch-value"],
                 "reason":"Four squares supplies unit norm and coordinate x; x<1 supplies v0!=1. No branch oracle added to user theorem."},
                {"consumer":"result:matrix-D","produced_by":["result:completion-cubic","result:range-norm"],
                 "discharges":["premise:unit-branch","premise:branch-value"],
                 "reason":"Four squares supplies unit norm and coordinate a; a<1 supplies v0!=1. No branch oracle added to user theorem."},
                {"consumer":"result:scalar-specialization","produced_by":["result:range-norm"],
                 "discharges":["the cubic amplitude lies in the supplied tier law's [0,1] domain"],
                 "reason":"A scalar range law remains supplied interface evidence; it does not become a physical Ry witness."}]},
        "lean-graph":{"status":"ACTUAL_IMPORT_AND_LEXICAL_OWNERSHIP_ONLY",
            "target_import_edges":[{"from":"module:"+TARGET[:-5].replace("/","."),"to":"module:"+i,"kind":"actual-module-import"} for i in target["imports"]],
            "provider_import_edges":[{"from":"module:"+p["path"][:-5].replace("/","."),"to":"module:"+i,"kind":"actual-module-import"} for p in providers for i in p["imports"]],
            "ownership_edges":[{"from":"module:"+r["module"][:-5].replace("/","."),"to":("private-helper:" if r["private"] else "declaration:")+r["name"],
                               "kind":"private-source-helper-owner" if r["private"] else "public-source-owner"} for r in roots],
            "elaborated_theorem_dependencies":[],"private_source_helpers":50,
            "not_claimed":"Imports do not give each theorem every imported proof dependency; no elaborated types or trust audit."},
        "compressed-quantum-spine":{"status":"AUTHOR_NAVIGATION_PENDING_PURIFICATION","groups":[
            {"id":"concept:cubic-target-and-scaling","expands_to":["result:targets","result:range-norm","result:threshold","result:rank-one-adapter"]},
            {"id":"concept:rational-branch-dilation","expands_to":["result:reflection","result:fiber","result:directsum","result:completion-linear","result:completion-cubic","result:matrix-X","result:matrix-D"]},
            {"id":"concept:polynomial-clean-matrix-consumer","expands_to":["result:diagonal-cube","result:clean-product","result:qsvt-consumer"]},
            {"id":"concept:diagonal-error-transfer","expands_to":["result:euclidean-error","result:circle-branch"]},
            {"id":"concept:finite-payload-reversible-lift","expands_to":["result:fixed-payload","result:modular-cleanup","result:bridge-normal-form","result:expanded-adapter"]}],
            "lossless_drilldown":[PREFIX+"author-source-coverage.json",PREFIX+"author-formal-context.json"],
            "process_metadata":"S13 retained but excluded from scientific closure.","purification":"PENDING","Exposition_Seal":"PENDING"},
        "functor-hypergraph":{"status":"AUTHOR_CONCEPTUAL_NOT_CERTIFIED_FUNCTOR","certified_transport":False,
            "hyperedges":[{"id":"transport:"+key,"logic":"AND","tails":tails,"heads":heads,"formula":formula,
                           "hypothesis_map":hyp,"conclusion_map":"Exactly named output and its stated evidence layer, not stronger physical consumers.",
                           "failure_boundary":failure,"source":LESSON,"candidate_Lean_substrate":TARGET,
                           "independent_review":"PENDING"} for key,tails,heads,formula,hyp,failure in transports],
            "not_claimed":"No categorical identity/composition certificate or automatic theorem edge."}}}


def bundle_record(relative, root, input_hash):
    body = root["clean_definition_body"]
    fields = []
    if root["kind"] == "structure":
        matches = list(re.finditer(r"^  (?P<name>[A-Za-z_][\w']*)\s*:", body, re.M))
        for index, match in enumerate(matches):
            end = matches[index+1].start() if index+1 < len(matches) else len(body)
            exact = body[match.start():end].strip()
            field = match["name"]
            logical = (
                field.endswith(("Proof", "Proofs", "_proof")) or field in {
                    "unitaryProof","cleanBlockProof","normalizerProof","boundedOnInputSpectrum",
                    "outputUnitary","outputIsCubicTransform","degree_eq","oddParity_eq",
                    "cleanEntry_of_range","workspaceQubitCount_eq","computes",
                    "preserves_index","preserves_workspace","computeStep_matches_backend_on_clean",
                    "compute_preserves_index","uncompute_preserves_index","uncompute_after_compute",
                    "diagonal_entrywise_error_operatorNorm_le","blockProof","layoutMatches",
                })
            fields.append({"name":field,"exact_source_field_region":exact,
                           "classification":"SOURCE" if logical else "TYPING",
                           "reason":"Stored law/equality/proof of this supplied local contract, not an automatic produced physical result."
                                    if logical else "Data, proposition/relation parameter, text or arbitrary function; recursive supplied payload evidence stays explicit."})
    return {"name":root["name"],"provider_path":relative,"provider_sha256":input_hash,
            "exact_lexical_header":root["exact_lexical_header"],
            "exact_definition_region":root["source_block"],
            "field_audit":fields,"not_elaborated":True,
            "authority":"AUTHOR_PROVISIONAL_LOCAL_INTERFACE_EXPANSION"}


def build(repo, out):
    assert out.is_dir()
    original_records = [file_record(out/name,name) for name in ORIGINAL]
    assert all(rec["sha256"]==ORIGINAL[rec["path"]] for rec in original_records)
    source = (out/"source-only.md").read_bytes()
    source_sections = paragraphs(source)
    frozen_map = private_map(out)
    before_ambient = ambient_files(repo)
    assert len(before_ambient)==202, ("ambient file set changed; stop",len(before_ambient))
    config = [file_record(repo/p,p,True) for p in ("lean-toolchain","lake-manifest.json","lakefile.lean")]
    target = file_record(repo/TARGET,TARGET,True)
    assert target["sha256"]==TARGET_SHA
    target["imports"] = imports((repo/TARGET).read_text(encoding="utf-8"))
    roots = inventory(TARGET,(repo/TARGET).read_bytes())
    assert len(roots)==319 and len({r["name"] for r in roots})==319
    assert sum(not r["private"] for r in roots)==269 and sum(r["private"] for r in roots)==50
    assert sum(r["kind"]=="structure" for r in roots)==11
    assert set(frozen_map)=={r["name"] for r in roots}
    providers, queue = {}, list(target["imports"])
    while queue:
        imp = queue.pop()
        if not imp.startswith("QuantumBlockEncoding."):
            continue
        path = imp.replace(".","/")+".lean"
        if path==TARGET or path in providers:
            continue
        rec = file_record(repo/path,path)
        rec["imports"] = imports((repo/path).read_text(encoding="utf-8"))
        rec["read_permission"] = "Exact source under recorded hash, no whole-provider review credit."
        providers[path] = rec
        queue += rec["imports"]
    assert len(providers)==5, providers.keys()
    external = file_record(repo/".lake/packages/mathlib/Mathlib/NumberTheory/SumFourSquares.lean",
                           ".lake/packages/mathlib/Mathlib/NumberTheory/SumFourSquares.lean")
    external["purpose"] = "Direct imported theorem source hash, not a transitive Mathlib proof review or build certificate."
    checker_path = "website/scripts/check_research_publications.py"
    checker_before = file_record(repo/checker_path,checker_path)
    binding_digest, checker_hash = binding_function(repo)
    assert checker_hash==checker_before["sha256"]
    catalog_raw = (repo/"website/research/sources.json").read_bytes()
    registry_raw = (repo/"website/research/publications.json").read_bytes()
    registry_count = len(json.loads(registry_raw)["records"])
    strict_inputs = before_ambient + [{k:v for k,v in c.items() if k in ("path","sha256","bytes")} for c in config] + [external,checker_before]
    assert_current(repo,strict_inputs)
    masked = mask_comments((repo/TARGET).read_text(encoding="utf-8"))
    ambient = {"module":TARGET,"commands":[{"line":n+1,"exact_text":line}
               for n,line in enumerate(masked.splitlines()) if re.match(
                   r"^(?:import |namespace |end\b|open |section\b|noncomputable section|set_option |variable |universe |scoped |local |notation |attribute )",line)],
               "private_named_roots":[r["name"] for r in roots if r["private"]],
               "explicit_instances":[],"target_global_variables":[],"target_local_notation":[],
               "full_source_bytes_retained":True,"implicit_policy":"Generic helper universes/autoimplicit finite infrastructure are lexical only; actual elaborated binders need decoder compilation.",
               "zero_division_boundary":"Rat total division; reflection theorem explicitly guarded; finite grid always nonzero."}
    formal_inventory = [{k:v for k,v in r.items() if k not in ("source_block","clean_definition_body","exact_lexical_header")} for r in roots]
    formal = {"status":"FORMAL_ONLY_INPUT_NO_ACCEPTANCE","target_files":[target],
              "inventory":formal_inventory,"inventory_count":319,"public_inventory_count":269,"private_target_helper_count":50,
              "public_roots_per_module":{"CubicStatePreparation":269},"ambient_scope":[ambient],
              "provider_index":[providers[p] for p in sorted(providers)],"external_direct_import_index":[external],
              "dependency_context":config,
              "type_authority":"Lossless raw source lines/base64 and lexical whole-module inventory, not elaborated types, axioms or Lean success.",
              "fixed_read_boundary":{"targets":"Exactly one complete source module, all ambient bytes, 269 explicit public plus50 private source roots including opaque contracts.",
                  "providers":"Exact five-module local import closure by path/hash/imports; inspect necessary source under those hashes.",
                  "external":"Direct external source hash plus pinned toolchain/manifest; no floating retrieval or unsupported provider admission.",
                  "not_claimed":"No desired natural conclusion, author source alignment, graph, prior decoder/reviewer or success verdict supplied."}}
    emit(out,"author-formal-context.json",formal)
    context_hash = sha((out/"author-formal-context.json").read_bytes())
    packet = {"status":"FORMAL_ONLY_INPUT_NO_ACCEPTANCE","formal_context_path":PREFIX+"author-formal-context.json",
              "formal_context_sha256":context_hash,"opaque_context_binding_sha256":context_hash,
              "target_modules":[TARGET],"inventory_count":319,"public_count":269,"private_count":50,
              "required_work":"Decode all complete target source and ambient context, inspect necessary provider definitions, reconstruct every authored public/private root and real proposition/metadata boundaries. Lexical names are not final checked types.",
              "fixed_read_boundary":formal["fixed_read_boundary"],
              "publication_binding_state":"LATE_BRIDGE_REQUIRED_AFTER_INDEPENDENT_FORMAL_RECONSTRUCTION_FREEZE",
              "withheld":"Natural source/lesson/source-row/assumption map, author coverage/topology, old or fresh independent reconstructions and verdicts."}
    emit(out,"author-decoder-packet.json",packet)
    emit_raw(out,"cubic-grid-rational-operators-and-contracts.md",source)
    obligations = []
    representative_defs = {"linearDiagonalHouseholderInputBEContract","cubicDiagonalHouseholderExactBEContract","linearDiagonalCubicProductCertificate"}
    for index,root in enumerate(roots,1):
        mapping = frozen_map[root["name"]]
        normalized_header = re.sub(r"\s+"," ",root["exact_lexical_header"]).replace("|","&#124;")
        assert normalized_header==mapping["frozen_exact_header"], (root["name"],"frozen header mismatch")
        source_region = mapping["source_region"]
        binder = binder_audit(root)
        kind = ("theorem-not-definition" if root["kind"] in ("theorem","lemma") else
                "opaque-unspecified" if root["kind"]=="opaque" else
                "quotient/representative" if root["lexical_local_name"] in representative_defs else "literal")
        obligations.append({
            "id":f"C29-{index:03d}","name":root["name"],"module":TARGET,"line":root["line"],
            "kind":root["kind"],"private":root["private"],"status":WIP,"source_region":source_region,
            "source_paragraphs":[p["id"] for p in source_sections if p["disposition"]=="NODE" and p["source_region"]==source_region],
            "source_obligation":"Frozen natural "+source_region+"; exact local conditional statement/body and complete private table row "+str(mapping["ordinal"]),
            "source_role":"historical-process-metadata-excluded-from-scientific-closure" if source_region=="S13" else
                          "local-mathematical-proof-edge" if root["kind"] in ("theorem","lemma") else "literal-or-conditional-interface",
            "binder_audit":binder,"logical_inputs":[b for b in binder if b["classification"]=="SOURCE"],
            "lexical_header_for_audit_only":root["exact_lexical_header"],
            "output_logic":"Every conjunction conclusion and both iff directions remain outputs, not inserted proof premises.",
            "definition_audit":{"kind":kind,"noncomputable":root["noncomputable"],
                "representative_semantics":"A selected noncanonical branch family from an existence proof; clean target independent of choice, no uniqueness or efficient algorithm." if kind=="quotient/representative" else None,
                "opaque_boundary":"Unspecified matrix/predicate, no physical semantics or proof supplied by name." if kind=="opaque-unspecified" else None,
                "expanded_structure_members":root["clean_definition_body"] if root["kind"]=="structure" else None,
                "literal_scope_guard":"Total Rat formula; reflection valid only under unit and v0!=1." if root["lexical_local_name"]=="householder8" else None},
            "proof_region_sha256":root["source_block_sha256"],"author_only":True})
    bundles = {}
    for root in roots:
        if root["kind"]=="structure" or (root["kind"]=="def" and
            any(name==root["lexical_local_name"] for name in BUNDLE_NAMES)) or (
            root["kind"]=="def" and re.search(r":\s*Prop\s*$",root["exact_lexical_header"])):
            bundles[root["name"]] = bundle_record(TARGET,root,TARGET_SHA)
    provider_specs = {
        "QuantumBlockEncoding/BlockEncodingClassics.lean":["ExactCleanBlock","LCUCertificate","QSVTConsumerContract","IsRationalOrthogonal","cleanBlockBy","productIndex"],
        "QuantumBlockEncoding/BlockEncoding.lean":["RegisterLayout","BlockEncodingCost","QueryOperatorTarget","OperatorBlockEncodingCandidate","VerifiedOperatorBlockEncoding","ConstructionClaim"],
        "QuantumBlockEncoding/Resources.lean":["Resource","CostExpr"],
    }
    for relative,names in provider_specs.items():
        own = inventory(relative,(repo/relative).read_bytes())
        for name in names:
            found = [r for r in own if r["lexical_local_name"]==name]
            assert len(found)==1, (relative,name)
            bundles[found[0]["name"]] = bundle_record(relative,found[0],providers[relative]["sha256"])
    private_text = (out/"author-private-coverage.md").read_text(encoding="utf-8")
    manual_audit = private_text.split("## Definition audit and expanded bundled contracts\n",1)[1].split("## Source proof topology",1)[0]
    graph = graph_views(source_sections,roots,target,list(providers.values()))
    gapids = graph["views"]["source-construction-graph"]["open_source_gap_ids"]
    coverage = {"status":WIP,"role":"AUTHOR_CURATOR_NOT_INDEPENDENT_REVIEWER","source_path":LESSON,
                "source_sha256":ORIGINAL["source-only.md"],"source_bytes":len(source),"source_paragraphs":source_sections,
                "reconstruction":"Concatenate exact_text without separators for every source byte including final newline.",
                "whole_module_inventory":obligations,"public_target_roots":269,"private_target_helpers":50,
                "explicit_structure_count":11,"ambient_scope":[ambient],"full_formal_context_sha256":context_hash,
                "project_owned_bundle_expansions":bundles,"frozen_manual_nested_contract_audit":manual_audit,
                "logical_input_policy":"SOURCE applies only to premises of stated local conditional interfaces. They are not automatically source premises of final unconditional user-target constructions. TYPING outer objects retain nested SOURCE evidence.",
                "definition_policy":"Literal formulas/contract aliases retain full carrier scope; opaque predicates remain unspecified. Selected Householder representatives are nonunique, not characterized-unique and not efficient algorithms.",
                "generated_declarations":"Structure fields/constructors preserved in full source; compiler recursors/equation auxiliaries excluded as infrastructure, no elaborated inventory claim.",
                "topology_authority":"AUTHOR_PROVISIONAL_NOT_INDEPENDENT","open_source_gap_ids":gapids,"remaining_boundary":RESIDUAL}
    emit(out,"author-source-coverage.json",coverage)
    emit(out,"author-binder-definition-audit.json",{
        "status":WIP,"whole_module_inventory":[{k:v for k,v in o.items() if k in ("id","name","private","binder_audit","definition_audit","lexical_header_for_audit_only")} for o in obligations],
        "project_owned_bundle_expansions":bundles,"frozen_manual_nested_contract_audit":manual_audit,
        "classification_authority":"AUTHOR_PROVISIONAL; no human-approved correction or unconditional target theorem claimed.",
        "original_private_coverage_unchanged":True,
        "same_source_vs_stronger_consumer":"Conditional contract premises are not promoted to an unconditional O/D physical target; opaque success predicates never manufacture mathematical closure."})
    graph["coverage_sha256"] = sha((out/"author-source-coverage.json").read_bytes())
    emit(out,"author-graph-views.json",graph)
    source_row = {
        "id":SOURCE_ID,"title":"Cubic grid rational operators, branch dilations and conditional circuit contracts",
        "authors":"Historical formalizer UNKNOWN; retrospective local AUTHOR-curator cubic-source-author-c29",
        "url":"https://github.com/DakeBU/Quantum-Computing-Block-Encoding","year":2026,
        "status":"primary-text-checked",
        "anchor":LESSON+" sections S01–S13; immutable UTF-8 SHA256 "+ORIGINAL["source-only.md"],
        "scope":"One complete actual legacy module, 269 public plus50 private authored lexical roots and11 explicit structures. Distinct rank-one/diagonal targets, exact rational matrix existence, conditional supplied contracts, finite arithmetic/error and label accounting boundaries.",
        "formal_status":"AUTHOR/WIP retrospective source only; no independent acceptance, historical formalizer identity, pre-proof provenance, novelty, fresh compile, main admission or PURIFIED claim.",
    }
    emit(out,"author-source-row-candidate.json",{"status":WIP,"source":source_row,
        "immutability":"Prospective source-row only; parent must retain exact row once binding frozen. Other catalog rows are not rewritten."})
    catalog = json.loads(catalog_raw)
    assert not any(s["id"]==SOURCE_ID for s in catalog["sources"]), "Source ID already exists: stop, do not replace."
    catalog["sources"].append(source_row)
    overlay = OverlayRoot(repo,{LESSON:source,"website/research/sources.json":json.dumps(catalog,ensure_ascii=False).encode()})
    public = [o for o in obligations if not o["private"]]
    contribution = {
        "baseline":BASE,"head":HEAD,"head_provenance":"Parent-supplied contextual reference only; author did not execute Git.",
        "classes":["reorganisation","bridge"],
        "node_ids":["module:QuantumBlockEncoding.CubicStatePreparation"]+
                   ["declaration:"+o["name"] for o in public]+
                   ["private-helper:"+o["name"] for o in obligations if o["private"]]+gapids,
        "views":["source-construction-graph","lean-graph","compressed-quantum-spine","functor-hypergraph"],
        "source_graph_sha256":sha((out/"author-graph-views.json").read_bytes()),
        "coverage_sha256":sha((out/"author-source-coverage.json").read_bytes()),
        "formal_context_sha256":context_hash,
        "formal_packet_sha256":sha((out/"author-decoder-packet.json").read_bytes()),
        "source_graph_authority":"AUTHOR_PROVISIONAL_NOT_INDEPENDENT",
        "preserved_contract":"Whole target source, all ambient source inputs and trusted runtime unchanged; source recovery/metadata only, no new theorem or canonical admission.",
        "remaining_boundary":RESIDUAL,
    }
    candidate = {
        "module":TARGET,"source_id":SOURCE_ID,
        "source_statement":"Frozen retrospective local source S01–S13, exact rational rank-one O/diagonal D/linear X and guarded eight-dimensional Householder/direct-sum construction, supplied interfaces, finite error and arithmetic. Whole 269 public and50 private source inventory with all source/definition/binder/metadata boundaries retained.",
        "source_anchor":LESSON+" sections S01–S13",
        "lesson_path":LESSON,"declarations":[o["name"] for o in public],
        "obligation_map":[{"kind":"proof-edge" if o["kind"] in ("theorem","lemma") else "prerequisite",
                           "source_obligation":o["id"],"declarations":[o["name"]]} for o in public],
        "assumption_deltas":[
            {"classification":"same",
             "source":"Distinct O,D,X, exact Rat finite sums, scales N/1, literal branch unit/coordinate/nontrivial guards, local conditional supplier laws and complete unknown consumer gaps.",
             "formal":"Every explicit public/private source header and recursive contract field retained. Primitive opaque predicates, arbitrary cleanup/resource propositions and unconstrained generic payload target are not strengthened.",
             "explanation":"The retrospective source states the actual conditional mathematics; proof ingredients are not assumed for unconditional user-target closure."},
            {"classification":"source-implicit",
             "source":"n>=0 extension including N=1, ancilla-high/system-low b*N+s flattening, total rational division with stated reflection guard, noncanonical residual-square choice.",
             "formal":"Finite range proof arguments, ambient definitions, full local import closure and exact selected formulas remain unchanged.",
             "explanation":"Positive-n task prose does not hide the actual n=0 carrier; zero vector is not normalized. No uniqueness, finite-bit producer, gate count, arbitrary phase quotient or physical denotation is inferred."},
            {"classification":"same",
             "source":"Process schedule/error-ladder and transcript/resource descriptions are retained as metadata, excluded from scientific success.",
             "formal":"Actual 3-rung ladder and literal 7/10/8/1 oracle-label counts are preserved, not silently replaced by historical task prose.",
             "explanation":"Label resource equalities and algebraic clean-matrix products do not become controller efficacy or gate-expanded implementation certificates."},
        ],
        "graph_contribution":contribution,
        "formalizer":"cubic-source-author-c29 retrospective AUTHOR-curator; historical formalizer UNKNOWN",
        "historical_formalizer":"UNKNOWN","residual_boundary":RESIDUAL,
        "decoder_evidence":PREFIX+"decoder-pending/CubicStatePreparation-evidence.json",
        "reviewer_evidence":PREFIX+"reviewer-pending/CubicStatePreparation-evidence.json",
        "evidence_paths_status":{"decoder":"UNATTACHED_NOT_INSPECTED_NO_AUTHORED_EVIDENCE",
                                 "reviewer":"UNATTACHED_NOT_INSPECTED_NO_AUTHORED_EVIDENCE"},
        "status":WIP,
        "statement_seal":{"timing":"RETROSPECTIVE_LOCAL_AFTER_PREEXISTING_PROOFS","pre_proof_seal_claim":False},
        "source_proof_coverage":PREFIX+"author-source-coverage.json",
        "binder_definition_audit":PREFIX+"author-binder-definition-audit.json",
        "graph_views":PREFIX+"author-graph-views.json",
        "formal_context":PREFIX+"author-formal-context.json",
        "formal_packet":PREFIX+"author-decoder-packet.json",
        "purification":{"status":"PENDING","Exposition_Seal":"PENDING"},
        "independent_acceptance":False,"main_admission":False,"scientific_ROOT":False,
    }
    assert_current(repo,strict_inputs)
    candidate["binding_sha256"] = binding_digest(overlay,candidate)
    emit(out,"publication-candidate-CubicStatePreparation.json",candidate)
    emit(out,"author-binding-bridge-proposal.json",{
        "status":WIP,"formal_context_sha256":context_hash,
        "formal_packet_sha256":sha((out/"author-decoder-packet.json").read_bytes()),
        "bindings":[{"module":TARGET,"binding_sha256":candidate["binding_sha256"]}],
        "procedure":"Only after independently frozen formal-only reconstruction may parent compare actual target/provider/config scope and add a later opaque bridge. Author reads no independent result and supplies no acceptance.",
        "independent_input_binding_inspected":False,"decoder_reconstruction_inspected":False,
        "reviewer_result_inspected":False,"accepted":False})
    emit(out,"formal-input-seal.json",{
        "status":"FORMAL_ONLY_FROZEN_NOT_ACCEPTANCE","formal_context_sha256":context_hash,
        "formal_packet_sha256":sha((out/"author-decoder-packet.json").read_bytes()),
        "target_bindings":[{k:target[k] for k in ("path","sha256","bytes")}],
        "provider_index_sha256":sha(json.dumps(formal["provider_index"],sort_keys=True,ensure_ascii=False).encode()),
        "external_direct_import_index":formal["external_direct_import_index"],
        "dependency_context":[{k:c[k] for k in ("path","sha256","bytes")} for c in config],
        "public_roots":269,"private_helpers":50,"structures":11,
        "note":"Formal-only input seal, no source identity/alignment/desired outcome or independent verdict."})
    assert_current(repo,strict_inputs)
    assert sha((repo/"website/research/sources.json").read_bytes())==sha(catalog_raw), "Source catalog changed: stop before freeze."
    names = sorted(p.name for p in out.iterdir() if p.is_file() and p.name not in ORIGINAL)
    emit(out,"metadata-freeze.json",{
        "status":WIP,"head":HEAD,"base":BASE,
        "original_immutable_inputs":original_records,
        "new_artifacts":[file_record(out/name,name) for name in names],
        "whole_ambient_binding_inputs":before_ambient,
        "strict_config_and_direct_external_inputs":strict_inputs[len(before_ambient):],
        "checker_path":checker_path,"checker_sha256":checker_hash,
        "binding_recipe":{"function":"binding_digest","function_unchanged":True,
            "fields":["module","source_id","source_statement","source_anchor","lesson_path","declarations",
                      "obligation_map","assumption_deltas","graph_contribution","formalizer","residual_boundary"],
            "virtual_data_overlay":[LESSON,"website/research/sources.json"],
            "method":"Unchanged binding_digest on prospective data-only source-row/lesson overlay; validate_record/check/main never called."},
        "registry_observed_count":registry_count,"registry_sha256":sha(registry_raw),
        "original_source_catalog_sha256":sha(catalog_raw),
        "format_reference":{"path":"primitive-semantics-author-c28/author-package-build.py",
                            "use":"Mechanical formats/overlay serialization only; no independent c28/c29 decoder/reviewer input or result read."},
        "source_inventory":"319 exact case-sensitive source names;269 public catalog roots and50 private helpers,11 structures.",
        "emission":"New C-owned files only through bounded apply_patch; old source trio never overwritten.",
        "all_artifacts_WIP":True,"independent_evidence_fabricated":False,"production_writes":False,
        "Lean_executed":False,"Git_executed":False,"acceptance":False,"freeze_self_hash_excluded":True})
    report = verify(repo,out,manifest=False)
    emit(out,"mechanical-selftest.json",report)
    names = sorted(p.name for p in out.iterdir() if p.is_file())
    records = []
    for name in names:
        rec = file_record(out/name,name)
        rec["planned_canonical_path"] = LESSON if name=="cubic-grid-rational-operators-and-contracts.md" else PREFIX+name
        records.append(rec)
    emit(out,"outputs-manifest.json",{
        "status":WIP,"artifacts":records,"mechanical_selftest":report,
        "manifest_self_hash_excluded":True,"planned_prefix":PREFIX,"lesson_path":LESSON,
        "all_output_paths_relative":True,"independent_acceptance":False,"main_admission":False,"scientific_ROOT":False,
        "recovery":"Raw artifacts and immutable source trio remain. Concatenated source paragraphs and formal raw lines/base64 recover exact inputs. Existing partial output is never replaced on replay."})
    print(json.dumps(verify(repo,out,manifest=True),ensure_ascii=False,indent=2))


def verify(repo, out, manifest=True):
    load = lambda name: json.loads((out/name).read_bytes())
    frozen = load("metadata-freeze.json")
    for rec in frozen["original_immutable_inputs"]+frozen["new_artifacts"]:
        raw = (out/rec["path"]).read_bytes()
        assert sha(raw)==rec["sha256"] and len(raw)==rec["bytes"], rec["path"]
    assert_current(repo,frozen["whole_ambient_binding_inputs"]+frozen["strict_config_and_direct_external_inputs"])
    formal,packet=load("author-formal-context.json"),load("author-decoder-packet.json")
    context_hash=sha((out/"author-formal-context.json").read_bytes())
    assert context_hash==packet["formal_context_sha256"]
    for rec in formal["target_files"]+formal["dependency_context"]:
        raw = base64.b64decode("".join(rec["full_source_utf8_base64_chunks"]))
        assert raw=="".join(rec["full_source_lines"]).encode()==(repo/rec["path"]).read_bytes()
        assert sha(raw)==rec["sha256"] and len(raw)==rec["bytes"]
    providers={p["path"]:p for p in formal["provider_index"]}
    for rec in formal["target_files"]+formal["provider_index"]:
        raw=(repo/rec["path"]).read_bytes()
        assert sha(raw)==rec["sha256"] and imports(raw.decode())==rec["imports"]
        for imp in rec["imports"]:
            if imp.startswith("QuantumBlockEncoding."):
                assert imp.replace(".","/")+".lean" in set(providers)|{TARGET}
    roots=formal["inventory"]
    assert len(roots)==319 and len({r["name"] for r in roots})==319
    assert sum(not r["private"] for r in roots)==269 and sum(r["private"] for r in roots)==50
    assert sum(r["kind"]=="structure" for r in roots)==11 and sum(r["kind"]=="opaque" for r in roots)==7
    cov=load("author-source-coverage.json")
    source=(out/"source-only.md").read_bytes()
    assert source==(out/"cubic-grid-rational-operators-and-contracts.md").read_bytes()
    assert sha(source)==ORIGINAL["source-only.md"]
    assert "".join(p["exact_text"] for p in cov["source_paragraphs"]).encode()==source
    for p in cov["source_paragraphs"]:
        assert source[p["start_utf8_byte"]:p["end_utf8_byte"]]==p["exact_text"].encode()
        assert sha(p["exact_text"].encode())==p["sha256"]
        assert p["disposition"] in ("NODE","EXCLUDED") and (p["source_nodes"] or p["reason"])
        if p["source_region"]=="S13":
            assert p["counts_as_scientific_closure"] is False
    obligations=cov["whole_module_inventory"]
    assert {o["name"] for o in obligations}=={r["name"] for r in roots}
    assert all(o["source_paragraphs"] for o in obligations)
    assert all(b["classification"] in ("SOURCE","TYPING") for o in obligations for b in o["binder_audit"])
    graph=load("author-graph-views.json")
    sg=graph["views"]["source-construction-graph"]
    ids={node["id"] for node in sg["nodes"]}
    assert len(ids)==len(sg["nodes"])
    for edge in sg["AND_hyperedges"]+graph["views"]["functor-hypergraph"]["hyperedges"]:
        assert edge["logic"]=="AND" and set(edge["tails"]+edge["heads"])<=ids
    assert len(graph["views"]["lean-graph"]["ownership_edges"])==319
    packet_text=(out/"author-decoder-packet.json").read_text(encoding="utf-8")
    for forbidden in (SOURCE_ID,LESSON,"source-construction-graph","binding_sha256","source-only.md"):
        # opaque_context_binding is only the formal context digest, never a publication/source verdict.
        if forbidden=="binding_sha256":
            assert "publication_"+forbidden not in packet_text
        else:
            assert forbidden not in packet_text
    catalog=json.loads((repo/"website/research/sources.json").read_bytes())
    row=load("author-source-row-candidate.json")["source"]
    existing=[s for s in catalog["sources"] if s["id"]==SOURCE_ID]
    assert not existing or existing==[row], "Existing exact source row changed."
    if not existing:
        catalog["sources"].append(row)
    overlay=OverlayRoot(repo,{LESSON:source,"website/research/sources.json":json.dumps(catalog,ensure_ascii=False).encode()})
    bind,checker_hash=binding_function(repo)
    assert checker_hash==frozen["checker_sha256"]
    candidate=load("publication-candidate-CubicStatePreparation.json")
    public={r["name"] for r in roots if not r["private"]}
    assert len(candidate["declarations"])==269 and set(candidate["declarations"])==public
    assert {n for edge in candidate["obligation_map"] for n in edge["declarations"]}==public
    assert candidate["status"]==WIP and not candidate["independent_acceptance"] and not candidate["main_admission"]
    assert bind(overlay,candidate)==candidate["binding_sha256"]
    if manifest:
        man=load("outputs-manifest.json")
        for rec in man["artifacts"]:
            raw=(out/rec["path"]).read_bytes()
            assert sha(raw)==rec["sha256"] and len(raw)==rec["bytes"], rec["path"]
            assert not re.search(r"(?:[A-Za-z]:[\\/]|^/|\\)",rec["planned_canonical_path"])
    return {"status":"MECHANICAL_AUTHOR_INTEGRITY_PASS_NOT_ADMISSION","whole_target_modules":1,
            "public_roots":269,"private_named_helpers":50,"structures":11,"opaque_contract_roots":7,
            "lossless_source_paragraphs":len(cov["source_paragraphs"]),
            "source_AND_edges":len(sg["AND_hyperedges"]),"open_SOURCE_GAPs":len(sg["open_source_gap_ids"]),
            "provider_closure_modules":len(providers),"whole_ambient_source_files":len(frozen["whole_ambient_binding_inputs"]),
            "binding_replayed_with_unchanged_checker":candidate["binding_sha256"],
            "registry_observed_count":frozen["registry_observed_count"],
            "validate_record_called":False,"Lean_executed":False,"independent_evidence_fabricated":False,
            "main_admission":False,"scientific_ROOT":False,"PURIFIED":False,"manifest_verified":manifest}


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo",type=Path,required=True)
    parser.add_argument("--out",type=Path,required=True)
    parser.add_argument("--verify",action="store_true")
    args=parser.parse_args()
    if args.verify:
        print(json.dumps(verify(args.repo.resolve(),args.out.resolve()),ensure_ascii=False,indent=2))
    else:
        build(args.repo.resolve(),args.out.resolve())

