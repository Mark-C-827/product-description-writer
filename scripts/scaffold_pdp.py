#!/usr/bin/env python3
"""Emit a blank PDP skeleton to fill in.

For when you would rather have the structure in front of you than hold it in
your head. The skeleton encodes the F-pattern: hook, intro, bullets, objections,
CTA, Details.

Usage:
    python scaffold_pdp.py                          # generic
    python scaffold_pdp.py --category apparel       # category-aware prompts
    python scaffold_pdp.py --product "8in Chef Knife" --out knife.md
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

CATEGORY_PROMPTS = {
    "apparel": "Fit, fabric and feel. Model measurements AND garment measurements.",
    "electronics": "Capability, compatibility, battery with conditions.",
    "beauty": "Sensory experience and actives. No outcome claims.",
    "home": "Dimensions, materials, assembly, delivery.",
    "food": "Taste, ingredients, allergens, servings.",
    "tools": "The job it does. Materials, ratings, warranty.",
    "outdoor": "Conditions handled. Ratings with standards named, weight.",
    "auto": "Fitment (year/make/model), install, durability.",
    "jewelry": "Materials and craft with exact specs. Never 'luxury'.",
    "baby": "Age range, materials, named safety standards, care.",
    "digital": "Workflow outcome, platform support, limits, terms.",
}

TEMPLATE = """# PDP master copy - {product}

> Fill every section. Delete nothing that a shopper needs.
> Voice: {voice_note}
{category_note}
## Lead hook

<!-- One line. The transformation, not the category. Must work standalone. -->

<!-- Example: Slices a ripe tomato without crushing it. -->

## Intro

<!-- 2-3 sentences, each under 20 words. Hook -> context -> setup. -->

## Benefit bullets

<!-- 3-5. Each: **bold payoff** -> mechanism -> spec. One idea each. -->

- **<payoff>** - <mechanism>, <spec from source>.
- **<payoff>** - <mechanism>, <spec from source>.
- **<payoff>** - <mechanism>, <spec from source>.

## Good to know

<!-- Optional. 2-4 honest lines answering real objections. Delete if empty. -->

- <objection> - <honest answer>
- <objection> - <honest answer>

## CTA

<!-- One line. Restate the benefit. Never a bare "Buy now". -->

## Details

<!-- Every literal number, dimension, material and care instruction from the source.
     No marketing language here. -->

| Spec | Value |
| --- | --- |
|  |  |
|  |  |
|  |  |

## Notes to merchant

<!-- Specs dropped and why -->
<!-- Claims that could not be supported from the inputs -->
<!-- Assumptions to verify before publishing -->
---

Before shipping: python scripts/validate_pdp.py <this file> --specs <spec sheet>
"""


def main() -> int:
    ap = argparse.ArgumentParser(description="Scaffold a blank PDP copy file.")
    ap.add_argument("--product", default="<product name>", help="Product name for the heading.")
    ap.add_argument("--category", help="One of: " + ", ".join(sorted(CATEGORY_PROMPTS)))
    ap.add_argument("--voice", help="Voice note to carry at the top of the file.")
    ap.add_argument("--out", help="Write to this path instead of stdout.")
    args = ap.parse_args()

    category_note = ""
    if args.category:
        key = args.category.lower()
        if key not in CATEGORY_PROMPTS:
            print(f"error: unknown category '{args.category}'", file=sys.stderr)
            print("valid: " + ", ".join(sorted(CATEGORY_PROMPTS)), file=sys.stderr)
            return 1
        category_note = f"> Category: {key} - {CATEGORY_PROMPTS[key]}\n"

    voice_note = args.voice or "match the brand (see references/voice-and-tone-matrix.md)"

    content = TEMPLATE.format(
        product=args.product,
        voice_note=voice_note,
        category_note=category_note,
    )

    if args.out:
        Path(args.out).write_text(content, encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        print(content)
    return 0


if __name__ == "__main__":
    sys.exit(main())
