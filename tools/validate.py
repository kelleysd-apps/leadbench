#!/usr/bin/env python3
"""validate.py — forker-facing setup linter for LeadBench.

This is NOT a leak scanner (see leakscan.py for that). It checks whether a
fresh fork/clone has been configured yet: which of the five brain/*.md
market files are still unfilled, whether active-focus/focus.md is filled,
and what <PLACEHOLDER_TOKEN>-style tokens still need attention.

Usage:
    python3 tools/validate.py [--strict]

Exit code:
    Always 0, unless --strict is passed, in which case it exits 1 if
    anything is still unfilled/unconfigured (useful for a forker's own CI
    once they've filled things in and want a hard gate).

Standard library only. No third-party dependencies.
"""

from __future__ import annotations

import argparse
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)

BRAIN_DIR = os.path.join(REPO_ROOT, "brain")
FOCUS_PATH = os.path.join(REPO_ROOT, "active-focus", "focus.md")

# The five market-fill files documented in the project's CLAUDE.md contract:
# vertical profile, ICP, positioning, offer, voice.
EXPECTED_BRAIN_FILES = [
    "vertical-profile.md",
    "icp.md",
    "positioning.md",
    "offer.md",
    "voice.md",
]

# Two conventions are used across this template for "not yet filled in":
#   1. `<FILL: description>` placeholder markers inline
#   2. a bare `TODO` marker
#   3. YAML-ish frontmatter line `status: unfilled`
# We code defensively against all three since, at the time this script was
# written, brain/ and active-focus/ were empty in the target repo and the
# actual authoring convention for shipped template files was not yet fixed.
UNFILLED_MARKERS = [
    re.compile(r"<FILL:[^>]*>"),
    re.compile(r"\bTODO\b"),
    re.compile(r"^status:\s*unfilled\s*$", re.MULTILINE),
]

PLACEHOLDER_TOKEN_RE = re.compile(r"<[A-Z][A-Z0-9_]+>")

SKIP_DIR_NAMES = {".git", "node_modules"}


def file_is_unfilled(path: str) -> bool:
    """A file counts as unfilled if it doesn't exist, is empty, or contains
    any of the recognized "not yet configured" markers."""
    if not os.path.exists(path):
        return True
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            content = fh.read()
    except OSError:
        return True
    if not content.strip():
        return True
    return any(marker.search(content) for marker in UNFILLED_MARKERS)


def check_brain_files() -> tuple[int, int, list[str]]:
    """Returns (filled_count, total_count, unfilled_filenames)."""
    unfilled = []
    for filename in EXPECTED_BRAIN_FILES:
        path = os.path.join(BRAIN_DIR, filename)
        if file_is_unfilled(path):
            unfilled.append(filename)
    filled_count = len(EXPECTED_BRAIN_FILES) - len(unfilled)
    return filled_count, len(EXPECTED_BRAIN_FILES), unfilled


def check_focus() -> bool:
    """Returns True if active-focus/focus.md is filled."""
    return not file_is_unfilled(FOCUS_PATH)


def find_placeholder_tokens(root: str) -> dict[str, list[tuple[int, str]]]:
    """Scan the repo for <PLACEHOLDER_TOKEN> style tokens, grouped by file."""
    findings: dict[str, list[tuple[int, str]]] = {}
    for current_root, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIR_NAMES and not d.startswith(".")]
        for filename in filenames:
            path = os.path.join(current_root, filename)
            try:
                with open(path, "rb") as fh:
                    if b"\x00" in fh.read(8192):
                        continue
            except OSError:
                continue
            try:
                with open(path, "r", encoding="utf-8", errors="replace") as fh:
                    for line_number, line in enumerate(fh, start=1):
                        for match in PLACEHOLDER_TOKEN_RE.finditer(line):
                            rel_path = os.path.relpath(path, root)
                            findings.setdefault(rel_path, []).append((line_number, match.group(0)))
            except OSError:
                continue
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Forker-facing setup linter for LeadBench: reports which brain/*.md "
            "market files, active-focus/focus.md, and <PLACEHOLDER_TOKEN> markers "
            "still need to be filled in before the fork is ready to run."
        )
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 if anything is unfilled/unconfigured (default: always exit 0)",
    )
    args = parser.parse_args()

    anything_unfilled = False

    print("LeadBench setup check")
    print("======================")
    print()

    filled_count, total_count, unfilled_files = check_brain_files()
    print(f"{'✓' if filled_count == total_count else '✗'} {filled_count} of {total_count} brain files filled")
    if unfilled_files:
        anything_unfilled = True
        for filename in unfilled_files:
            print(f"    - brain/{filename} is unfilled")
    print()

    focus_filled = check_focus()
    if focus_filled:
        print("✓ active-focus/focus.md is filled")
    else:
        anything_unfilled = True
        print("✗ active-focus/focus.md is unfilled — start here")
    print()

    tokens = find_placeholder_tokens(REPO_ROOT)
    if tokens:
        anything_unfilled = True
        total_tokens = sum(len(v) for v in tokens.values())
        print(f"✗ {total_tokens} placeholder token(s) remaining across {len(tokens)} file(s):")
        for rel_path in sorted(tokens):
            print(f"  {rel_path}")
            for line_number, token in sorted(set(tokens[rel_path])):
                print(f"    - line {line_number}: {token}")
    else:
        print("✓ no <PLACEHOLDER_TOKEN> markers remaining")
    print()

    if anything_unfilled:
        print("Next step: fill in active-focus/focus.md first, then the brain/ files.")
    else:
        print("Setup looks complete.")

    if args.strict and anything_unfilled:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
