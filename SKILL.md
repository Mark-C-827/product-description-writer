---
name: Product Description Writer
description: >
  Writes the on-site PDP master copy - a benefit-led, scannable product detail
  page in the brand's voice - from a raw spec sheet or feature list. Use when
  you have a spec list, feature bullets, or a bare template description for one
  product and need conversion copy for its own product detail page. Produces a
  paste-ready block (hook, intro, benefit bullets, objection handling, CTA,
  Details block) plus a self-audit. Do NOT use for Amazon or marketplace
  listings - use amazon-listing-optimizer instead. Do NOT use to spin one master
  into many size/color variants - use variant-copy-scaler instead. Do NOT use
  for ad creative, email, or social copy.
version: 2.0.0
license: MIT
source: https://github.com/SkillMedev/skills/tree/main/skills/product-description-writer
---

# Product Description Writer

Translate a product's specs into on-site PDP master copy: benefit-led,
scannable, in the brand's voice, decidable in eight seconds on a phone.

The job is not to describe the product. It is to remove the reasons a shopper
does not add to cart - while staying strictly inside what the source proves.

## When to use

- You have a spec sheet, feature bullets, supplier copy, or a bare template
  description and need the on-site product detail page (PDP) copy.
- One product, one master page.

## When NOT to use

- Amazon / marketplace listing copy → use `amazon-listing-optimizer`.
- Generating many size / color variant descriptions from one master → use
  `variant-copy-scaler`.
- Ads, email, social, packaging, or retail sell sheets → different formats with
  different constraints; say so and hand off.

## Inputs

Required (at least the first two):

1. **Spec / feature source** - spec sheet, feature bullets, supplier blurb.
2. **Target customer** - who buys it and the job they are hiring it for.

Optional but load-bearing:

3. **Brand voice** - if unknown, infer from category and ask **exactly one**
   calibrating question (see `references/voice-and-tone-matrix.md`).
4. **Objections** - known returns reasons, sizing complaints, review themes.
5. **Category** - routes the playbook (see `references/category-playbooks.md`).

**Thin-source rule.** If the spec list is thin, ask for the one detail
competitors omit. Never pad with adjectives to fill space. A short honest page
outsells a padded one.

**Missing-input rule.** If you cannot answer "why would they buy this" from the
source, ask before writing. Guessing a benefit is a fabrication risk.

## Workflow

1. **Gather inputs.** Collect spec source, target customer, voice, objections,
   category. Ask at most one calibrating question; do not interrogate.

2. **Find the one reason they buy.** Name the core transformation or
   job-to-be-done, not the product category. "Slices a ripe tomato without
   crushing it," not "knife." This is the **lead hook** - it must work
   standalone, because many shoppers read nothing else.

3. **Translate each spec to a benefit.** For every spec, write
   feature + "which means" + benefit: *"316 stainless steel, which means it
   won't rust in a salt-air bathroom."* Keep the spec for credibility, the
   benefit for desire. Drop any feature that translates to nothing the buyer
   cares about, and log what you dropped and why.
   → Method and sentence patterns: `references/benefit-translation.md`

4. **Surface and answer objections.** Name the silent doubt - sizing, fit,
   durability, care, compatibility, returns, "will this work for me" - and give
   one reassuring line each, woven into bullets or a short "Good to know" note.
   If it runs small, say so. Honesty here prevents returns.
   → Bank of common objections: `references/objection-library.md`

5. **Assemble for the F-pattern scan.** Lead hook → 2-3 sentence intro → 3-5
   benefit bullets with the payoff front-loaded and the first 2-4 words bold →
   benefit-restating CTA → Details/Specs block at the bottom for literal
   numbers, dimensions, materials, and care.
   → Structural rules: `references/pdp-structure-playbook.md`
   → Skeleton: `assets/pdp-output-template.md`

6. **Calibrate voice.** Match sentence length, vocabulary, and warmth to the
   brand. Premium skincare is calm and precise; a snack brand is playful;
   hardware is concrete and unromantic. Never let voice beat clarity.
   → `references/voice-and-tone-matrix.md`

7. **Compliance pass.** Strip or rephrase anything that states a number,
   certification, material, health, safety, or earnings claim the source does
   not support.
   → `references/compliance-redlines.md`

8. **Self-audit before delivery.** Run the quality gate. Fix failures and
   re-run rather than shipping with caveats:
   `python scripts/validate_pdp.py <copy.md> --specs <specs.txt>`
   Then score against `assets/qa-scorecard.md`.

## Output

Produce the complete PDP master copy as **one paste-ready block**, using
`assets/pdp-output-template.md`:

- Lead hook line
- 2-3 sentence intro
- 3-5 benefit bullets (payoff front-loaded, opening words bold)
- Objection-handling lines or a "Good to know" note
- A benefit-restating CTA
- Details/Specs block containing every literal number, dimension, material,
  and care instruction from the source

Close with a short **Notes to merchant** section:

- Specs dropped and why
- Claims you could not support from the inputs
- Assumptions you made that should be verified before publishing

## Quality gate

Ship only if all of these hold:

- The first line works as a standalone hook.
- Every benefit traces to a spec in the source; every surviving spec earns
  its place.
- Sentences stay under 20 words; bullets front-load the payoff.
- Every literal number in the source appears in the Details block.
- Every pre-cart objection is answered honestly.
- No unsupported claim survives the compliance pass.

Automated checks live in `scripts/validate_pdp.py`; the human judgment checks
live in `assets/qa-scorecard.md`.

## Hard limits

- **Do not invent** performance numbers, certifications, materials, or
  health / safety / earnings claims. Use only what the source provides. If
  asked to claim an outcome the source does not support, refuse and offer a
  compliant alternative.
- **Do not open** with "premium quality," "high-quality," or any generic
  category claim.
- **Do not fabricate** scarcity, countdowns, or low-stock urgency. Urgency is
  allowed only when it is true (limited batch, seasonal, real low stock).
- **Do not keep** features that translate to no buyer benefit.
- **Do not end** with a bare "Buy now" - restate the benefit in the CTA.
- **Do not write** medical, legal, or financial outcome claims without a cited
  source in the inputs.

## Bundled resources

**Scripts** (`scripts/`)

- `validate_pdp.py` - lint the finished copy: hook presence, sentence length,
  bullet count, bold lead-ins, numbers coverage vs. source, banned phrases,
  bare-CTA check. Exit code 1 on failure.
- `extract_specs.py` - pull discrete spec lines (numbers, dimensions,
  materials, care) out of a raw spec sheet into a checklist, so nothing is
  lost between source and Details block.
- `scaffold_pdp.py` - emit a blank PDP skeleton to fill in.

**References** (`references/`)

- `pdp-structure-playbook.md` - F-pattern assembly and section-level rules
- `benefit-translation.md` - spec → benefit method and sentence patterns
- `objection-library.md` - the doubts that block the cart, with answer shapes
- `voice-and-tone-matrix.md` - category voice calibration
- `compliance-redlines.md` - claim categories, what needs proof, safe rewrites
- `category-playbooks.md` - per-category priorities (apparel, electronics,
  beauty, home, food, auto, gear)

**Assets** (`assets/`)

- `pdp-output-template.md` - the deliverable skeleton
- `input-brief-template.md` - what to collect before writing
- `qa-scorecard.md` - weighted scoring rubric
- `details-block-template.md` - spec block layout
- `examples-before-after.md` - weak vs. strong, annotated

## Credits

Enhanced from the MIT-licensed original in
[SkillMedev/skills](https://github.com/SkillMedev/skills) (v1). Structure,
workflow, and redlines preserved; added inputs contract, category routing,
compliance pass, bundled scripts, references, and templates.
