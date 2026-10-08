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

import json
import sys
from pathlib import Path

REQUIRED_FIELDS = ("language", "commands")


def validate(obj) -> list[str]:
    """Return schema-violation messages for obj against solution.schema.json (empty if valid)."""
    if not isinstance(obj, dict):
        return ["not a JSON object"]
    errors = []
    for key in REQUIRED_FIELDS:
        if key not in obj:
            errors.append(f"missing '{key}'")
    if "language" in obj and not isinstance(obj["language"], str):
        errors.append("'language' is not a string")
    cmds = obj.get("commands")
    if "commands" in obj:
        if not isinstance(cmds, list) or not all(isinstance(c, str) for c in cmds):
            errors.append("'commands' is not a list of strings")
        elif not cmds:
            errors.append("'commands' is empty")
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

    # claude --output-format json: a single-line JSON object on stdout, with the
    # schema-validated reply under "structured_output". The container runtime
    # may print warnings around it (stderr is merged into the log), so look at
    # each line rather than the whole file.
    for line in reversed(log_text.splitlines()):
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            envelope = json.loads(line)
        except json.JSONDecodeError:
            continue
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
            rows.append((h.name, "-", "no reply", "-", source))
            continue
        errors = validate(answer)
        if errors:
            rows.append((h.name, "-", "invalid reply", "-",
                         f"{source} [SCHEMA ERROR: {'; '.join(errors)}]"))
            continue
        verify = None
        meta = h / "meta.json"
        if meta.is_file():
            try:
                verify = json.loads(meta.read_text()).get("verify")
            except json.JSONDecodeError:
                pass
        if not verify:
            status, value = "not verified", "-"
        elif verify.get("timed_out"):
            status, value = "timeout", "-"
        elif verify.get("exit_code") == 0:
            status, value = "ok", verify.get("answer") or "-"
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

    answers = {r[3] for r in rows if r[2] == "ok" and r[3] != "-"}
    if len(answers) > 1:
        print(f"\nMISMATCH: harnesses disagree on the answer: {sorted(answers)}")
    elif len(answers) == 1:
        print(f"\nAll harnesses with an answer agree: {next(iter(answers))}")
    else:
        print("\nNo harness produced a successful run with an answer.")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
