"""Markdown report rendering."""

from __future__ import annotations

from docsmoke.models import ScanReport, SnippetStatus


def render_markdown(report: ScanReport) -> str:
    lines = [
        "# docsmoke report",
        "",
        f"- Total snippets: {report.total}",
        f"- Passed: {report.passed}",
        f"- Failed: {report.failed}",
        f"- Skipped: {report.skipped}",
        f"- Errors: {report.errors}",
        f"- Duration: {report.duration_seconds:.3f}s",
        "",
    ]

    failures = [
        result
        for result in report.results
        if result.status in {SnippetStatus.failed, SnippetStatus.error}
    ]
    if not failures:
        lines.append("All snippets passed.")
        return "\n".join(lines)

    lines.append("## Failures")
    lines.append("")
    for result in failures:
        lines.extend(
            [
                f"### {result.snippet.display_name}",
                "",
                f"- Location: `{result.snippet.path}:{result.snippet.start_line}`",
                f"- Status: `{result.status.value}`",
                f"- Message: {result.message}",
                "",
            ]
        )
    return "\n".join(lines)
