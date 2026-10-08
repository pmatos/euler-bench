#!/usr/bin/env python3
"""Collect an agent's solution into a self-contained `code/` folder.

For a harness run directory (<run_root>/<problem>/<harness>/) this writes:

    code/
      <the files the agent wrote in /work, minus PROMPT.txt, the statement,
       result.json and build/dependency dirs>
      assets/          (if the problem has data files)
      solve-run.sh     the agent's commands, as a runnable script
      solve-reply.json the agent's structured reply {language, commands}
      README.md        how to run it, plus the verification result if known
                       (an agent-written README.md is kept as README.agent.md)

`solve` calls this after each run; it can also be run on existing runs:

    uv run python codeout.py out/20261008-104305/problem-1/haiku5.5
"""

from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

from compare import load_answer, validate

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
         "haskell", "julia", "lua", "bash", "kotlin", "swift", "scala", "ocaml"}


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


def statement_name(harness_dir: Path) -> str:
    meta = harness_dir / "meta.json"
    if meta.is_file():
        try:
            return Path(json.loads(meta.read_text())["problem_file"]).name
        except (json.JSONDecodeError, KeyError, TypeError):
            pass
    return f"{harness_dir.parent.name}.md"


def render_script(commands: list[str]) -> str:
    return "#!/usr/bin/env bash\nset -e\ncd \"$(dirname \"$0\")\"\n" + "\n".join(commands) + "\n"


def render_readme(title: str, answer: dict, verify: dict | None) -> str:
    lines = [f"# {title}", "", f"- Language: `{answer['language']}`"]
    if verify:
        outcome = "timed out" if verify.get("timed_out") else f"exit {verify.get('exit_code')}"
        lines.append(f"- Verified in container: {outcome}"
                     + (f", answer `{verify['answer']}`" if verify.get("answer") else ""))
    lines += ["", "Run (from this directory; the last line printed is the answer):", "", "```sh"]
    lines += answer["commands"]
    lines += ["```", "", "or simply `./solve-run.sh`.", ""]
    return "\n".join(lines)


def write_code_dir(harness_dir: Path, verify: dict | None = None
                   ) -> tuple[Path | None, dict | None, str]:
    """Write <harness_dir>/code/. Returns (code_dir, answer, note); code_dir is None on failure."""
    harness_dir = harness_dir.resolve()
    answer, source = load_answer(harness_dir)
    if answer is None:
        return None, None, source
    errors = validate(answer)
    if errors:
        return None, answer, f"{source} [SCHEMA ERROR: {'; '.join(errors)}]"

    work = harness_dir / "work"
    code_dir = harness_dir / "code"
    if code_dir.exists():
        shutil.rmtree(code_dir)
    top_skip = {"PROMPT.txt", "result.json", statement_name(harness_dir)}
    any_skip = {"__pycache__", "node_modules", ".venv", "target"}

    def ignore(d: str, names: list[str]) -> set[str]:
        skipped = any_skip & set(names)
        return skipped | (top_skip & set(names)) if Path(d) == work else skipped

    shutil.copytree(work, code_dir, ignore=ignore, symlinks=True)

    if (code_dir / "README.md").exists():
        (code_dir / "README.md").rename(code_dir / "README.agent.md")
    (code_dir / "solve-reply.json").write_text(json.dumps(answer, indent=2) + "\n")
    run_sh = code_dir / "solve-run.sh"
    run_sh.write_text(render_script(answer["commands"]))
    run_sh.chmod(0o755)
    (code_dir / "README.md").write_text(
        render_readme(f"{harness_dir.parent.name} / {harness_dir.name}", answer, verify)
    )
    return code_dir, answer, source


def main(argv: list[str]) -> int:
    if not argv:
        print("usage: codeout.py <run_root>/<problem>/<harness> [...]", file=sys.stderr)
        return 1
    status = 0
    for arg in argv:
        harness_dir = Path(arg)
        if not harness_dir.is_dir():
            print(f"codeout: not a directory: {arg}", file=sys.stderr)
            status = 1
            continue
        verify = None
        meta = harness_dir / "meta.json"
        if meta.is_file():
            try:
                verify = json.loads(meta.read_text()).get("verify")
            except json.JSONDecodeError:
                print(f"codeout: {arg}: ignoring unreadable meta.json", file=sys.stderr)
        code_dir, _, note = write_code_dir(harness_dir, verify)
        if code_dir is None:
            print(f"codeout: {arg}: no code extracted ({note})", file=sys.stderr)
            status = 1
        else:
            print(f"{arg}: wrote {code_dir}")
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
