from __future__ import annotations

import json
from pathlib import Path

import pytest

from docsmoke.models import ScanReport, Snippet, SnippetDirectives, SnippetResult, SnippetStatus
from docsmoke.reporting import render


def _result(status: SnippetStatus, message: str) -> SnippetResult:
    return SnippetResult(
        snippet=Snippet(
            path=Path("README.md"),
            language="bash",
            executor="sh",
            code="printf 'hello\\n'",
            start_line=1,
            end_line=3,
            directives=SnippetDirectives(name="sample"),
        ),
        status=status,
        duration_seconds=0.123,
        exit_code=0 if status is SnippetStatus.passed else 1,
        stdout="hello\n",
        stderr="",
        message=message,
    )


def test_render_json() -> None:
    report = ScanReport(results=[_result(SnippetStatus.passed, "ok")])
    report.finish()

    payload = json.loads(render(report, "json"))

    assert payload["summary"]["passed"] == 1


def test_render_markdown_includes_failures() -> None:
    report = ScanReport(results=[_result(SnippetStatus.failed, "missing expected text")])
    report.finish()

    rendered = render(report, "markdown")

    assert "## Failures" in rendered
    assert "missing expected text" in rendered


def test_render_console_summary() -> None:
    report = ScanReport(results=[_result(SnippetStatus.passed, "ok")])
    report.finish()

    rendered = render(report, "console")

    assert "Summary:" in rendered
    assert "passed" in rendered


def test_render_markdown_all_passes() -> None:
    report = ScanReport(results=[_result(SnippetStatus.passed, "ok")])
    report.finish()

    rendered = render(report, "markdown")

    assert "All snippets passed." in rendered


def test_unknown_renderer_raises() -> None:
    report = ScanReport()
    report.finish()

    with pytest.raises(ValueError):
        render(report, "xml")
