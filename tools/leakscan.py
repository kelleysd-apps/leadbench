#!/usr/bin/env python3
"""leakscan.py — scan a directory tree for patterns that should never reach
a public repo (infra identifiers, operator identity, secrets, PII shapes).

Patterns live in tools/denylist.txt (committed, structural regexes only)
and, optionally, tools/denylist.local.txt (gitignored, operator-private
literal names/emails). Both are merged before scanning.

Usage:
    python3 tools/leakscan.py [TARGET_DIR] [--verbose] [--json]

Exit code:
    0 if no hits, 1 if any hits (or on a fatal error loading the denylist).

Standard library only. No third-party dependencies.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DENYLIST_PATH = os.path.join(SCRIPT_DIR, "denylist.txt")
DENYLIST_LOCAL_PATH = os.path.join(SCRIPT_DIR, "denylist.local.txt")

# Files this scanner must never treat as scan targets: itself and the
# denylist(s) it loads. If these were scanned, every pattern would match
# its own source line.
SELF_SKIP_BASENAMES = {
    os.path.basename(__file__),
    "denylist.txt",
    "denylist.local.txt",
}

SKIP_DIR_NAMES = {".git"}


@dataclass
class Pattern:
    section: str
    label: str
    regex: re.Pattern
    source_file: str


@dataclass
class Hit:
    path: str
    line_number: int
    section: str
    label: str
    matched_text: str


def load_denylist(path: str) -> list[Pattern]:
    """Parse a denylist file into a list of compiled Pattern objects.

    Format: one regex per line. `#` starts a comment. A comment line of the
    form `## Section Name` starts a new section; comment lines are also
    used as the human-readable label for the pattern immediately following
    them (falls back to a truncated form of the pattern itself).
    """
    patterns: list[Pattern] = []
    if not os.path.exists(path):
        return patterns

    section = "uncategorized"
    pending_label: str | None = None

    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        for raw_line in fh:
            line = raw_line.rstrip("\n")
            stripped = line.strip()

            if not stripped:
                pending_label = None
                continue

            if stripped.startswith("## "):
                section = stripped[3:].strip()
                pending_label = None
                continue

            if stripped.startswith("#"):
                # Plain comment: remember as the label for the next pattern.
                comment_text = stripped.lstrip("#").strip()
                if comment_text:
                    pending_label = comment_text
                continue

            # Otherwise this is a pattern line.
            try:
                regex = re.compile(stripped)
            except re.error as exc:
                print(
                    f"warning: skipping invalid regex in {path}: {stripped!r} ({exc})",
                    file=sys.stderr,
                )
                pending_label = None
                continue

            label = pending_label or (stripped if len(stripped) <= 40 else stripped[:37] + "...")
            patterns.append(Pattern(section=section, label=label, regex=regex, source_file=path))
            pending_label = None

    return patterns


def check_public_denylist_for_literals() -> list[str]:
    """Guard against the exact mistake that caused a prior leak: someone
    pastes a literal identifier into the PUBLIC denylist.txt instead of
    the private denylist.local.txt.

    We can't know what counts as a "literal" in general, but we do know
    the operator's own private literal list: tools/denylist.local.txt.
    Any non-comment line in denylist.local.txt that also appears verbatim
    as a non-comment line in denylist.txt means a literal has leaked into
    the public file. Returns the list of offending lines (empty if clean
    or if denylist.local.txt doesn't exist).
    """
    if not os.path.exists(DENYLIST_LOCAL_PATH):
        return []

    def pattern_lines(path: str) -> set[str]:
        lines: set[str] = set()
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            for raw_line in fh:
                stripped = raw_line.strip()
                if not stripped or stripped.startswith("#"):
                    continue
                lines.add(stripped)
        return lines

    public_lines = pattern_lines(DENYLIST_PATH)
    local_lines = pattern_lines(DENYLIST_LOCAL_PATH)

    return sorted(public_lines & local_lines)


def is_binary(path: str, sample_size: int = 8192) -> bool:
    try:
        with open(path, "rb") as fh:
            chunk = fh.read(sample_size)
    except OSError:
        return True
    return b"\x00" in chunk


def mask(text: str, verbose: bool) -> str:
    if verbose:
        return text
    if len(text) <= 4:
        return text[:4] + "***"
    return text[:4] + "***"


def iter_target_files(target_dir: str):
    for root, dirnames, filenames in os.walk(target_dir):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIR_NAMES]
        for filename in filenames:
            if filename in SELF_SKIP_BASENAMES:
                continue
            full_path = os.path.join(root, filename)
            yield full_path


def scan(target_dir: str, patterns: list[Pattern]) -> list[Hit]:
    hits: list[Hit] = []
    for path in iter_target_files(target_dir):
        if is_binary(path):
            continue
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                for line_number, line in enumerate(fh, start=1):
                    for pattern in patterns:
                        match = pattern.regex.search(line)
                        if match:
                            hits.append(
                                Hit(
                                    path=os.path.relpath(path, target_dir),
                                    line_number=line_number,
                                    section=pattern.section,
                                    label=pattern.label,
                                    matched_text=match.group(0),
                                )
                            )
        except OSError as exc:
            print(f"warning: could not read {path}: {exc}", file=sys.stderr)
    return hits


def main() -> int:
    default_target = os.path.dirname(SCRIPT_DIR)  # repo root = parent of tools/
    parser = argparse.ArgumentParser(
        description=(
            "Scan a directory for leaked infra identifiers, operator identity, "
            "secrets, and PII shapes, using tools/denylist.txt (+ optional "
            "tools/denylist.local.txt)."
        )
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=default_target,
        help="Directory to scan (default: repo root, the parent of tools/)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show full matched text instead of masking it (first 4 chars + ***)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON instead of human-readable text",
    )
    args = parser.parse_args()

    if not os.path.isdir(args.target):
        print(f"error: target directory does not exist: {args.target}", file=sys.stderr)
        return 1

    leaked_literals = check_public_denylist_for_literals()
    if leaked_literals:
        print(
            "error: tools/denylist.txt (PUBLIC) contains line(s) that also "
            "appear in tools/denylist.local.txt (PRIVATE). That means a "
            "literal identifier has been committed to the public denylist "
            "instead of kept in the private one — this discloses the very "
            "thing the denylist exists to protect. Move these line(s) out "
            "of tools/denylist.txt and into tools/denylist.local.txt:",
            file=sys.stderr,
        )
        for line in leaked_literals:
            print(f"  {line}", file=sys.stderr)
        return 1

    patterns = load_denylist(DENYLIST_PATH)
    patterns += load_denylist(DENYLIST_LOCAL_PATH)

    if not patterns:
        print(f"error: no patterns loaded from {DENYLIST_PATH}", file=sys.stderr)
        return 1

    hits = scan(args.target, patterns)

    # Summary count by section.
    section_counts: dict[str, int] = {}
    for hit in hits:
        section_counts[hit.section] = section_counts.get(hit.section, 0) + 1

    if args.json:
        payload = {
            "target": args.target,
            "hit_count": len(hits),
            "section_counts": section_counts,
            "hits": [
                {
                    "path": h.path,
                    "line": h.line_number,
                    "section": h.section,
                    "pattern": h.label,
                    "matched": h.matched_text if args.verbose else mask(h.matched_text, False),
                }
                for h in hits
            ],
        }
        print(json.dumps(payload, indent=2))
    else:
        for h in hits:
            shown = mask(h.matched_text, args.verbose)
            print(f"{h.path}:{h.line_number}: [{h.label}] {shown}")

        print()
        print(f"leakscan: {len(hits)} hit(s) in {args.target}")
        if section_counts:
            print("by section:")
            for section, count in sorted(section_counts.items(), key=lambda kv: -kv[1]):
                print(f"  {section}: {count}")

        if not hits:
            print("clean — no denylist matches found.")

    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
