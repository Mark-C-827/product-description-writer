#!/usr/bin/env python3
"""Pull discrete specs out of a raw spec sheet so nothing is lost in translation.

Feeds two things:
  - the writer's working checklist (every spec must be used or explicitly dropped)
  - validate_pdp.py --specs, which checks number coverage against the source

Usage:
    python extract_specs.py specs.txt
    python extract_specs.py specs.txt --json
    python extract_specs.py specs.txt --out spec-checklist.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

NUMERIC = re.compile(
    r"\b\d+(?:[.,]\d+)?\s?"
    r"(?:mm|cm|m|in|inch|inches|ft|oz|lb|lbs|g|kg|ml|l|L|°|mah|mAh|wh|Wh|w|W|v|V|"
    r"hz|Hz|gb|GB|tb|TB|mb|MB|%|x)\b",
    re.I,
)
DIMENSION = re.compile(r"\d+(?:\.\d+)?\s*[x×]\s*\d+", re.I)
MATERIAL_HINTS = re.compile(
    r"\b(stainless(?: steel)?|aluminum|aluminium|carbon steel|cast iron|damascus|titanium|"
    r"brass|copper|bronze|cotton|linen|wool|silk|polyester|nylon|leather|suede|denim|"
    r"bamboo|oak|walnut|birch|ash|maple|teak|ceramic|glass|silicone|ABS|polycarbonate|"
    r"pakkawood|micarta|G10|TPU|EVA|memory foam|down|flax)\b",
    re.I,
)
WARRANTY_HINTS = re.compile(r"\b(warranty|guarantee(d)?|limited lifetime)\b", re.I)
CARE_HINTS = re.compile(
    r"\b(machine wash|hand wash|dry clean|tumble dry|line dry|do not bleach|wipe clean|"
    r"dishwasher safe|hand wash only|spot clean|air dry|iron low)\b",
    re.I,
)
CERT_HINTS = re.compile(
    r"\b(OEKO-TEX|GOTS|FSC|CE|UL|FCC|RoHS|Energy Star|EN 71|CPSIA|ISO \d+|IP\d{2}|"
    r"bluesign|GRS|Fair Trade|USDA Organic)\b",
)
COMPAT_HINTS = re.compile(
    r"\b(compatible with|fits|works with|for use with|fits models?|compatible)\b", re.I,
)


def to_lines(text: str) -> list[str]:
    lines = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        line = re.sub(r"^\s*[-*+•]\s*", "", line)
        if not line:
            continue
        lines.append(line)
    return lines


def classify(line: str) -> list[str]:
    tags = []
    if DIMENSION.search(line):
        tags.append("dimension")
    elif NUMERIC.search(line):
        tags.append("numeric")
    if MATERIAL_HINTS.search(line):
        tags.append("material")
    if CARE_HINTS.search(line):
        tags.append("care")
    if CERT_HINTS.search(line):
        tags.append("certification")
    if COMPAT_HINTS.search(line):
        tags.append("compatibility")
    if WARRANTY_HINTS.search(line):
        tags.append("warranty")
    return tags or ["unclassified"]


def extract(text: str) -> dict:
    lines = to_lines(text)
    rows = []
    for i, line in enumerate(lines, 1):
        rows.append({"line": i, "spec": line, "tags": classify(line)})

    counts: dict[str, int] = {}
    for r in rows:
        for t in r["tags"]:
            counts[t] = counts.get(t, 0) + 1

    numbers = sorted({m.group(0).strip() for m in NUMERIC.finditer(text)})

    return {
        "total_lines": len(rows),
        "tag_counts": counts,
        "numbers": numbers,
        "rows": rows,
    }


def render_markdown(data: dict, source: str) -> str:
    out = [f"# Spec checklist - {source}", ""]
    out.append(f"Extracted {data['total_lines']} spec lines.")
    out.append("")
    out.append("Every line below must either appear in the copy or be listed in")
    out.append("'Notes to merchant' with a reason for dropping it.")
    out.append("")
    for tag in sorted(data["tag_counts"]):
        out.append(f"- {tag}: {data['tag_counts'][tag]}")
    out.append("")
    out.append("## Lines")
    out.append("")
    out.append("| # | Spec | Tags | Used? | Benefit / why dropped |")
    out.append("| --- | --- | --- | --- | --- |")
    for r in data["rows"]:
        spec = r["spec"].replace("|", "\\|")
        out.append(f"| {r['line']} | {spec} | {', '.join(r['tags'])} |  |  |")
    out.append("")
    if data["numbers"]:
        out.append("## Numbers that must reach the Details block")
        out.append("")
        for n in data["numbers"]:
            out.append(f"- {n}")
        out.append("")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description="Extract specs from a raw spec sheet.")
    ap.add_argument("specs", help="Path to the raw spec sheet (txt or md).")
    ap.add_argument("--json", action="store_true", help="Emit JSON.")
    ap.add_argument("--out", help="Write the markdown checklist to this path.")
    args = ap.parse_args()

    path = Path(args.specs)
    if not path.exists():
        print(f"error: file not found: {path}", file=sys.stderr)
        return 1

    data = extract(path.read_text(encoding="utf-8"))

    if args.json:
        print(json.dumps(data, indent=2))
    elif args.out:
        Path(args.out).write_text(render_markdown(data, path.name), encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        print(render_markdown(data, path.name))
    return 0


if __name__ == "__main__":
    sys.exit(main())
