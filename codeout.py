#!/usr/bin/env python3
"""Extract a run's structured answer into a ready-to-run `code/` folder.

For a harness run directory (<run_root>/<problem>/<harness>/) this writes:

    code/
      solution.<ext>   the solution source from the schema-validated answer
      answer.json      the raw {language, answer, code} object
      README.md        how to build/run it (python command, gcc + run, ...)
      assets/          copied from the work dir when the problem has data files

`solve` calls this after every run; it can also be run on existing runs:

    uv run python codeout.py out/20261008-104305/problem-1/haiku5.5
"""

from __future__ import annotations

import json
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

from compare import load_answer, validate


@dataclass(frozen=True)
class Lang:
    ext: str
    steps: tuple[str, ...]
    requires: str


LANGS: dict[str, Lang] = {
    "python": Lang(".py", ("python3 {file}",), "python3"),
    "c": Lang(".c", ("gcc -O2 -o solution {file} -lm", "./solution"), "gcc"),
    "c++": Lang(".cpp", ("g++ -O2 -std=c++17 -o solution {file}", "./solution"), "g++"),
    "rust": Lang(".rs", ("rustc -O -o solution {file}", "./solution"), "rustc"),
    "go": Lang(".go", ("go run {file}",), "go"),
    "java": Lang(".java", ("javac {file}", "java {class_name}"), "a JDK (javac, java)"),
    "javascript": Lang(".js", ("node {file}",), "node"),
    "typescript": Lang(".ts", ("npx tsx {file}",), "node + npx"),
    "ruby": Lang(".rb", ("ruby {file}",), "ruby"),
    "haskell": Lang(".hs", ("ghc -O2 -o solution {file}", "./solution"), "ghc"),
    "julia": Lang(".jl", ("julia {file}",), "julia"),
    "perl": Lang(".pl", ("perl {file}",), "perl"),
    "lua": Lang(".lua", ("lua {file}",), "lua"),
    "bash": Lang(".sh", ("bash {file}",), "bash"),
}

ALIASES = {
    "py": "python", "python3": "python", "python2": "python", "cpython": "python",
    "cpp": "c++", "cxx": "c++", "cc": "c++",
    "rs": "rust",
    "golang": "go",
    "js": "javascript", "node": "javascript", "nodejs": "javascript",
    "ts": "typescript",
    "rb": "ruby",
    "hs": "haskell",
    "sh": "bash", "shell": "bash",
}


def canonical_language(name: str) -> str:
    key = re.sub(r"\s+", " ", name.strip().lower())
    key = re.sub(r"[\s_-]*\d+(\.\d+)*$", "", key)
    return ALIASES.get(key, key)


def java_class_name(code: str) -> str:
    m = re.search(r"public\s+(?:final\s+|abstract\s+)*class\s+(\w+)", code)
    return m.group(1) if m else "Main"


def render_readme(title: str, language: str, answer: str, filename: str,
                  lang: Lang | None, has_assets: bool, class_name: str) -> str:
    lines = [f"# {title}", "", f"- Language: `{language}`", f"- Reported answer: `{answer}`", ""]
    if lang is None:
        lines += [f"No run recipe is known for `{language}`. The source is in `{filename}`.", ""]
    else:
        lines += [f"Requires: {lang.requires}", "", "Run from this directory:", "", "```sh"]
        lines += [s.format(file=filename, class_name=class_name) for s in lang.steps]
        lines += ["```", ""]
    if has_assets:
        lines += ["`assets/` holds the problem's data files; keep it next to the source.", ""]
    return "\n".join(lines)


def write_code_dir(harness_dir: Path, title: str | None = None) -> tuple[Path | None, dict | None, str]:
    """Write <harness_dir>/code/. Returns (code_dir, answer, note); code_dir is None on failure."""
    answer, source = load_answer(harness_dir)
    if answer is None:
        return None, None, source
    errors = validate(answer)
    if errors:
        return None, answer, f"{source} [SCHEMA ERROR: {'; '.join(errors)}]"

    code_dir = harness_dir / "code"
    if code_dir.exists():
        shutil.rmtree(code_dir)
    code_dir.mkdir()

    language = answer["language"]
    lang = LANGS.get(canonical_language(language))
    class_name = java_class_name(answer["code"]) if lang and lang.ext == ".java" else ""
    if lang is None:
        filename = "solution.txt"
    elif class_name:
        filename = f"{class_name}.java"
    else:
        filename = f"solution{lang.ext}"

    code = answer["code"]
    (code_dir / filename).write_text(code if code.endswith("\n") else code + "\n")
    (code_dir / "answer.json").write_text(json.dumps(answer, indent=2) + "\n")

    work_assets = harness_dir / "work" / "assets"
    has_assets = work_assets.is_dir()
    if has_assets:
        shutil.copytree(work_assets, code_dir / "assets")

    harness_dir = harness_dir.resolve()
    title = title or f"{harness_dir.parent.name} / {harness_dir.name}"
    (code_dir / "README.md").write_text(
        render_readme(title, language, answer["answer"], filename, lang, has_assets, class_name)
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
        code_dir, _, note = write_code_dir(harness_dir)
        if code_dir is None:
            print(f"codeout: {arg}: no code extracted ({note})", file=sys.stderr)
            status = 1
        else:
            print(f"{arg}: wrote {code_dir}")
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
