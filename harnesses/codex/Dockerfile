# OpenAI Codex CLI harness image.
#
# Auth is NOT baked in. At run time, `solve` bind-mounts your host
# ~/.codex/auth.json into /root/.codex — see config.example.yaml.
#
# Build:
#   podman build -t euler-harness/codex:latest harnesses/codex
FROM docker.io/library/node:22-bookworm-slim

ARG CODEX_VERSION=0.144.1
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      git ca-certificates python3 build-essential \
 && rm -rf /var/lib/apt/lists/* \
 && npm install -g @openai/codex@${CODEX_VERSION}

ENV HOME=/root
WORKDIR /work

# The invocation comes from the harness `cmd` in config.yaml, e.g.
#   codex exec --skip-git-repo-check --dangerously-bypass-approvals-and-sandbox {prompt}
# (verify flags for your version with: codex exec --help)
