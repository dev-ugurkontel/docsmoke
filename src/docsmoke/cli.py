"""Command-line interface entrypoint."""

from __future__ import annotations

import typer

app = typer.Typer(
    name="docsmoke",
    help="Validate executable Markdown documentation snippets.",
    add_completion=False,
    no_args_is_help=True,
)

