"""Inventory downloaded public documentation; never evaluate survey expressions.

Inputs are fixed A032 XLSForm cell metadata and public DDI, not respondent files.
Output describes syntactic references, not executable gates or observed errors.
"""

import collections
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parent
NS = {"d": "http://www.icpsr.umich.edu/DDI"}
REFERENCE = re.compile(r"\$\{([^}]+)\}")


def main():
    cells = json.loads((ROOT / "questionnaire-cells.json").read_text(encoding="utf-8"))
    ddi = ET.parse(ROOT / "catalog1030-ddi.xml").getroot()
    variables = []
    by_name = collections.defaultdict(list)
    for var in ddi.findall(".//d:var", NS):
        item = {
            "id": var.get("ID"), "name": var.get("name"),
            "file": var.get("files"), "label": var.findtext("d:labl", namespaces=NS),
            "categories": [
                {"value": cat.findtext("d:catValu", namespaces=NS),
                 "label": cat.findtext("d:labl", namespaces=NS)}
                for cat in var.findall("d:catgry", NS)
            ],
        }
        variables.append(item)
        by_name[item["name"]].append({k: item[k] for k in ("id", "file")})

    result = {"scope": "PUBLIC_METADATA_ONLY", "ddi_variable_count": len(variables),
              "files": [{"id": f.get("ID"),
                         "name": f.findtext("d:fileTxt/d:fileName", namespaces=NS)}
                        for f in ddi.findall(".//d:fileDscr", NS)],
              "forms": {}, "ddi_variables": variables}
    for filename, sheets in cells.items():
        headers = {value: key for key, value in sheets["survey"][0]["cells"].items()}
        rows, stack, anomalies = [], [], []
        for record in sheets["survey"][1:]:
            c = record["cells"]
            kind = c.get(headers["type"], "").strip()
            if kind in ("end_group", "end_repeat", "end group", "end repeat"):
                expected = "repeat" if "repeat" in kind else "group"
                if not stack:
                    anomalies.append({"row": record["row"], "issue": "unmatched end"})
                else:
                    opened = stack.pop()
                    if expected not in opened["type"]:
                        anomalies.append({"row": record["row"], "issue": "nesting mismatch"})
                continue
            name = c.get(headers["name"], "")
            if not name:
                continue
            row = {"row": record["row"], "name": name, "type": kind,
                   "chapter_raw": c.get(headers["chapter"], ""),
                   "relevant": c.get(headers["relevant"], ""),
                   "calculation": c.get(headers["calculation"], ""),
                   "required": c.get(headers["required"], ""),
                   "disabled": c.get(headers["disabled"], ""),
                   "ancestors": [dict(a) for a in stack],
                   "ddi_exact_name_matches": by_name.get(name, [])}
            rows.append(row)
            if kind in ("begin_group", "begin_repeat", "begin group", "begin repeat"):
                stack.append({k: row[k] for k in ("row", "name", "type", "chapter_raw", "relevant")})
        if stack:
            anomalies.append({"issue": "unclosed containers", "rows": [s["row"] for s in stack]})
        names = collections.defaultdict(list)
        for row in rows:
            names[row["name"]].append(row)
        edges, unresolved = [], []
        for child in rows:
            refs = sorted(set(REFERENCE.findall(child["relevant"])))
            for ref in refs:
                parents = names.get(ref, [])
                if len(parents) != 1:
                    unresolved.append({"child_row": child["row"], "reference": ref,
                                       "matches": len(parents)})
                    continue
                parent = parents[0]
                edges.append({"child_row": child["row"], "child": child["name"],
                              "child_type": child["type"], "child_chapter_raw": child["chapter_raw"],
                              "parent_row": parent["row"], "parent": ref,
                              "parent_type": parent["type"], "parent_chapter_raw": parent["chapter_raw"],
                              "explicit_cross_chapter": bool(child["chapter_raw"] and parent["chapter_raw"]
                                                             and child["chapter_raw"] != parent["chapter_raw"])})
        special = []
        for record in sheets["choices"][1:]:
            c = record["cells"]
            if re.search(r"refus|don.t know|not applicable|not asked|prefer not", c.get("C", ""), re.I):
                special.append({"row": record["row"], "list": c.get("A"),
                                "code": c.get("B"), "label": c.get("C"),
                                "note": "Text match only; semantic classification requires review."})
        result["forms"][filename] = {
            "settings": sheets["settings"], "survey_nonempty_rows_including_header": len(sheets["survey"]),
            "choice_rows_including_header": len(sheets["choices"]), "rows": rows,
            "direct_relevance_edges_deduplicated_per_child_parent": edges,
            "unresolved_direct_references": unresolved, "nesting_anomalies": anomalies,
            "special_choice_text_matches": special,
            "duplicate_names": {k: [r["row"] for r in v] for k, v in names.items() if len(v) > 1},
        }
    result["limitations"] = [
        "No expression evaluation, inferred chapter assignment or response access.",
        "Ancestor contexts retained; direct edge counts omit inherited/calculation dependencies.",
        "Chapter labels differ between forms; raw labels are not normalized or renamed.",
        "Exact variable-name match does not establish provenance, unit, category or semantic parity.",
        "No export transformation, missing-reason or observed routing-error inference.",
    ]
    output = ROOT / "routing-metadata.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary = {"ddi_variables": len(variables), "forms": {}}
    for name, form in result["forms"].items():
        summary["forms"][name] = {
            "named_rows": len(form["rows"]),
            "direct_edges": len(form["direct_relevance_edges_deduplicated_per_child_parent"]),
            "explicit_cross_chapter_edges": sum(e["explicit_cross_chapter"] for e in form["direct_relevance_edges_deduplicated_per_child_parent"]),
            "unresolved_direct_references": len(form["unresolved_direct_references"]),
            "nesting_anomalies": form["nesting_anomalies"], "duplicate_names": form["duplicate_names"],
        }
    print(json.dumps(summary, ensure_ascii=True))


if __name__ == "__main__":
    main()
