# euler-bench — Project Euler problem prompts

Self-contained local snapshot of **all Project Euler problems 1–1005** (as of 2026-07-10),
one markdown prompt per problem, with every image and data file stored locally.

## Layout

```
prompts/
  problem-<N>/
    problem-<N>.md      # the problem statement
    assets/             # present only when the problem references files
      <image>.png|gif|jpg
      <data>.txt
```

- **1005** problems, one folder each.
- **214** problems have an `assets/` folder → **255 images** + **23 `.txt` data files**.
- Everything is local and relative: markdown references assets as `assets/<name>`.
  There are **no** remote resource URLs. Links to *other* problems (`problem=<N>`) remain absolute.

## How it was built

- **Bodies** come from Project Euler's clean HTML endpoint `https://projecteuler.net/minimal=<N>`,
  converted to GitHub-flavored Markdown with `pandoc`. All mathematics is preserved as LaTeX (`$...$`);
  Project Euler renders formulas as text, so images are never equations — they are diagrams,
  figures, and animations.
- **Titles** come from the archives pages (`/archives;page=<p>`) and `/recent`.
- **Assets** (images + linked `.txt` data files) were downloaded and copied into each problem's
  `assets/` folder, with the markdown rewritten to relative paths.

## Notes

- 20 of the images are animated GIFs (only the first frame renders in most markdown viewers).
- **Problem 991** ("Fruit Salad"): Project Euler's own text has a typo in the third denominator;
  the authoritative rendered equation is at `prompts/problem-991/assets/0991_fruits.png`.
  The markdown reproduces the source text faithfully (uncorrected).

Data © Project Euler contributors — see https://projecteuler.net (problems are published under
CC BY-NC-SA). This repository is an offline mirror for local use.

## Running solvers (`solve`)

`solve` runs each problem through one or more *harnesses* (claude, codex, oh-my-pi, …),
each inside its own container (docker or podman) with only a per-run work folder
bind-mounted, plus whatever host auth/config you choose to share (see below).

```
uv run python solve <config.yaml> <problem-dir> [<problem-dir> ...] [options]

# e.g.
uv run python solve config.example.yaml prompts/problem-3 prompts/problem-98
```

Options:

| flag | meaning |
|------|---------|
| `--harness NAME` | run only the named harness (repeatable); default: all in config |
| `--runtime BIN` | container runtime (`docker` or `podman`); overrides config `runtime` |
| `--runs-dir DIR` | output root (default `./runs`) |
| `-j, --jobs N` | run up to N containers concurrently (default 1) |
| `--language LANG` | force the solution language (python, c, c++, rust, go, java, …); overrides config `language` |
| `--dry-run` | assemble work dirs and print the `docker run` commands without executing |

### What happens per run

For every `(problem × harness)` pair, `solve`:

1. Creates `runs/<timestamp>/<problem>/<harness>/work/` and copies the whole
   problem folder into it (statement `.md` + `assets/`).
2. Composes the prompt (config `prompt` with `{problem}` filled in) and writes it
   to `work/PROMPT.txt`.
3. Runs `docker run --rm -v <work>:/work -w /work <image> <cmd>`.
4. Captures combined stdout+stderr to `output.log` and writes `meta.json`
   (command, exit code, duration, timeout status). Anything the solver writes
   into `/work` (solution code) stays in `work/`.

5. Parses the agent's structured reply (`schemas/solution.schema.json`):
   `{"language": ..., "commands": [...]}`. The reply holds no code. The agent
   writes its solution (one file or a whole project) in `/work` and lists the
   shell commands that build and run it.
6. **Verifies** by running those commands (`bash -e`, from `/work`) in a fresh
   container of the same image. Output goes to `verify.log`; the last line
   printed to stdout is recorded as the answer. Timeout: `verify_timeout`
   (default 600s).
7. Collects `<harness>/code/`: the agent's files (minus `PROMPT.txt` and the
   statement), `assets/`, `solve-run.sh` and a `README.md` with the
   commands. Regenerate for an existing run with
   `uv run python codeout.py <run_root>/<problem>/<harness>`.

**A run succeeds** when the agent exits 0 *and* the verification commands exit 0
(`success` in `meta.json`, counted in `summary.json`) and printed something on
stdout. The answer is not checked for correctness. Verification runs in the work dir as the agent left it,
so leftover build artifacts can mask a missing build step. Use
`compare.py <run_root>/<problem>` to see all harnesses side by side.

**Forcing the language:** set `language: c` in the config or pass `--language c`
(CLI wins). A requirement is prepended to the prompt, and `meta.json` records
`language_mismatch` (with a warning) if the model answers in another language.
The images ship `build-essential` (gcc, g++, make) next to `python3`; other
toolchains (rust, go, ...) must be added to the Dockerfiles, otherwise the agent
cannot test its code and verification fails.

**Vow:** `--language vow` is supported. Vow isn't in the images, so a
`toolchains.vow` entry in the config (see `config.example.yaml`) bind-mounts the
host's `vow` and `esbmc` binaries, its `libvow_runtime.a` (via `VOW_RUNTIME_PATH`) and the vow
skill docs (`/opt/vow-skill`) into both the agent and the verification
container, unlike harness `mounts`, which are agent-only. The prompt requires
the agent to build with verification on (`vow build`, never `--no-verify`). The `vow`
binary needs glibc ≥ 2.39, so the claude/codex images use a Debian trixie base.
Rebuild them after pulling this change. Adjust the mount paths to where vow lives on your machine.

### Config

See [`config.example.yaml`](config.example.yaml). Shape:

```yaml
runtime: podman             # docker (default) or podman; --runtime overrides

prompt: |
  ... instructions ...
  {problem}                 # replaced with the problem-statement markdown

defaults:                   # optional; per-harness keys override / extend these
  timeout: 1800             # seconds per agent run (null = no limit)
  # verify_timeout: 600     # seconds for the verification commands
  # network: bridge         # --network value; leave unset for internet access

harnesses:
  - name: claude
    image: euler-harness/claude:latest   # image must have the CLI installed
    cmd: "claude -p {prompt} --dangerously-skip-permissions"
    mounts:                              # share host auth/config into container
      - "~/.claude:/root/.claude"
      - "~/.claude.json:/root/.claude.json"
    # env: [ANTHROPIC_API_KEY]           # alternative: forward host env vars
    # docker_args: ["--gpus", "all"]     # extra flags appended to `docker run`
```

**Prompt placeholders** (`prompt`): `{problem}` (statement text), `{problem_file}`,
`{assets_dir}`.
**Command placeholders** (`cmd`): `{prompt}` (composed prompt, stays a single
argv token), `{prompt_file}` (`/work/PROMPT.txt`), `{problem_file}`, `{workdir}`
(`/work`).

### Harness images & sharing auth

You build the images; each just needs its CLI installed (`HOME=/root`,
`WORKDIR=/work`). Ready-made Dockerfiles are in [`harnesses/`](harnesses):

```
podman build -t euler-harness/claude:latest   harnesses/claude
podman build -t euler-harness/codex:latest    harnesses/codex
podman build -t euler-harness/oh-my-pi:latest  harnesses/oh-my-pi
```

Nothing is authenticated *inside* the image. Instead, `solve` bind-mounts your
**existing host CLI config** into each container via `mounts:`, so runs use the
login you already have:

| harness | host config mounted |
|---------|---------------------|
| claude | `~/.claude` + `~/.claude.json` |
| codex | `~/.codex/auth.json` |
| oh-my-pi | `~/.omp` |

Mount syntax is `"HOST:CONTAINER[:MODE]"` — `HOST` expands `~` and `$VARS`;
`MODE` is `ro`/`rw` (default `rw`, so the CLIs can refresh OAuth tokens). If a
mount source is missing, `solve` warns and skips it. As an alternative to
mounting a login, `env: [VAR, ...]` forwards named host env vars (e.g. API keys)
into the container.

Per-harness notes (from validating the sample images):
- **claude** runs as container root, which normally blocks
  `--dangerously-skip-permissions`; the image sets `IS_SANDBOX=1` so it's
  allowed (the container *is* the sandbox).
- **codex** reads `~/.codex/auth.json`; `--skip-git-repo-check` is needed since
  `/work` isn't a git repo, and `--dangerously-bypass-approvals-and-sandbox`
  lets it run without codex's own (container-incompatible) sandbox.
- **oh-my-pi** reads config/keys from `~/.omp`, but also forward the provider key
  your model uses (e.g. `env: [GEMINI_API_KEY]`).

Caveats:
- **Network**: harnesses need internet to reach their model APIs, so leave the
  default network in place (do *not* set `network: none`).
- **Concurrency**: the mounted auth/state (e.g. sqlite dbs, token files) is live
  and shared. Prefer `-j 1`, and avoid running the same CLI on the host at the
  same time, to sidestep write races. `:ro` mounts help but block token refresh.
- **SELinux**: append `,Z` to a mount's mode (e.g. `~/.claude:/root/.claude:rw,Z`).
