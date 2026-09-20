# Changelog

All notable changes to this skill. Version follows the `version` field in
`SKILL.md` frontmatter.

## 2.0.0 — 2026-09-20

Rebuilt as a complete four-part skill package. The original workflow, quality
bar, and Do NOT list are preserved intact; everything below is added around
them.

### Added — SKILL.md

- Input contract: required vs. load-bearing inputs, thin-source rule,
  missing-input rule
- Category routing to per-category playbooks
- Step 7 compliance pass, with a hard refuse-and-offer-alternative rule
- Step 8 self-audit, wired to `scripts/validate_pdp.py`
- "Notes to merchant" as part of the deliverable: dropped specs, unsupported
  claims, assumptions to verify
- Bundled-resources index so the agent knows what it can load

### Added — references/

- `pdp-structure-playbook.md` — F-pattern scanning, section-by-section rules,
  mobile constraints, length guidance
- `benefit-translation.md` — spec → benefit method, sentence patterns, and how
  to decide which specs to drop
- `objection-library.md` — the five universal objections plus per-category
  tables, and how to source real ones
- `voice-and-tone-matrix.md` — calibration axes, category defaults, the one
  calibrating question
- `compliance-redlines.md` — claim categories, what each requires, safe rewrites,
  regulated categories
- `category-playbooks.md` — decision axes and defaults for 11 categories

### Added — scripts/

- `validate_pdp.py` — hook, sentence length, bullet count and bold payoffs,
  number coverage against the source, banned filler, bare-CTA, Details block,
  plus claim tripwire warnings
- `extract_specs.py` — spec checklist from a raw spec sheet, so no number is
  lost between source and page
- `scaffold_pdp.py` — blank PDP skeleton, category-aware

### Added — assets/

- `pdp-output-template.md`, `input-brief-template.md`, `qa-scorecard.md`,
  `details-block-template.md`, `examples-before-after.md`

### Added — examples/

- Runnable samples: a spec sheet plus one good and one bad output that exercise
  the linter

### Changed

- README split into Chinese (`README.md`) and English (`README.en.md`)
- LICENSE restates SkillMedev's original copyright alongside the enhancements

## 1.0.0 — upstream

The original `product-description-writer` skill from
[SkillMedev/skills](https://github.com/SkillMedev/skills), MIT licensed: six-step
workflow, quality bar, deliverable spec, and Do NOT list. No changes were made
to those parts.
