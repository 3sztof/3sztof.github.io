#!/usr/bin/env python3
"""
Guard: reject NEW em-dashes (U+2014) in changed lines.

This blog's house style uses ' - ' (space-hyphen-space) instead of em-dashes,
and avoids the "AI wall of text" tell that em-dashes have become. This script
is diff-aware: it only flags em-dashes on lines being ADDED, so it prevents
regressions without failing on untouched lines (e.g. vendored theme content).

Modes:
  Pre-commit (default): reads `git diff --cached` from the working tree.
  CI (--stdin):         reads a unified diff piped to stdin, produced by the
                        caller with e.g.:
                          git diff "$BASE"...HEAD --unified=0 | python3 check_no_em_dash.py --stdin

Usage:
    check_no_em_dash.py              # pre-commit mode (staged diff)
    check_no_em_dash.py --stdin      # CI mode (diff on stdin)

Exit codes:
  0 - no new em-dashes
  1 - one or more added lines contain an em-dash
"""

from __future__ import annotations

import subprocess
import sys

EM_DASH = "\u2014"


def _scan_diff(diff_text: str) -> list[str]:
    """Return added lines containing an em-dash as '<file>: <line>' strings."""
    findings: list[str] = []
    current_file = "?"
    for line in diff_text.splitlines():
        if line.startswith("+++ b/"):
            current_file = line[len("+++ b/") :]
            continue
        if line.startswith(("+++", "---")):
            continue
        if line.startswith("+") and EM_DASH in line:
            findings.append(f"{current_file}: {line[1:].strip()}")
    return findings


def added_lines_with_em_dash(stdin_mode: bool) -> list[str]:
    if stdin_mode:
        return _scan_diff(sys.stdin.read())
    diff = subprocess.run(
        ["git", "diff", "--cached", "--unified=0", "--no-color"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    return _scan_diff(diff)


def main() -> int:
    stdin_mode = "--stdin" in sys.argv
    findings = added_lines_with_em_dash(stdin_mode)
    if not findings:
        return 0
    print("Em-dash (\u2014) found in newly added lines. Use ' - ' or reword:\n")
    for f in findings:
        print(f"  {f}")
    print(
        "\nEm-dashes are prohibited in this blog's prose. "
        "Replace with ' - ' (space-hyphen-space), ',', ':', or restructure the sentence."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
