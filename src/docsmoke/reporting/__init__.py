"""Report rendering utilities."""

from __future__ import annotations

from typing import TYPE_CHECKING

from docsmoke.reporting.console import render_console
from docsmoke.reporting.json import render_json
from docsmoke.reporting.markdown import render_markdown

if TYPE_CHECKING:
    from pathlib import Path

    from docsmoke.models import ScanReport

RENDERERS = {
    "console": render_console,
    "json": render_json,
    "markdown": render_markdown,
}


def render(report: ScanReport, fmt: str) -> str:
    try:
        renderer = RENDERERS[fmt]
    except KeyError as exc:
        raise ValueError(f"unknown report format: {fmt!r}") from exc
    return renderer(report)


def write(report: ScanReport, path: Path, fmt: str) -> None:
    path.write_text(render(report, fmt), encoding="utf-8")
