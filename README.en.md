# Product Description Writer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](scripts/)
[![Zero dependencies](https://img.shields.io/badge/dependencies-none-brightgreen.svg)](scripts/)
[![Skill parts](https://img.shields.io/badge/parts-SKILL%20%2B%20refs%20%2B%20scripts%20%2B%20assets-blueviolet.svg)](#layout)

Turn a dry spec sheet into product detail page (PDP) copy that sells.

Enhanced from [SkillMedev/skills](https://github.com/SkillMedev/skills) (MIT;
the original ships as a single 3.6 KB `SKILL.md`). This version keeps the
original workflow and red lines, and completes the four parts a production
skill needs — **SKILL.md / references / scripts / assets** — adding an input
contract, category routing, a compliance pass, and executable quality checks.

## What it does

Input: a spec sheet + target customer (+ brand voice)
Output: a paste-ready PDP master block, plus notes to the merchant

```
Lead hook        the transformation, not the category
Intro            2-3 sentences, each under 20 words
Benefit bullets  3-5, bold payoff front-loaded, each traceable to a spec
Good to know     honest answers to real objections (if it runs small, say so)
CTA              restates the benefit — never a bare "Buy now"
Details          every number, dimension, material, and care instruction
Notes to merchant  specs dropped / claims unsupported / assumptions to verify
```

Governing rule: **write only what the source proves.** Performance numbers,
certifications, materials, and health or safety claims that are not in the spec
sheet do not go on the page. That is the hardest line in this skill.

## Layout

```
product-description-writer/
├── SKILL.md                       main instructions (what the agent reads)
├── references/                    loaded on demand
│   ├── pdp-structure-playbook.md    F-pattern scanning, section rules
│   ├── benefit-translation.md       spec → benefit method
│   ├── objection-library.md         the doubts that block the cart
│   ├── voice-and-tone-matrix.md     category voice calibration
│   ├── compliance-redlines.md       claim rules and safe rewrites
│   └── category-playbooks.md        decision axes for 11 categories
├── scripts/
│   ├── validate_pdp.py              lint finished copy (exit 1 on failure)
│   ├── extract_specs.py             spec checklist from a raw spec sheet
│   └── scaffold_pdp.py              blank PDP skeleton
├── assets/
│   ├── pdp-output-template.md
│   ├── input-brief-template.md
│   ├── qa-scorecard.md
│   ├── details-block-template.md
│   └── examples-before-after.md
└── examples/                      runnable samples
```

## Install

```bash
cp -r product-description-writer ~/.claude/skills/   # Claude Code
cp -r product-description-writer ~/.codex/skills/    # Codex
```

The frontmatter `name` / `description` handle trigger routing.

## Scripts (Python 3.9+, no dependencies)

```bash
python scripts/validate_pdp.py copy.md                      # lint
python scripts/validate_pdp.py copy.md --specs specs.txt    # + number coverage
python scripts/validate_pdp.py copy.md --json               # machine-readable
python scripts/extract_specs.py specs.txt --out checklist.md
python scripts/scaffold_pdp.py --category apparel --out draft.md
```

`validate_pdp.py` checks hook length, sentence length (≤ 20 words), bullet count
(3-5), bold payoffs, number coverage against the source, banned filler phrases,
bare-command CTAs, and the presence of a Details block. It also raises
**warnings for human review** on clinical claims, certifications, safety
promises, and fabricated urgency.

It is mechanical. Whether the hook is good and the benefit is real is still a
human call — use `assets/qa-scorecard.md`.

## Example prompt

> Use product-description-writer for this knife. Specs: 8 in, 316 stainless,
> 61 HRC, 15° edge, 7.4 oz, pakkawood handle, hand wash only. Target: home
> cooks tired of blades that dull in two weeks. Voice: tool specialist, no
> sentimentality.

The agent asks at most one calibrating question, writes to the structure, then
runs the quality gate itself.

## Differences from the original

| | Original | This version |
| --- | --- | --- |
| SKILL.md | single 3.6 KB file | + input contract, category routing, compliance pass, self-audit, resource index |
| references | none | 6 deep references |
| scripts | none | 3 executable scripts |
| assets | none | 5 templates + annotated examples |
| QA | by feel | executable linter + weighted scorecard |
| Compliance | one Do NOT line | dedicated redlines doc + automated warnings |

The original six-step workflow, quality bar, and Do NOT list are preserved.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) first. In short:

- Welcome: real before/after examples, uncovered categories, objections sourced
  from actual return data, linter rules that catch real failures
- Not welcome: more words in SKILL.md (detail belongs in `references/`),
  invented compliance rules, urgency tactics, third-party dependencies

Any script change must keep these two as-is — first exits 0, second exits 1:

```bash
python scripts/validate_pdp.py examples/sample-output-good.md --specs examples/spec-sheet.txt
python scripts/validate_pdp.py examples/sample-output-bad.md
```

Version history lives in [CHANGELOG.md](CHANGELOG.md).

## License

MIT. Original copyright SkillMedev; enhancements under the same terms. See
[LICENSE](LICENSE).
