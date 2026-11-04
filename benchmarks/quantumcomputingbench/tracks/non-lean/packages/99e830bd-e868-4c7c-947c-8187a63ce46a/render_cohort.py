#!/usr/bin/env python3
"""Render the frozen QA payloads into a readable Markdown companion."""
import json
from pathlib import Path


def cell(value):
    if not isinstance(value, str):
        value = json.dumps(value, ensure_ascii=False)
    return value.replace("|", "\\|").replace("\n", " ")


def bullets(values):
    return "\n".join("- " + (x if isinstance(x, str) else json.dumps(x, ensure_ascii=False))
                     for x in values)


def main():
    root = Path(__file__).resolve().parent
    files = sorted((root / "qa").glob("[ABC][1-4].json"))
    if len(files) != 12:
        raise ValueError("Expected the twelve frozen cohort payloads.")
    items = [json.loads(f.read_text()) for f in files]
    out = ["# State-preparation foundations and composition cohort\n",
           "Twelve proposed contribution packets: four existing-core refinements and eight "
           "unadmitted candidates. This rendering is derived from the authoritative JSON "
           "payloads. Current exact-content review status is in `manifest.json` and the "
           "review reports; author-time uncertainty statements are preserved unchanged. "
           "No benchmark admission, new Lean verification or measured model difficulty is implied.\n",
           "| Slot | Target | Identity kind |\n| --- | --- | --- |"]
    out += [f"| {i['slot']} | [{cell(i['title'])}](#{i['slot'].lower()}) | {i['contribution_type']} |"
            for i in items]
    for item in items:
        slot=item['slot']
        out += [f"\n## {slot}\n", f"**{item['title']}**\n",
                f"Core: `{item['core_id']}`. Split: `{item['split']}`. "
                f"Author: `{item['author']}`. [Authoritative payload](qa/{slot}.json).\n",
                "### Mathematical target\n", item['mathematical_target'],
                "\n### Assumptions\n", bullets(item['assumptions']) or "No extra assumptions are added to the immutable question.",
                "\n### Conventions\n", bullets(item['conventions']) or "The mathematical conventions are stated in the question.",
                "\n### Question\n", item['question'],
                "\n### Reference answer\n", item['reference_answer'],
                "\n### Partial-credit rubric\n",
                "Score out of 10. Credit mathematically valid alternative derivations; the stated criteria assess correctness, not wording.\n",
                "| Points | Criterion |\n| --- | --- |"]
        out += [f"| {r['weight']} | {cell(r['criterion'])} |" for r in item['rubric']]
        out += ["\n### Common errors\n", bullets(item['common_errors']),
                "\n### Boundary cases\n", bullets(item['boundary_cases']),
                "\n### Difficulty annotation\n", "```json\n"+json.dumps(item['difficulty'],indent=2,ensure_ascii=False)+"\n```",
                "\n### Author-supplied reasoning map\n",
                "These are natural-language mathematical dependencies, not extracted Lean proof-term dependencies. All required inputs at a step are conjunctive.\n",
                "| Input | Kind | Statement |\n| --- | --- | --- |"]
        out += [f"| {cell(x['id'])} | {cell(x.get('kind',''))} | {cell(x['statement'])} |" for x in item['reasoning_map']['inputs']]
        for step in item['reasoning_map']['steps']:
            out += [f"\n**{step['id']}: {step['claim']}**\n",
                    "Assumptions: "+cell(step['assumptions'])+". Required inputs (AND): "+", ".join(step['required_inputs'])+".\n",
                    "Conclusion: "+step['conclusion']+"\n", "Justification: "+step['justification']+"\n"]
        out += ["Reuse and reconvergence:\n", "```json\n"+json.dumps({k:item['reasoning_map'][k] for k in ['reused_results','reconvergent_branches']},indent=2,ensure_ascii=False)+"\n```",
                "\n### Sources and evidence boundary\n"]
        for ref in item['source_refs']:
            url="https://github.com/DakeBU/QuantumComputinglib-QuantumComputingBench/blob/6b23dab68c2970062ddfd568ce94bce74b566483/"+ref['path']
            out += [f"- [{ref['path']}]({url}): {ref['anchor']} SHA-256 `{ref['sha256']}`. {ref['license']}"]
        out += ["\nComplete source checks, separate reading/import/conceptual/dependency records, overlap and uncertainty are in the JSON payload.\n",
                bullets(item['unverified']), "\n---\n"]
    (root/'COHORT.md').write_text("\n".join(out).rstrip()+"\n",encoding='utf-8')


if __name__=='__main__':
    main()
