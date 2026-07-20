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
   into `/work` (e.g. `answer.txt`, solution code) stays in `work/`.

A `summary.json` is written at the run root. Correctness is **not** graded.

### Config

See [`config.example.yaml`](config.example.yaml). Shape:

```yaml
runtime: podman             # docker (default) or podman; --runtime overrides

prompt: |
  ... instructions ...
  {problem}                 # replaced with the problem-statement markdown

defaults:                   # optional; per-harness keys override / extend these
  timeout: 1800             # seconds per run (null = no limit)
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
