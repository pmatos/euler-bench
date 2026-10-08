"""Shared parsing of an agent's structured reply and a run's meta.json.

The reply ({language, commands}, schemas/solution.schema.json) is found in
work/result.json (codex) or output.log (claude's structured_output, or a
best-effort trailing JSON object for harnesses with no schema flag).
"""

from __future__ import annotations

import json
import re
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


def load_valid_answer(harness_dir: Path) -> tuple[dict | None, str]:
    """Return (reply, source description); reply is None if missing or schema-invalid."""
    answer, source = load_answer(harness_dir)
    if answer is None:
        return None, source
    errors = validate(answer)
    if errors:
        return None, f"{source} [SCHEMA ERROR: {'; '.join(errors)}]"
    return answer, source


def load_meta(harness_dir: Path) -> dict:
    """Parsed meta.json for a run, or {} if missing or unreadable."""
    try:
        return json.loads((harness_dir / "meta.json").read_text())
    except (OSError, json.JSONDecodeError):
        return {}


ALIASES = {
    "py": "python", "python3": "python",
    "cpp": "c++", "cxx": "c++", "cc": "c++",
    "rs": "rust",
    "golang": "go",
    "js": "javascript", "node": "javascript", "nodejs": "javascript",
    "ts": "typescript",
    "rb": "ruby",
    "hs": "haskell",
    "sh": "bash", "shell": "bash",
}


KNOWN = {"python", "c", "c++", "rust", "go", "java", "javascript", "typescript", "ruby",
         "haskell", "julia", "lua", "bash", "kotlin", "swift", "scala", "ocaml", "vow"}


def canonical_language(name: str) -> str:
    """Normalise a language name; version suffixes (python3, c++17) are dropped
    only when the remainder is a known language."""
    key = re.sub(r"\s+", " ", name.strip().lower())
    base = ALIASES.get(key, key)
    if base in KNOWN:
        return base
    stripped = re.sub(r"[\s_-]*\d+(\.\d+)*$", "", key)
    stripped = ALIASES.get(stripped, stripped)
    return stripped if stripped in KNOWN else base
