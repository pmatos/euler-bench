"""Active Claude models and the effort levels each accepts.

Source: Claude API docs (model status table + effort/thinking table), 2026-10-14.
`efforts` is empty for models that have no `effort` parameter (the API errors
if one is sent). `default` is the API default when effort is omitted; Claude Code
applies its own default (xhigh on supporting models), so `solve` always passes
effort explicitly for models that support it.
"""

from __future__ import annotations

from dataclasses import dataclass

ALL5 = ("low", "medium", "high", "xhigh", "max")
NO_XHIGH = ("low", "medium", "high", "max")
LMH = ("low", "medium", "high")


@dataclass(frozen=True)
class ModelInfo:
    efforts: tuple[str, ...]
    default: str | None
    note: str = ""


MODELS: dict[str, ModelInfo] = {
    "claude-fable-5-1": ModelInfo(ALL5, "high"),
    "claude-fable-5": ModelInfo(ALL5, "high"),
    "claude-opus-5-5": ModelInfo(ALL5, "medium"),
    "claude-opus-5": ModelInfo(ALL5, "high"),
    "claude-opus-4-8": ModelInfo(ALL5, "high"),
    "claude-opus-4-7": ModelInfo(ALL5, "high"),
    "claude-opus-4-6": ModelInfo(NO_XHIGH, "high"),
    "claude-opus-4-5-20251101": ModelInfo(LMH, "high"),
    "claude-sonnet-5-5": ModelInfo(ALL5, "high"),
    "claude-sonnet-5": ModelInfo(ALL5, "high"),
    "claude-sonnet-4-6": ModelInfo(NO_XHIGH, "high"),
    "claude-haiku-5-5": ModelInfo(ALL5, "medium"),
    "claude-haiku-4-5-20251001": ModelInfo((), None, "no effort parameter"),
}


def check_effort(model: str, effort: str | None) -> str | None:
    """Return an error message if (model, effort) is invalid, else None."""
    info = MODELS.get(model)
    if info is None:
        return f"unknown model '{model}' (add it to models.py)"
    if not info.efforts:
        return None if effort is None else f"{model} has no effort levels; remove 'effort'"
    if effort is None:
        return f"{model} supports effort; set 'effort' to one of: {', '.join(info.efforts)}"
    if effort not in info.efforts:
        return f"{model} does not support effort '{effort}'; valid: {', '.join(info.efforts)}"
    return None
