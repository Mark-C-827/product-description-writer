# PDP Structure Playbook

How a shopper actually reads a product page, and what each section owes them.

## The reading pattern

Shoppers do not read PDPs. They **scan** them in an F-pattern: across the top,
down the left edge, across again partway down. Two consequences:

1. **The first line carries disproportionate weight.** Many shoppers read only
   the hook. It must survive alone - lifted out of the page, pasted into a
   search result, still meaningful.
2. **The left edge of each bullet carries the message.** Front-load the payoff
   in the first 2-4 words and bold them. A bullet whose payoff sits in word 12
   is a bullet nobody reads.

Everything below the fold is for the already-interested. Everything above it is
for the skeptical.

## Section by section

### 1. Lead hook (one line, no period required)

The core transformation or job-to-be-done. Not the category.

- Weak: "Premium Chef's Knife, 8 inch"
- Strong: "Slices a ripe tomato without crushing it"

Test: if this line appeared alone in a Google result, would a shopper
understand what changes for them? If not, rewrite.

### 2. Intro (2-3 sentences)

Bridge from hook to proof. Sentence 1 restates the transformation in context.
Sentence 2 names who it is for or the situation it fixes. Sentence 3 (optional)
sets up the bullets.

Rules: under 20 words per sentence. No backstory, no brand founding story, no
"we believe." Shoppers are not here for your origin story.

### 3. Benefit bullets (3-5)

Each one: **bold payoff** → mechanism → spec.

```
**Holds an edge through 6 months of daily use** - 61 HRC Japanese steel
resists rolling, so you sharpen twice a year instead of twice a month.
```

Rules:

- 3-5 bullets. Fewer than 3 looks thin; more than 5 and nothing is read.
- Front-load the payoff word, bold the first 2-4 words.
- One idea per bullet. Two ideas means two bullets.
- Every bullet traces to a spec. No spec, no bullet.
- Concrete over abstract: "sharpens twice a year" beats "long-lasting."
- Vary the payoff - do not write four bullets that all say "durable."

### 4. Objection handling (woven, or a "Good to know" note)

Answer the doubts that block the cart. Weave them into bullets when they fit
naturally; use a short labeled note when there are several.

The note is not a disclaimer dump. Two to four lines, in the brand's voice,
each one removing a specific fear. See `objection-library.md`.

### 5. CTA (one line)

Restate the benefit, do not issue a command.

- Weak: "Buy now."
- Strong: "Get a knife that still slices clean in a year."

### 6. Details / Specs block (bottom)

The literal record: every number, dimension, material, weight, capacity,
compatibility, care instruction, and what's in the box.

This is where spec-hunters go. Its job is to be complete and findable so the
sell above it can stay clean. If a number matters to the purchase decision, it
appears here even if it also appears above.

Layout: labeled rows, consistent units, no marketing language. See
`assets/details-block-template.md`.

## Mobile-first constraints

Most PDP traffic is a phone. Write for it:

- Bullets that wrap to 3+ lines on a 375px screen are too long.
- Lead with the payoff because truncation cuts the tail.
- Put the Details block behind a disclosure only if the platform does it;
  otherwise keep it visible but compact.
- Assume the shopper is distracted and has a thumb on the back button.

## Length guidance

There is no word count that converts. There is a length at which the page
stops answering questions and starts asking for patience. As a working range:

| Page type | Typical total |
| --- | --- |
| Simple / low-consideration | 80-150 words + specs |
| Standard | 150-250 words + specs |
| High-consideration / technical | 250-400 words + specs |

Cut rather than pad. Every sentence that does not move the shopper closer to
the cart is a sentence between them and it.

## Assembly checklist

- [ ] Hook works standalone
- [ ] Intro is 2-3 sentences, each under 20 words
- [ ] 3-5 bullets, payoff front-loaded and bold
- [ ] Bullet payoffs are varied, not redundant
- [ ] Objections answered honestly
- [ ] CTA restates a benefit
- [ ] Details block carries every literal number
- [ ] No marketing language in the Details block
