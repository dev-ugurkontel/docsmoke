"""Command-line interface for docsmoke."""

from __future__ import annotations

import json
from pathlib import Path  # noqa: TC003 - Typer resolves path annotations at runtime
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from docsmoke import __version__
from docsmoke.config import Config
from docsmoke.config import load as load_config
from docsmoke.exceptions import ConfigError, DirectiveError
from docsmoke.reporting import render, write
from docsmoke.runner import collect_snippets
from docsmoke.runner import scan as run_scan

app = typer.Typer(
    name="docsmoke",
    help="Validate executable Markdown documentation snippets.",
    add_completion=False,
    no_args_is_help=True,
)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"docsmoke {__version__}")
        raise typer.Exit()


def _resolve_config(
    config_path: Path | None,
    *,
    all_supported: bool,
    fail_fast: bool | None,
) -> Config:
    config = load_config(config_path)
    if all_supported:
        config.require_directive = False
    if fail_fast is not None:
        config.fail_fast = fail_fast
    return config


@app.callback()
def _root(
    _version: Annotated[
        bool | None,
        typer.Option(
            "--version",
            callback=_version_callback,
            is_eager=True,
            help="Show version and exit.",
        ),
    ] = None,
) -> None:
    """Executable documentation smoke tests for Markdown."""


@app.command()
def scan(
    paths: Annotated[
        list[Path] | None,
        typer.Argument(
            help="Markdown files or directories to scan. Defaults to configured include globs."
        ),
    ] = None,
    config_path: Annotated[
        Path | None,
        typer.Option("--config", help="Path to docsmoke.toml or pyproject.toml."),
    ] = None,
    output: Annotated[
        Path | None,
        typer.Option("--output", "-o", help="Write a machine-readable report."),
    ] = None,
    fmt: Annotated[
        str,
        typer.Option("--format", "-f", help="Report format for --output: json or markdown."),
    ] = "json",
    quiet: Annotated[
        bool,
        typer.Option("--quiet", "-q", help="Suppress console report output."),
    ] = False,
    all_supported: Annotated[
        bool,
        typer.Option(
            "--all-supported",
            help="Execute every supported fenced block, even when not explicitly marked.",
        ),
    ] = False,
    fail_fast: Annotated[
        bool | None,
        typer.Option("--fail-fast/--no-fail-fast", help="Stop after the first failing snippet."),
    ] = None,
) -> None:
    """Scan Markdown files, execute snippets, and report the results."""
    try:
        paths = paths or []
        config = _resolve_config(config_path, all_supported=all_supported, fail_fast=fail_fast)
        report = run_scan(paths, config=config)
    except (ConfigError, DirectiveError) as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=2) from None

    if not quiet:
        typer.echo(render(report, "console"))

    if output is not None:
        if fmt not in {"json", "markdown"}:
            typer.secho("--format must be 'json' or 'markdown'", fg=typer.colors.RED, err=True)
            raise typer.Exit(code=2)
        write(report, output, fmt)

    if report.has_failures:
        raise typer.Exit(code=2)


@app.command("list-snippets")
def list_snippets(
    paths: Annotated[
        list[Path] | None,
        typer.Argument(
            help="Markdown files or directories to inspect. Defaults to configured include globs."
        ),
    ] = None,
    config_path: Annotated[
        Path | None,
        typer.Option("--config", help="Path to docsmoke.toml or pyproject.toml."),
    ] = None,
    as_json: Annotated[
        bool,
        typer.Option("--json", help="Emit JSON instead of a table."),
    ] = False,
    all_supported: Annotated[
        bool,
        typer.Option(
            "--all-supported",
            help="List every supported fenced block, even when not explicitly marked.",
        ),
    ] = False,
) -> None:
    """List snippets that docsmoke would execute."""
    try:
        paths = paths or []
        config = _resolve_config(config_path, all_supported=all_supported, fail_fast=None)
        snippets = collect_snippets(paths, config=config)
    except (ConfigError, DirectiveError) as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=2) from None

    if as_json:
        payload = [
            {
                "id": snippet.identifier,
                "path": str(snippet.path),
                "language": snippet.language,
                "executor": snippet.executor,
                "name": snippet.display_name,
                "line": snippet.start_line,
            }
            for snippet in snippets
        ]
        typer.echo(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    table = Table(title="docsmoke snippets")
    table.add_column("Snippet")
    table.add_column("Language")
    table.add_column("Executor")
    table.add_column("Location")
    for snippet in snippets:
        table.add_row(
            snippet.display_name,
            snippet.language,
            snippet.executor,
            f"{snippet.path}:{snippet.start_line}",
        )
    console = Console()
    console.print(table)
