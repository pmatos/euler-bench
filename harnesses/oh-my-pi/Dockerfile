# oh-my-pi (omp) harness image.
#
# Auth/config is NOT baked in. At run time, `solve` bind-mounts your host
# ~/.omp into /root/.omp — see config.example.yaml.
#
# Build:
#   podman build -t euler-harness/oh-my-pi:latest harnesses/oh-my-pi
FROM docker.io/oven/bun:1-debian

ARG OMP_VERSION=16.3.15
USER root
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      git ripgrep ca-certificates python3 build-essential \
 && rm -rf /var/lib/apt/lists/* \
 && bun install -g @oh-my-pi/pi-coding-agent@${OMP_VERSION}

ENV HOME=/root
ENV PATH="/root/.bun/bin:${PATH}"
WORKDIR /work

# The invocation comes from the harness `cmd` in config.yaml, e.g.
#   omp -p {prompt} --auto-approve --no-session
