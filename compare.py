#!/usr/bin/env python3
"""Compare solutions across harnesses for one problem run.

Reads each harness's schema-validated final reply (schemas/solution.schema.json:
{language, commands}) plus the verification result recorded by `solve` in
meta.json, and prints a side-by-side table. A harness succeeded when its
commands exited 0 in the verification container; the answer shown is the last
line they printed.

Usage:
    uv run python compare.py <run_root>/<problem-dir>

    e.g. uv run python compare.py runs/20260911-114621/problem-1
"""

from __future__ import annotations

import sys
from pathlib import Path

from reply import load_meta, load_valid_answer

def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print("usage: compare.py <run_root>/<problem-dir>", file=sys.stderr)
        return 1

    problem_dir = Path(argv[0])
    if not problem_dir.is_dir():
        print(f"compare: not a directory: {problem_dir}", file=sys.stderr)
        return 1

    harness_dirs = sorted(p for p in problem_dir.iterdir() if p.is_dir())
    if not harness_dirs:
        print(f"compare: no harness subdirectories under {problem_dir}", file=sys.stderr)
        return 1

    rows = []
    answers = set()
    for h in harness_dirs:
        answer, source = load_valid_answer(h)
        if answer is None:
            rows.append((h.name, "-", "no reply", "-", source))
            continue
        verify = load_meta(h).get("verify")
        if not verify:
            status, value = "not verified", "-"
        elif verify.get("timed_out"):
            status, value = "timeout", "-"
        elif verify.get("exit_code") == 0:
            status, value = "ok", verify.get("answer") or "-"
            if verify.get("answer"):
                answers.add(verify["answer"])
        else:
            status, value = f"exit {verify.get('exit_code')}", "-"
        rows.append((h.name, answer["language"], status, value, source))

    header = ("harness", "language", "run", "answer", "source")
    widths = [max(len(str(r[i])) for r in [header, *rows]) for i in range(len(header))]

    def fmt(row) -> str:
        return "  ".join(str(c).ljust(w) for c, w in zip(row, widths))

    print(fmt(header))
    print(fmt(tuple("-" * w for w in widths)))
    for row in rows:
        print(fmt(row))

    if len(answers) > 1:
        print(f"\nMISMATCH: harnesses disagree on the answer: {sorted(answers)}")
    elif len(answers) == 1:
        print(f"\nAll harnesses with an answer agree: {next(iter(answers))}")
    else:
        print("\nNo harness produced a successful run with an answer.")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
