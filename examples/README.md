# Examples

Runnable samples. Use them to confirm the linter works on your machine before
you rely on it.

| File | What it is | Expected result |
| --- | --- | --- |
| `spec-sheet.txt` | Raw spec source for an 8-inch chef's knife | — |
| `sample-output-good.md` | Copy that follows the skill | **exit 0**, all checks pass |
| `sample-output-bad.md` | Every mistake in the book | **exit 1**, 10 failures |

These are deliberately kept as clean copy files — the linter treats the first
content line as the lead hook, so no explanatory header is added here.

## Try it

```bash
python scripts/validate_pdp.py examples/sample-output-good.md --specs examples/spec-sheet.txt
echo "exit=$?"   # expect 0

python scripts/validate_pdp.py examples/sample-output-bad.md
echo "exit=$?"   # expect 1

python scripts/extract_specs.py examples/spec-sheet.txt --out /tmp/checklist.md
python scripts/scaffold_pdp.py --product "8in Chef Knife" --category tools
```

## What the bad sample gets wrong

`sample-output-bad.md` fails on:

- hook is 39 words and opens with "premium quality"
- banned filler: premium quality, high-quality, revolutionary, cutting-edge,
  must-have, unparalleled
- three bullets with no bold payoff and no benefit translation
- bare "Buy now" CTA
- no Details block, so no literal numbers anywhere

Read it next to `assets/examples-before-after.md` for the annotated rewrite.
