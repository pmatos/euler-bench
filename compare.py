#!/usr/bin/env python3
"""Compare structured answers across harnesses for one problem run.

Reads each harness's schema-validated final answer (schemas/answer.schema.json:
{language, answer, code}) and prints a side-by-side table, so results from
different harnesses/models are comparable without depending on file-writing
conventions.

Usage:
    uv run python compare.py <run_root>/<problem-dir>

    e.g. uv run python compare.py runs/20260911-114621/problem-1
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REQUIRED_FIELDS = ("language", "answer", "code")


def validate(obj) -> list[str]:
    """Return schema-violation messages for obj against answer.schema.json (empty if valid)."""
    if not isinstance(obj, dict):
        return ["not a JSON object"]
    errors = []
    for key in REQUIRED_FIELDS:
        if key not in obj:
            errors.append(f"missing '{key}'")
        elif not isinstance(obj[key], str):
            errors.append(f"'{key}' is not a string")
    extra = set(obj) - set(REQUIRED_FIELDS)
    if extra:
        errors.append(f"unexpected field(s): {', '.join(sorted(extra))}")
    return errors


def extract_trailing_json(text: str) -> dict | None:
    """Best-effort: find the last top-level {...} object in free-form text.

    Used for harnesses with no schema-enforcement flag (e.g. oh-my-pi), where
    the model was only asked in the prompt to end with a JSON object.
    """
    depth = 0
    end = None
    start = None
    for i in range(len(text) - 1, -1, -1):
        c = text[i]
        if c == "}":
            if depth == 0:
                end = i + 1
            depth += 1
        elif c == "{":
            depth -= 1
            if depth == 0:
                start = i
                break
    if start is None or end is None:
        return None
    try:
        return json.loads(text[start:end])
    except json.JSONDecodeError:
        return None


def load_answer(harness_dir: Path) -> tuple[dict | None, str]:
    """Return (answer_dict_or_None, description of where it came from)."""
    result_json = harness_dir / "work" / "result.json"
    if result_json.is_file():
        try:
            return json.loads(result_json.read_text()), "work/result.json"
        except json.JSONDecodeError as exc:
            return None, f"work/result.json (invalid JSON: {exc})"

    log_path = harness_dir / "output.log"
    if not log_path.is_file():
        return None, "no output.log or result.json"

    log_text = log_path.read_text(errors="replace")

    # claude --output-format json: single JSON object on stdout, with the
    # schema-validated reply under "structured_output".
    stripped = log_text.strip()
    if stripped.startswith("{"):
        try:
            envelope = json.loads(stripped)
        except json.JSONDecodeError:
            envelope = None
        if isinstance(envelope, dict) and "structured_output" in envelope:
            return envelope["structured_output"], "output.log (structured_output)"

    # Best-effort fallback for harnesses with no schema enforcement: scan for
    # a trailing JSON object.
    found = extract_trailing_json(log_text)
    if found is not None:
        return found, "output.log (best-effort trailing JSON)"

    return None, "no structured answer found in output.log"


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
    for h in harness_dirs:
        answer, source = load_answer(h)
        if answer is None:
            rows.append((h.name, "-", "-", "-", source))
            continue
        errors = validate(answer)
        language = answer.get("language", "?") if isinstance(answer, dict) else "?"
        value = answer.get("answer", "?") if isinstance(answer, dict) else "?"
        code_len = f"{len(answer.get('code', ''))} chars" if isinstance(answer, dict) else "-"
        status = source if not errors else f"{source} [SCHEMA ERROR: {'; '.join(errors)}]"
        rows.append((h.name, language, value, code_len, status))

    header = ("harness", "language", "answer", "code", "source")
    widths = [max(len(str(r[i])) for r in [header, *rows]) for i in range(len(header))]

    def fmt(row) -> str:
        return "  ".join(str(c).ljust(w) for c, w in zip(row, widths))

    print(fmt(header))
    print(fmt(tuple("-" * w for w in widths)))
    for row in rows:
        print(fmt(row))

    answers = {r[2] for r in rows if r[2] != "-"}
    if len(answers) > 1:
        print(f"\nMISMATCH: harnesses disagree on the answer: {sorted(answers)}")
    elif len(answers) == 1:
        print(f"\nAll harnesses with an answer agree: {next(iter(answers))}")
    else:
        print("\nNo harness produced a parseable structured answer.")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
