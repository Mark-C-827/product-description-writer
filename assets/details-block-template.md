# Details Block Template

Where literal facts live. Its job: let a spec-hunter verify everything without
the sell above it getting cluttered.

## Rules

- **Complete.** Every number, dimension, material, and care instruction from the
  source appears here, even if it also appears above.
- **Consistent units.** Pick a system and hold it. Dual units only if the
  merchant's market needs both.
- **No marketing language.** No adjectives, no benefits, no persuasion here.
- **Labeled rows.** Shoppers skim labels, not prose.
- **Ordered by decision weight.** Put what they check first at the top.

## Standard layout

| Spec | Value |
| --- | --- |
| Dimensions | <L> × <W> × <H> <unit> |
| Weight | <value> <unit> |
| Material | <material>, <% if known> |
| Finish | <finish> |
| Color | <color name> |
| Capacity / size | <value> <unit> |
| Compatibility | <exact models / standards> |
| Power / battery | <value> <unit> <conditions> |
| Rating | <value> (<standard named>) |
| Care | <instruction in words> |
| Warranty | <length and terms> |
| What's in the box | <items> |
| Origin | <country, only if verified> |

Delete rows that do not apply. Add rows the category needs - see
`references/category-playbooks.md`.

## Ordering by category

| Category | Lead the block with |
| --- | --- |
| Apparel | Size / measurements, then fabric %, then care |
| Electronics | Compatibility, then battery, then ports, then dimensions |
| Beauty | Volume, then key actives with %, then usage |
| Home | Dimensions, then materials, then assembly |
| Food | Net weight, then ingredients, then allergens, then storage |
| Tools | Material / hardness, then ratings, then dimensions |
| Outdoor | Ratings with standard, then weight, then packed size |
| Auto | Fitment list, then material, then ratings |
| Jewelry | Metal and purity, then stone specs, then dimensions |
| Baby | Age / weight range, then materials, then named standards |
| Digital | Platform support, then limits, then terms |

## Care instructions

Write them in words, not symbols. A shopper scanning on a phone should not have
to decode a laundry glyph.

- Weak: "30°C M/C wash, no tumble"
- Strong: "Machine wash cold at 30°C. Do not tumble dry."

## What to do with specs you cannot verify

Leave them out of the Details block and note them in **Notes to merchant**.
An incomplete Details block is recoverable; a wrong one is a refund.

## Anti-patterns

| Anti-pattern | Fix |
| --- | --- |
| Benefits in the Details block | Move them up to bullets |
| "Approx." on everything | Give the real number, or say why it varies |
| Mixed units | Standardize |
| Empty rows left in the table | Delete or fill |
| Care given as symbols only | Write it out |
| Marketing copy repeated at the bottom | Delete |
