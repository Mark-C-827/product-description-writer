# QA Scorecard

Weighted rubric for reviewing finished PDP copy. Use after
`scripts/validate_pdp.py` passes - the linter catches mechanics, this catches
judgment.

Score each item 0-2 (0 = fails, 1 = partial, 2 = solid). Weight, multiply, sum.

| # | Criterion | Weight | Score (0-2) | Weighted |
| --- | --- | --- | --- | --- |
| 1 | **Hook works standalone** - meaningful lifted out of the page | 5 | | |
| 2 | **Hook names a transformation**, not the category | 4 | | |
| 3 | **Every benefit traces to a spec** | 5 | | |
| 4 | **Specs kept are the ones buyers care about** | 3 | | |
| 5 | **Bullets front-load a distinct payoff** | 4 | | |
| 6 | **Bullet payoffs are varied**, not four versions of "durable" | 3 | | |
| 7 | **Every sentence under 20 words** | 2 | | |
| 8 | **Objections pre-answered honestly** | 4 | | |
| 9 | **Details block is complete** - every literal number present | 3 | | |
| 10 | **Details block has no marketing language** | 2 | | |
| 11 | **Voice matches the brand** | 3 | | |
| 12 | **CTA restates a benefit** | 2 | | |
| 13 | **No unsupported claim survives** | 5 | | |
| 14 | **Nothing padded** - no sentence exists to add length | 3 | | |
| 15 | **Mobile-scannable** - bullets wrap to ≤ 3 lines on a phone | 2 | | |
| | **Total** | **50** | | **/100** |

## Interpretation

| Score | Verdict |
| --- | --- |
| 85-100 | Ship it. |
| 70-84 | Ship with the flagged fixes. |
| 55-69 | Rewrite the weak sections - usually the hook or the bullets. |
| < 55 | Back to the source. The copy is guessing. |

## Automatic fails

Any one of these and the copy does not ship, regardless of score:

- [ ] A number, certification, or material appears that the source does not contain
- [ ] A health, safety, or earnings outcome claim
- [ ] Fabricated scarcity or urgency
- [ ] The hook is a generic category claim ("premium quality", "high-quality")
- [ ] A known real objection is dodged rather than answered

## The three questions that matter most

If you only have two minutes, ask these:

1. **Could the first line alone make someone want this?**
   It is the only thing many shoppers read.

2. **Is there any sentence a disappointed customer could quote back at the
   merchant?** If yes, cut it or prove it.

3. **What did you leave out, and was that the right call?**
   A page that answers everything is a page nobody finishes. A page that omits
   the dealbreaker is a page that gets returned.

## Common deductions

| Issue | Deduct from |
| --- | --- |
| Hook is a feature restated as a benefit | #2 |
| A bullet is two ideas jammed together | #5 |
| Objection buried in Details instead of answered | #8 |
| Voice drifts between sections | #11 |
| Bullet repeats a payoff already used | #6 |
| Adjectives doing a number's job | #3, #14 |
