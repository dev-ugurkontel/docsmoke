"""Rich console rendering."""

from __future__ import annotations

from rich.console import Console
from rich.table import Table

from docsmoke.models import ScanReport, SnippetStatus

STATUS_STYLE = {
    SnippetStatus.passed: "green",
    SnippetStatus.failed: "red",
    SnippetStatus.skipped: "yellow",
    SnippetStatus.error: "bold red",
}


def render_console(report: ScanReport) -> str:
    console = Console(width=100)
    table = Table(title="docsmoke")
    table.add_column("Status")
    table.add_column("Snippet")
    table.add_column("Language")
    table.add_column("Duration")
    table.add_column("Message")

    for result in report.results:
        table.add_row(
            f"[{STATUS_STYLE[result.status]}]{result.status.value}[/{STATUS_STYLE[result.status]}]",
            result.snippet.display_name,
            result.snippet.language,
            f"{result.duration_seconds:.3f}s",
            result.message,
        )

    with console.capture() as capture:
        console.print(table)
        console.print(
            f"Summary: total={report.total} passed={report.passed} failed={report.failed} "
            f"skipped={report.skipped} errors={report.errors} duration={report.duration_seconds:.3f}s"
        )
    return capture.get()
