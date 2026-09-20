# Contributing

Thanks for wanting to improve this. It is a small skill with a narrow job, so
the bar for changes is simple: **make it produce better copy, without making it
longer or looser.**

## What is welcome

- **Real product examples.** Actual before/after from a real PDP beats invented
  ones. Redact what you need to; keep the specs honest.
- **Category playbooks for categories not yet covered.** Follow the shape in
  `references/category-playbooks.md`.
- **Objections collected from real data** — return reasons, support tickets,
  3-star reviews. This is the highest-value contribution available.
- **Linter rules that catch real failures.** Every rule in
  `scripts/validate_pdp.py` should exist because someone shipped a mistake.
- **Bug fixes in the scripts**, with a failing case that proves the bug.
- **Translations** of the SKILL.md or references.

## What is not welcome

- **More words in `SKILL.md`.** It is deliberately short. Detail belongs in
  `references/`. If your change makes SKILL.md longer, move the detail instead.
- **Invented compliance rules.** Claim rules in `references/compliance-redlines.md`
  must be real. If you are unsure, do not add it.
- **Copy patterns that fabricate.** No urgency tricks, no implied guarantees,
  no outcome claims. This skill's whole value is that it stays inside the source.
- **Dependency additions.** The scripts are stdlib-only Python on purpose — a
  skill that needs `pip install` is a skill nobody runs.
- **Reformatting the docs** with no content change.

## Changing SKILL.md

`SKILL.md` is loaded wholesale into an agent's context. Before adding a line,
ask whether the agent needs it every single run or only sometimes:

- Every run → `SKILL.md`
- Sometimes → `references/`, linked from SKILL.md

Keep the frontmatter `description` accurate — it is what decides whether the
skill fires at all. If you change what the skill does, change the description.

## Changing the scripts

Requirements, all of them:

- Python 3.9+, **standard library only**
- Works on Windows, macOS, and Linux
- `validate_pdp.py` must exit 0 on `examples/sample-output-good.md` and 1 on
  `examples/sample-output-bad.md`
- New checks need a sample that fails them, added to `examples/`

Run the checks before you open a PR:

```bash
python scripts/validate_pdp.py examples/sample-output-good.md --specs examples/spec-sheet.txt
python scripts/validate_pdp.py examples/sample-output-bad.md
python scripts/extract_specs.py examples/spec-sheet.txt
python scripts/scaffold_pdp.py --category apparel
```

The first must exit 0; the second must exit 1.

## Adding examples

Examples are the most-read part of this repo. For each one:

1. Say whether the product is real or illustrative.
2. Keep the specs internally consistent — the Details block must contain every
   number used above it.
3. Show the honest limitation. An example with no objection handling teaches
   the wrong lesson.
4. Annotate why the rewrite works, not just that it does.

## Submitting

1. Fork and branch.
2. Make the change.
3. Run the checks above.
4. Open a PR describing **what copy gets better** because of this. Not "updated
   docs" — what an actual page will now say differently.

If you are unsure whether a change fits, open an issue first. Cheaper than a
PR that gets argued about.

## License

Contributions are accepted under the same MIT license. See [LICENSE](LICENSE).
