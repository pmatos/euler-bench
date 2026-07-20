# Claude Code harness image.
#
# Auth is NOT baked in. At run time, `solve` bind-mounts your host config
# (~/.claude and ~/.claude.json) into /root — see config.example.yaml.
#
# Build:
#   podman build -t euler-harness/claude:latest harnesses/claude
# Pin a different CLI version:
#   podman build --build-arg CLAUDE_VERSION=2.1.206 -t euler-harness/claude:latest harnesses/claude
FROM docker.io/library/node:22-bookworm-slim

ARG CLAUDE_VERSION=2.1.206
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      git ripgrep ca-certificates python3 curl \
 && rm -rf /var/lib/apt/lists/* \
 && npm install -g @anthropic-ai/claude-code@${CLAUDE_VERSION}

ENV HOME=/root
# Allow --dangerously-skip-permissions while running as container root
# (claude blocks it under uid 0 otherwise). Safe: the container is the sandbox.
ENV IS_SANDBOX=1
WORKDIR /work

# The invocation comes from the harness `cmd` in config.yaml, e.g.
#   claude -p {prompt} --dangerously-skip-permissions
