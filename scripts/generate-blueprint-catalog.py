#!/usr/bin/env python3
"""Generate the exhaustive, auditable Verso Blueprint declaration catalog."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "QuantumBlockEncoding"
OUTPUT_ROOT = ROOT / "ABEISBlueprint" / "Catalog"
REPORT_PATH = ROOT / "docs" / "blueprint-coverage.json"
EXPLORER_PATH = ROOT / "web" / "library" / "declarations.json"

KINDS = (
    "def",
    "abbrev",
    "opaque",
    "inductive",
    "structure",
    "class",
    "theorem",
    "lemma",
)
THEOREM_KINDS = {"theorem", "lemma"}
DECL_RE = re.compile(
    r"^\s*(?:(?:@\[[^\n]*?\])\s*)*"
    r"(?P<mods>(?:(?:private|protected|noncomputable|unsafe|partial)\s+)*)"
    r"(?P<kind>" + "|".join(KINDS) + r")\s+"
    r"(?P<name>[^\s\(\{\[\:]+)"
)
SCOPE_RE = re.compile(r"^\s*(namespace|section)\s*([^\s-]*)")
END_RE = re.compile(r"^\s*end(?:\s+([^\s-]+))?")


@dataclass(frozen=True)
class Declaration:
    kind: str
    name: str
    full_name: str
    source: str
    line: int
    doc: str
    source_preview: str
    experimental: bool
    open_proof: bool


@dataclass
class Scope:
    kind: str
    name: str


CATALOGS = [
    (
        "Foundations",
        "catalog-foundations",
        {
            "Core.lean",
            "Resources.lean",
            "Circuit.lean",
            "BlockEncoding.lean",
            "StatePreparation.lean",
            "TechnicalLemmas.lean",
        },
    ),
    (
        "Semantics",
        "catalog-semantics",
        {
            "CircuitSemantics.lean",
            "ConcreteSemantics.lean",
            "PrimitiveCircuit.lean",
            "PrimitiveBasisLE.lean",
            "PrimitiveSemantics.lean",
            "PrimitiveRefinement.lean",
            "ReversibleClassical.lean",
            "PrimitiveMacros.lean",
            "ModularAdder3.lean",
            "PromiseGateOptimization.lean",
            "UniformlyControlledRy.lean",
            "TextbookStatePreparation.lean",
            "TeachingRouteClosures.lean",
        },
    ),
    (
        "ClassicRoutes",
        "catalog-classic-routes",
        {"BandedSparseAccess.lean", "BandedSparseAccessPrimitive.lean", "BlockEncodingClassics.lean"},
    ),
    (
        "CertifiedCases",
        "catalog-certified-cases",
        {"ColdStartTransferE1.lean", "MainCase.lean", "OptimalControl.lean"},
    ),
    ("Cubic", "catalog-cubic", {"CubicStatePreparation.lean", "CubicAmplitudePrimitive.lean"}),
    (
        "PaperAndExamples",
        "catalog-paper-and-examples",
        {
            "GHL2025.lean",
            "GHLHamiltonian.lean",
            "Papers/GHL2025.lean",
            "Examples/RobinHeat.lean",
            "RobinEvolution.lean",
            "Robin/FixedN3Data.lean",
            "Robin/SourceBaseline.lean",
            "Robin/WeightedPermutation.lean",
            "Robin/EvolvedCandidates.lean",
            "Robin/ResourceComparison.lean",
            "Robin/ComplexLCU.lean",
            "Robin/ComplexLCUProjection.lean",
            "Robin/Hadamard8Verified.lean",
            "Robin/Hadamard8BlockEncoding.lean",
            "Robin/SixSlotOptimal.lean",
            "Robin/SymmetryFourSlot.lean",
            "Robin/SymmetryFourSlotLogicalUnitary.lean",
            "Robin/SymmetryFourSlotBlockEncoding.lean",
            "Robin/SymmetryFourSlotPrimitive.lean",
            "Robin/SymmetryXorFourSlotLogicalUnitary.lean",
            "Robin/SymmetryXorFourSlotPrimitive.lean",
            "Robin/SourceSevenSparseData.lean",
            "Robin/PaperSevenPrepare.lean",
            "Robin/PaperSevenLogicalUnitary.lean",
            "Robin/PaperSevenPrimitive.lean",
            "Robin/PaperSevenAmplitudePrimitive.lean",
            "Robin/PaperSevenPreparePrimitive.lean",
            "Robin/PaperSevenT3.lean",
            "Robin/Figure4SourceData.lean",
            "Robin/Figure4Primitive.lean",
            "Robin/Figure4Loaders.lean",
            "Robin/Figure4PreparePrimitive.lean",
            "Robin/Figure4MiddlePrimitive.lean",
            "Robin/Figure4T3.lean",
            "Robin/T3ResourceComparison.lean",
            "Robin/SystemConjugation.lean",
        },
    ),
    (
        "AutomationAndMemory",
        "catalog-automation-and-memory",
        {"Automation.lean", "AutomationTrace.lean", "Literature.lean", "OpenProblems.lean", "OpenProblemsAudit.lean"},
    ),
    (
        "ExperimentalRobinMatrix",
        "catalog-experimental-robin-matrix",
        {"RobinMatrix.lean"},
    ),
]

CATALOG_PURPOSES = {
    "Foundations": (
        "Core finite matrices, task contracts, resource records, circuit syntax, "
        "and certificate data structures."
    ),
    "Semantics": (
        "Definitions and lemmas that connect circuit syntax to evaluated matrix "
        "semantics, finite state action, and explicit product-register projection."
    ),
    "ClassicRoutes": (
        "Reusable band-address, permutation, sparse, LCU, product, dilation, "
        "and QSVT-facing block-encoding routes."
    ),
    "CertifiedCases": (
        "Completed transfer-operator and optimal-control certificates used as "
        "end-to-end case studies."
    ),
    "Cubic": (
        "State-preparation and exact rational Householder developments for the "
        "cubic benchmark family."
    ),
    "PaperAndExamples": (
        "Paper-facing backend models and concrete Robin-boundary example "
        "artifacts."
    ),
    "AutomationAndMemory": (
        "Typed controller state, agent contracts, literature memory, and "
        "explicit open-problem records."
    ),
    "ExperimentalRobinMatrix": (
        "Compiled Robin-matrix research included in the full ASPBE gate; local "
        "results are separated from the broader paper route and external contracts."
    ),
}


def relative_source(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def clean_doc(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    text = text.replace(chr(96), "'")
    text = text.replace(":::", "").replace("%%%", "")
    text = text.replace("#", "number ")
    return text


def doc_before(text: str, offset: int) -> str:
    prefix = text[:offset]
    end = prefix.rfind("-/")
    if end < 0:
        return ""
    start = prefix.rfind("/--", 0, end)
    if start < 0:
        return ""
    between = prefix[end + 2 :]
    stripped = re.sub(r"@\[[^\n]*?\]", "", between)
    stripped = re.sub(r"/-.*?-/", "", stripped, flags=re.S)
    stripped = re.sub(r"--[^\n]*", "", stripped)
    if stripped.strip():
        return ""
    return clean_doc(prefix[start + 3 : end])


def namespace_parts(scopes: list[Scope]) -> list[str]:
    parts: list[str] = []
    for scope in scopes:
        if scope.kind == "namespace" and scope.name:
            parts.extend(scope.name.split("."))
    return parts


def qualify(name: str, scopes: list[Scope]) -> str:
    if name.startswith("_root_."):
        return name.removeprefix("_root_.")
    return ".".join([*namespace_parts(scopes), name])


def source_preview(lines: list[str], start_line: int, limit: int = 14) -> str:
    """Return a bounded, deterministic declaration-local source preview."""

    start = start_line - 1
    preview: list[str] = []
    for index in range(start, min(len(lines), start + limit)):
        line = lines[index].rstrip("\r\n")
        if index > start and DECL_RE.match(line):
            break
        if (
            index > start
            and not line.startswith((" ", "\t"))
            and re.match(r"^(?:namespace|section|end)\b", line)
        ):
            break
        preview.append(line.rstrip())
    while preview and not preview[-1]:
        preview.pop()
    return "\n".join(preview)


def declaration_slug(full_name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", full_name.lower()).strip("-")


def module_slug(source: str) -> str:
    path = source.removeprefix("QuantumBlockEncoding/").removesuffix(".lean")
    return re.sub(r"[^a-z0-9]+", "-", path.lower()).strip("-")


def contains_proof_hole(preview: str) -> bool:
    """Recognize an actual sorry term without matching docs, names, or strings."""

    for line in preview.splitlines():
        stripped = line.strip()
        if re.match(r"^(?:exact\s+)?sorry(?:\s|$)", stripped):
            return True
        if re.search(r":=\s*sorry(?:\s|$)", stripped):
            return True
    return False


def parse_source(path: Path) -> tuple[list[Declaration], list[dict[str, object]]]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    scopes: list[Scope] = []
    declarations: list[Declaration] = []
    exclusions: list[dict[str, object]] = []
    offset = 0
    comment_depth = 0

    for line_no, line in enumerate(lines, start=1):
        starts_in_comment = comment_depth > 0
        match = None if starts_in_comment else DECL_RE.match(line)
        if match:
            kind = match.group("kind")
            name = match.group("name")
            modifiers = match.group("mods").split()
            full_name = qualify(name, scopes)
            if "private" in modifiers:
                exclusions.append(
                    {
                        "kind": kind,
                        "name": full_name,
                        "source": relative_source(path),
                        "line": line_no,
                        "reason": "private declaration",
                    }
                )
            else:
                preview = source_preview(lines, line_no)
                declarations.append(
                    Declaration(
                        kind=kind,
                        name=name,
                        full_name=full_name,
                        source=relative_source(path),
                        line=line_no,
                        doc=doc_before(text, offset),
                        source_preview=preview,
                        experimental=relative_source(path)
                        == "QuantumBlockEncoding/RobinMatrix.lean",
                        open_proof=contains_proof_hole(preview),
                    )
                )

        scope_match = None if starts_in_comment else SCOPE_RE.match(line)
        if scope_match:
            scopes.append(Scope(scope_match.group(1), scope_match.group(2)))
        else:
            end_match = None if starts_in_comment else END_RE.match(line)
            if end_match and scopes:
                expected = end_match.group(1)
                if expected:
                    for index in range(len(scopes) - 1, -1, -1):
                        if scopes[index].name == expected:
                            del scopes[index:]
                            break
                    else:
                        scopes.pop()
                else:
                    scopes.pop()
        comment_depth += line.count("/-") - line.count("-/")
        if comment_depth < 0:
            comment_depth = 0
        offset += len(line)

    return declarations, exclusions


def lean_string(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"')


def verso_prose(text: str) -> str:
    """Escape source prose so it cannot become Blueprint markup."""

    escaped = text.replace("\\", "\\\\")
    for character in ("*", "_", "[", "]", "{", "}"):
        escaped = escaped.replace(character, "\\" + character)
    return escaped


def humanize_identifier(full_name: str) -> str:
    leaf = full_name.rsplit(".", maxsplit=1)[-1].strip("«»")
    text = leaf.replace("_", " ")
    text = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", text)
    text = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", " ", text)
    text = re.sub(r"(?<=[A-Za-z])(?=[0-9])", " ", text)
    text = re.sub(r"(?<=[0-9])(?=[A-Za-z])", " ", text)
    return re.sub(r"\s+", " ", text).strip().lower()


def first_sentence(text: str, limit: int = 260) -> str:
    sentence = re.split(r"(?<=[.!?])\s+", text, maxsplit=1)[0].strip()
    if len(sentence) <= limit:
        return sentence
    shortened = sentence[: limit - 1].rsplit(" ", maxsplit=1)[0]
    return shortened.rstrip(" ,;:") + "…"


def plain_english(decl: Declaration) -> str:
    topic = humanize_identifier(decl.full_name)
    source_summary = first_sentence(decl.doc) if decl.doc else ""
    if decl.kind in THEOREM_KINDS:
        if decl.experimental:
            lead = (
                f"Lean checks the research-module proposition indexed as “{topic}”; "
                "its local proof does not by itself complete the broader paper route."
            )
        else:
            lead = (
                f"Lean checks the proposition indexed as “{topic}”; the hypotheses "
                f"and conclusion in the code panel fix its exact scope."
            )
    elif decl.kind == "structure":
        lead = (
            f"This record groups the data and proof fields needed for “{topic}”. "
            "A proposition-valued field is a requirement until a constructor supplies it."
        )
    elif decl.kind == "inductive":
        lead = (
            f"This type lists the allowed alternatives for “{topic}”; its constructors "
            "are the cases that downstream code must handle."
        )
    elif decl.kind == "abbrev":
        lead = (
            f"This abbreviation gives a shorter name to the type or expression "
            f"used for “{topic}”."
        )
    elif decl.kind == "opaque":
        lead = (
            f"This opaque declaration exposes the interface for “{topic}” while "
            "keeping its implementation from unfolding automatically."
        )
    else:
        lead = (
            f"This definition gives the library's named construction or computation "
            f"for “{topic}”."
        )
    return f"{lead} {source_summary}".strip()


def formal_status(decl: Declaration) -> str:
    if decl.open_proof:
        return (
            "Stated, proof incomplete. This declaration contains an explicit "
            "proof hole and is never counted as a compiled result."
        )
    if decl.experimental:
        return (
            "Compiled by the full ASPBE gate in a research-level module. The "
            "displayed theorem is checked, but it does not promote a broader "
            "paper route or an external oracle contract."
        )
    if decl.kind in THEOREM_KINDS:
        return (
            "Compiled theorem in the default ASPBE import surface; the displayed "
            "Lean signature is the authoritative claim."
        )
    if decl.kind == "structure":
        return (
            "Data contract in the default import surface; proposition-valued fields "
            "are obligations, not automatically established facts."
        )
    return (
        "Compiled declaration in the default ASPBE import surface; its kind and "
        "displayed Lean type determine how it may be used."
    )


def local_status(decl: Declaration) -> str:
    if decl.open_proof:
        return "Stated, proof incomplete"
    return "Compiled"


def route_status(decl: Declaration) -> str:
    if decl.open_proof:
        return "Blocked"
    if decl.experimental:
        return "Experimental"
    if decl.source.endswith("OpenProblems.lean"):
        return "Planned"
    if decl.source.endswith(
        ("GHL2025.lean", "RobinEvolution.lean", "Automation.lean", "Literature.lean")
    ):
        return "Partial route"
    if decl.kind in {"structure", "class", "opaque"}:
        return "Partial route"
    return "Compiled"


def render_declaration(decl: Declaration, catalog_name: str) -> str:
    directive = "theorem" if decl.kind in THEOREM_KINDS else "definition"
    explanation = decl.doc or (
        "The source declaration has no docstring. The reader cue above is generated "
        "from its kind and name and does not replace the Lean signature."
    )
    local_url = (
        "../../../../library/modules/"
        f"{module_slug(decl.source)}/#decl-{declaration_slug(decl.full_name)}"
    )
    return (
        f':::{directive} "{lean_string(decl.full_name)}" '
        f'(lean := "{lean_string(decl.full_name)}")\n'
        f"*Plain-English reading.* {verso_prose(plain_english(decl))}\n\n"
        f"*Formal status.* {verso_prose(formal_status(decl))}\n\n"
        f"*Why it is in this chapter.* "
        f"{verso_prose(CATALOG_PURPOSES[catalog_name])}\n\n"
        f"*Technical source note.* {verso_prose(explanation)}\n\n"
        f"*Declaration kind.* {decl.kind}.\n\n"
        f"Source: [{decl.source}:{decl.line}]({local_url}). "
        "A commit-pinned external link is added by the publication build when "
        "the source exists at the published ref.\n"
        ":::\n"
    )


def render_catalog(
    module_name: str, slug: str, declarations: list[Declaration]
) -> str:
    by_source: dict[str, list[Declaration]] = {}
    for declaration in declarations:
        by_source.setdefault(declaration.source, []).append(declaration)

    imports = ["import QuantumBlockEncoding"]
    if any(decl.experimental for decl in declarations):
        imports.append("import QuantumBlockEncoding.RobinMatrix")
    body = [
        *imports,
        "import Verso",
        "import VersoManual",
        "import VersoBlueprint",
        "",
        "open Verso.Genre",
        "open Verso.Genre.Manual",
        "open Informal",
        "",
        "set_option linter.hashCommand false",
        "set_option linter.style.longLine false",
        "set_option verso.blueprint.externalCode.strictResolve true",
        "",
        f'#doc (Manual) "Declaration catalog: {module_name}" =>',
        "%%%",
        f'file := "{slug}"',
        "%%%",
        "",
        "This chapter is generated from the Lean source. Every node denotes one explicit public",
        "declaration, and every Lean link is checked during the Blueprint build. Definitions appear",
        "in source order before later results whenever the source module does so.",
        "",
        f"Reader orientation: {CATALOG_PURPOSES[module_name]} Each card separates an accessible",
        "reading cue from formal status, the source docstring, and the authoritative Lean panel.",
        "The standalone Library Explorer adds full-text search and filters across every chapter.",
        "",
    ]
    if any(decl.experimental for decl in declarations):
        body.extend(
            [
                "*Research-module status.* RobinMatrix.lean is compiled by the full ASPBE gate",
                "with zero proof holes. Its declarations include proved helper lemmas, explicit",
                "counterexamples, and typed external contracts. A compiled local declaration does",
                "not by itself certify the complete paper construction.",
                "",
            ]
        )
    for source, source_declarations in by_source.items():
        body.extend(
            [
                f"# {source}",
                "",
                f"{len(source_declarations)} explicit public declarations, in source order.",
                "",
            ]
        )
        for declaration in source_declarations:
            body.append(render_declaration(declaration, module_name))
    return "\n".join(body).rstrip() + "\n"


def catalog_for(decl: Declaration) -> tuple[str, str]:
    source_name = decl.source.removeprefix("QuantumBlockEncoding/")
    for module_name, slug, source_names in CATALOGS:
        if source_name in source_names:
            return module_name, slug
    raise ValueError(f"declaration is not assigned to a catalog: {decl.full_name}")


def blueprint_declaration_url(decl: Declaration, catalog_slug: str) -> str:
    """Link directly to the generated source subpage and Lean panel."""

    source_route = decl.source.replace("/", "___").replace(".", "___")
    encoded_name = decl.full_name.replace(".", "___")
    anchor = (
        "--informal-preview-_FLQQ_"
        f"{encoded_name}_FLQQ_--statement"
    )
    return (
        f"../blueprint/html-multi/{catalog_slug}/{source_route}/"
        f"#{anchor}"
    )


def render_explorer(declarations: list[Declaration]) -> str:
    by_catalog: dict[str, int] = {}
    entries: list[dict[str, object]] = []
    for decl in declarations:
        catalog_name, slug = catalog_for(decl)
        by_catalog[catalog_name] = by_catalog.get(catalog_name, 0) + 1
        entries.append(
            {
                "kind": decl.kind,
                "name": decl.name,
                "fullName": decl.full_name,
                "readerLabel": humanize_identifier(decl.full_name),
                "plainEnglish": plain_english(decl),
                "formalStatus": formal_status(decl),
                "technicalNote": decl.doc,
                "sourcePreview": decl.source_preview,
                "source": decl.source,
                "line": decl.line,
                "sourceUrl": None,
                "localSourceUrl": (
                    f"library/modules/{module_slug(decl.source)}/"
                    f"#decl-{declaration_slug(decl.full_name)}"
                ),
                "catalog": catalog_name,
                "catalogPurpose": CATALOG_PURPOSES[catalog_name],
                "blueprintUrl": blueprint_declaration_url(decl, slug),
                "experimental": decl.experimental,
                "openProof": decl.open_proof,
                "localStatus": local_status(decl),
                "routeStatus": route_status(decl),
            }
        )
    payload = {
        "schemaVersion": 2,
        "scope": (
            "Every explicit public def/abbrev/opaque/inductive/structure/class/"
            "theorem/lemma declaration in QuantumBlockEncoding"
        ),
        "publicDeclarationCount": len(declarations),
        "sourceDocstringCount": sum(bool(decl.doc) for decl in declarations),
        "generatedReaderCueCount": len(declarations),
        "byCatalog": {
            name: by_catalog.get(name, 0) for name, _, _ in CATALOGS
        },
        "declarations": entries,
    }
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def collect() -> tuple[list[Declaration], list[dict[str, object]]]:
    declarations: list[Declaration] = []
    exclusions: list[dict[str, object]] = []
    for source in sorted(SOURCE_ROOT.rglob("*.lean")):
        found, excluded = parse_source(source)
        declarations.extend(found)
        exclusions.extend(excluded)
    return declarations, exclusions


def generate(check: bool) -> int:
    declarations, exclusions = collect()
    assigned: set[str] = set()
    outputs: dict[Path, str] = {}

    for module_name, slug, source_names in CATALOGS:
        selected = [
            declaration
            for declaration in declarations
            if declaration.source.removeprefix("QuantumBlockEncoding/") in source_names
        ]
        assigned.update(declaration.full_name for declaration in selected)
        outputs[OUTPUT_ROOT / f"{module_name}.lean"] = render_catalog(
            module_name, slug, selected
        )
    outputs[EXPLORER_PATH] = render_explorer(declarations)

    unassigned = [
        declaration
        for declaration in declarations
        if declaration.full_name not in assigned
    ]
    counts: dict[str, int] = {}
    for declaration in declarations:
        counts[declaration.full_name] = counts.get(declaration.full_name, 0) + 1
    duplicate_names = sorted(name for name, count in counts.items() if count > 1)
    if unassigned or duplicate_names:
        details = {
            "unassigned": [asdict(declaration) for declaration in unassigned],
            "duplicateNames": duplicate_names,
        }
        raise SystemExit(
            "catalog partition is incomplete:\n"
            + json.dumps(details, indent=2, ensure_ascii=False)
        )

    by_kind: dict[str, int] = {}
    by_source: dict[str, int] = {}
    for declaration in declarations:
        by_kind[declaration.kind] = by_kind.get(declaration.kind, 0) + 1
        by_source[declaration.source] = by_source.get(declaration.source, 0) + 1
    report = {
        "schemaVersion": 2,
        "scope": (
            "Explicit public def/abbrev/opaque/inductive/structure/class/"
            "theorem/lemma declarations"
        ),
        "publicDeclarationCount": len(declarations),
        "privateDeclarationExclusionCount": len(exclusions),
        "sourceDocstringCount": sum(bool(decl.doc) for decl in declarations),
        "generatedReaderCueCount": len(declarations),
        "byKind": dict(sorted(by_kind.items())),
        "bySource": dict(sorted(by_source.items())),
        "excluded": exclusions,
        "generatedCatalogs": [
            path.relative_to(ROOT).as_posix()
            for path in outputs
            if path.parent == OUTPUT_ROOT
        ],
        "libraryExplorer": EXPLORER_PATH.relative_to(ROOT).as_posix(),
    }
    outputs[REPORT_PATH] = (
        json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    )

    stale: list[str] = []
    for path, content in outputs.items():
        if check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(path.relative_to(ROOT).as_posix())
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8", newline="\n")

    if stale:
        print("Generated Blueprint files are stale:")
        for path in stale:
            print(f"  {path}")
        return 1

    action = "checked" if check else "generated"
    print(
        f"{action} {len(declarations)} public declarations; "
        f"excluded {len(exclusions)} private declarations"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if committed generated files differ from the source inventory",
    )
    args = parser.parse_args()
    return generate(args.check)


if __name__ == "__main__":
    raise SystemExit(main())
