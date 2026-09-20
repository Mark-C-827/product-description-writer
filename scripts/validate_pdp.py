#!/usr/bin/env python3
"""Lint finished PDP copy against the skill's quality gate.

Usage:
    python validate_pdp.py COPY.md
    python validate_pdp.py COPY.md --specs specs.txt
    python validate_pdp.py COPY.md --json          # machine-readable output

Checks (structural / mechanical):
    1.  Lead hook present and short enough to work standalone
    2.  Sentence length under the 20-word limit
    3.  Bullet count in the 3-5 range
    4.  Bullets front-load a bold payoff
    5.  Every numeric token in the source appears in the copy (--specs only)
    6.  No banned generic openers / filler phrases
    7.  CTA does not end on a bare command
    8.  A Details/Specs block exists
    9.  Unsupported-claim tripwires (health, safety, certs, urgency)

Checks 1-9 are mechanical. Judgement calls - is the hook *good*, is the benefit
real - stay with the human and assets/qa-scorecard.md.

Exit codes: 0 = pass (warnings allowed), 1 = failures found.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

MAX_SENTENCE_WORDS = 20
MAX_HOOK_WORDS = 25
MIN_BULLETS = 3
MAX_BULLETS = 5

BANNED_PHRASES = [
    r"\bpremium quality\b",
    r"\bhigh[- ]quality\b",
    r"\btop[- ]notch\b",
    r"\bbest[- ]in[- ]class\b",
    r"\bcutting[- ]edge\b",
    r"\bstate of the art\b",
    r"\bgame[- ]chang(er|ing)\b",
    r"\bmust[- ]have\b",
    r"\brevolutionary\b",
    r"\bmiracle\b",
    r"\bunparalleled\b",
    r"\bsecond to none\b",
]

# Claims that require a source. Flagged for human review, never auto-fixed.
CLAIM_TRIPWIRES = [
    (r"\bclinically (proven|tested|shown)\b", "clinical claim - requires study"),
    (r"\b(dermatologist|doctor|physician)[- ](tested|approved|recommended)\b", "endorsement - requires source"),
    (r"\b(FDA|CE|UL| Energy Star|OEKO-TEX|FCC|EN 71)\b", "certification - verify name and scope"),
    (r"\b(non[- ]?toxic|chemical[- ]free|100% safe|child[- ]safe)\b", "safety claim - requires named standard"),
    (r"\b(cures?|treats?|heals?|prevents?|reverses?)\b", "health outcome claim - remove unless lawful and sourced"),
    (r"\b(guaranteed|guarantee)\b", "guarantee claim - confirm it exists"),
    (r"\b(only \d+ left|sale ends (today|tonight)|limited time only)\b", "urgency/scarcity - confirm it is true now"),
    (r"\b(\d+x|\d+ times) (faster|stronger|better|longer)\b", "comparative claim - name the baseline"),
]

BARE_CTA = re.compile(r"^\s*(buy now|add to cart|shop now|order now|get yours)[.!]?\s*$", re.I)

SECTION_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.M)
BULLET_RE = re.compile(r"^\s*[-*+]\s+(.+)$", re.M)
BOLD_RE = re.compile(r"^\s*\*\*(.+?)\*\*")

# Split on sentence enders; keep decimals, versions, and abbreviations intact.
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])(?=\s+|$)|(?<=\.)(?=\s+[A-Z\"'(])")
NUMBER_RE = re.compile(r"\d+(?:[.,]\d+)?")
WORD_RE = re.compile(r"[A-Za-z0-9'\u2019%-]+")

DETAILS_HEADINGS = ("details", "specs", "specifications", "spec sheet", "product details", "tech specs")


@dataclass
class Result:
    failures: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    passed: list[str] = field(default_factory=list)
    stats: dict = field(default_factory=dict)

    def fail(self, msg: str) -> None:
        self.failures.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def ok(self, msg: str) -> None:
        self.passed.append(msg)


def strip_markdown(text: str) -> str:
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"`(.+?)`", r"\1", text)
    text = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", text)
    return text


def split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(])|(?<=[.!?])$", text.strip())
    return [p.strip() for p in parts if p.strip()]


def prose_blocks(text: str) -> list[str]:
    """Split copy into prose blocks, breaking on markdown structure.

    Headings, tables and rules end a block - otherwise a sentence without
    terminal punctuation (a CTA) would swallow the entire spec table and
    trip the word-limit check on content that is not prose.
    """
    blocks: list[str] = []
    buf: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        structural = (
            not line
            or line.startswith("#")
            or line.startswith("|")
            or line.startswith("```")
            or bool(BULLET_RE.match(line))
            or set(line) <= set("-=*_ ")
        )
        if structural:
            if buf:
                blocks.append(" ".join(buf))
                buf = []
            continue
        buf.append(line)
    if buf:
        blocks.append(" ".join(buf))
    return [strip_markdown(b) for b in blocks if b.strip()]


def word_count(sentence: str) -> int:
    return len(WORD_RE.findall(sentence))


def find_bullets(text: str) -> list[str]:
    return BULLET_RE.findall(text)


def find_hook(text: str) -> str:
    """First non-heading, non-empty content line."""
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("#") or line.startswith("---") or line.startswith("|"):
            continue
        if line.startswith(("-", "*", "+", ">")):
            continue
        return strip_markdown(line)
    return ""


def find_details_block(text: str) -> bool:
    for heading in SECTION_RE.findall(text):
        if heading.strip().strip("#").lower().strip() in DETAILS_HEADINGS:
            return True
    low = text.lower()
    return any(f"## {h}" in low or f"# {h}" in low for h in DETAILS_HEADINGS)


def check_hook(res: Result, hook: str) -> None:
    if not hook:
        res.fail("No lead hook found - copy must open with a standalone hook line.")
        return
    n = word_count(hook)
    res.stats["hook_words"] = n
    if n > MAX_HOOK_WORDS:
        res.fail(f"Lead hook is {n} words (max {MAX_HOOK_WORDS}): it must work standalone. -> {hook!r}")
    else:
        res.ok(f"Lead hook present ({n} words).")
    if re.match(r"^\s*(introduce|presenting|we are (proud|excited))", hook, re.I):
        res.fail("Lead hook opens like a press release, not a transformation.")


def check_sentences(res: Result, blocks: list[str]) -> None:
    longs = []
    for block in blocks:
        for s in split_sentences(block):
            n = word_count(s)
            if n > MAX_SENTENCE_WORDS:
                longs.append((n, s))
    res.stats["long_sentences"] = len(longs)
    if longs:
        for n, s in longs[:5]:
            res.fail(f"Sentence is {n} words (max {MAX_SENTENCE_WORDS}): {s[:90]}...")
    else:
        res.ok(f"All sentences under {MAX_SENTENCE_WORDS} words.")


def check_bullets(res: Result, bullets: list[str]) -> None:
    count = len(bullets)
    res.stats["bullets"] = count
    if count == 0:
        res.fail("No benefit bullets found - expected 3-5.")
        return
    if count < MIN_BULLETS:
        res.fail(f"Only {count} benefit bullets (minimum {MIN_BULLETS}).")
    elif count > MAX_BULLETS:
        res.fail(f"{count} benefit bullets (maximum {MAX_BULLETS}) - cut the weakest.")
    else:
        res.ok(f"{count} benefit bullets (in range).")

    unbolded = [b for b in bullets if not BOLD_RE.match(b)]
    if unbolded:
        res.fail(
            f"{len(unbolded)} bullet(s) do not open with a bold payoff. "
            f"First offender: {unbolded[0][:70]!r}"
        )
    else:
        res.ok("All bullets open with a bold payoff.")

    for b in bullets:
        plain = strip_markdown(b)
        if word_count(plain) < 5:
            res.warn(f"Bullet looks thin ({word_count(plain)} words): {plain[:60]!r}")


def check_banned(res: Result, text: str) -> None:
    low = text.lower()
    hits = []
    for pat in BANNED_PHRASES:
        m = re.search(pat, low)
        if m:
            hits.append(low[max(0, m.start() - 20): m.end() + 20].strip())
    if hits:
        for h in hits[:5]:
            res.fail(f"Generic filler phrase present: ...{h}...")
    else:
        res.ok("No banned generic openers.")


def check_cta(res: Result, text: str) -> None:
    if BARE_CTA.search(text.strip().splitlines()[-1] if text.strip() else ""):
        res.fail("Copy ends on a bare command CTA - restate the benefit instead.")
        return
    bare_found = False
    for line in text.splitlines():
        if BARE_CTA.search(line):
            bare_found = True
            break
    if bare_found:
        res.fail("Found a bare 'Buy now'-style CTA - restate the benefit instead.")
    else:
        res.ok("CTA is not a bare command.")


def check_details(res: Result, text: str) -> None:
    if find_details_block(text):
        res.ok("Details/Specs block present.")
    else:
        res.fail("No Details/Specs block found - literal numbers need a home.")


def check_number_coverage(res: Result, copy: str, specs: str) -> None:
    def nums(text: str) -> set[str]:
        return {n.replace(",", "") for n in NUMBER_RE.findall(text)}

    spec_nums = nums(specs)
    copy_nums = nums(copy)
    missing = sorted(spec_nums - copy_nums, key=lambda x: float(x) if _is_float(x) else 0)
    res.stats["spec_numbers"] = len(spec_nums)
    if missing:
        res.fail(
            f"{len(missing)} number(s) from the source are missing from the copy: "
            f"{', '.join(missing[:12])}"
        )
    else:
        res.ok(f"All {len(spec_nums)} source numbers present in the copy.")


def _is_float(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False


def check_claims(res: Result, text: str) -> None:
    low = text.lower()
    for pat, why in CLAIM_TRIPWIRES:
        m = re.search(pat, low)
        if m:
            snippet = low[max(0, m.start() - 25): m.end() + 25].strip()
            res.warn(f"Claim tripwire ({why}): ...{snippet}...")


def validate(copy_text: str, specs_text: str | None = None) -> Result:
    res = Result()
    blocks = prose_blocks(copy_text)

    check_hook(res, find_hook(copy_text))
    check_sentences(res, blocks)
    check_bullets(res, find_bullets(copy_text))
    check_banned(res, copy_text)
    check_cta(res, copy_text)
    check_details(res, copy_text)
    check_claims(res, copy_text)
    if specs_text:
        check_number_coverage(res, copy_text, specs_text)

    res.stats["words"] = sum(word_count(b) for b in blocks)
    return res


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate PDP copy against the skill quality gate.")
    ap.add_argument("copy", help="Path to the finished PDP copy (markdown).")
    ap.add_argument("--specs", help="Path to the raw spec sheet, to check number coverage.")
    ap.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    args = ap.parse_args()

    copy_path = Path(args.copy)
    if not copy_path.exists():
        print(f"error: file not found: {copy_path}", file=sys.stderr)
        return 1
    copy_text = copy_path.read_text(encoding="utf-8")

    specs_text = None
    if args.specs:
        specs_path = Path(args.specs)
        if not specs_path.exists():
            print(f"error: spec file not found: {specs_path}", file=sys.stderr)
            return 1
        specs_text = specs_path.read_text(encoding="utf-8")

    res = validate(copy_text, specs_text)

    if args.json:
        print(json.dumps({
            "passed": not res.failures,
            "failures": res.failures,
            "warnings": res.warnings,
            "checks_passed": res.passed,
            "stats": res.stats,
        }, indent=2))
        return 1 if res.failures else 0

    print(f"PDP copy lint: {copy_path.name}")
    print(f"  words: {res.stats.get('words', 0)} | bullets: {res.stats.get('bullets', 0)}")
    print()

    if res.passed:
        print("PASSED")
        for p in res.passed:
            print(f"  + {p}")
    print()
    if res.failures:
        print(f"FAILURES ({len(res.failures)})")
        for f in res.failures:
            print(f"  x {f}")
    else:
        print("FAILURES (0)")
    print()
    if res.warnings:
        print(f"WARNINGS - review manually ({len(res.warnings)})")
        for w in res.warnings:
            print(f"  ! {w}")
    else:
        print("WARNINGS (0)")

    print()
    print("Note: this linter is mechanical. It cannot tell you whether the hook is")
    print("good or the benefit is real - use assets/qa-scorecard.md for that.")
    return 1 if res.failures else 0


if __name__ == "__main__":
    sys.exit(main())
