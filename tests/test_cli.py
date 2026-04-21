from __future__ import annotations

import json

from typer.testing import CliRunner

from docsmoke.cli import _resolve_config, app

runner = CliRunner()


def test_scan_writes_json_report(tmp_path) -> None:
    report_path = tmp_path / "report.json"
    markdown_path = tmp_path / "README.md"
    markdown_path.write_text(
        "```bash docsmoke\n# docsmoke: expect-contains=hello\nprintf 'hello\\n'\n```\n",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["scan", str(markdown_path), "--quiet", "-o", str(report_path)])

    assert result.exit_code == 0
    payload = json.loads(report_path.read_text(encoding="utf-8"))
    assert payload["summary"]["passed"] == 1


def test_scan_returns_non_zero_on_failure(tmp_path) -> None:
    markdown_path = tmp_path / "README.md"
    markdown_path.write_text(
        "```bash docsmoke\n# docsmoke: expect-contains=missing\nprintf 'hello\\n'\n```\n",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["scan", str(markdown_path), "--quiet"])

    assert result.exit_code == 2


def test_list_snippets_json(tmp_path) -> None:
    markdown_path = tmp_path / "README.md"
    markdown_path.write_text(
        "```python docsmoke\n# docsmoke: name=quickstart\nprint('hello')\n```\n",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["list-snippets", str(markdown_path), "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload[0]["name"] == "quickstart"


def test_version_flag() -> None:
    result = runner.invoke(app, ["--version"])

    assert result.exit_code == 0
    assert "docsmoke 0.1.1" in result.stdout


def test_scan_rejects_unknown_output_format(tmp_path) -> None:
    markdown_path = tmp_path / "README.md"
    markdown_path.write_text(
        "```bash docsmoke\nprintf 'hello\\n'\n```\n",
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        ["scan", str(markdown_path), "-o", str(tmp_path / "report.txt"), "-f", "xml"],
    )

    assert result.exit_code == 2
    assert "--format must be 'json' or 'markdown'" in (result.stdout + result.stderr)


def test_scan_surfaces_config_errors(tmp_path) -> None:
    result = runner.invoke(app, ["scan", "--config", str(tmp_path / "missing.toml")])

    assert result.exit_code == 2
    assert "config file does not exist" in (result.stdout + result.stderr)


def test_scan_surfaces_missing_explicit_paths(tmp_path) -> None:
    result = runner.invoke(app, ["scan", str(tmp_path / "missing.md"), "--quiet"])

    assert result.exit_code == 2
    assert "path does not exist" in (result.stdout + result.stderr)


def test_list_snippets_table_output(tmp_path) -> None:
    markdown_path = tmp_path / "README.md"
    markdown_path.write_text(
        "```bash docsmoke\n# docsmoke: name=table-case\nprintf 'hello\\n'\n```\n",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["list-snippets", str(markdown_path)])

    assert result.exit_code == 0
    assert "table-case" in result.stdout


def test_scan_prints_console_report(tmp_path) -> None:
    markdown_path = tmp_path / "README.md"
    markdown_path.write_text(
        "```bash docsmoke\nprintf 'hello\\n'\n```\n",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["scan", str(markdown_path)])

    assert result.exit_code == 0
    assert "Summary:" in result.stdout
    assert result.stdout.count("Summary:") == 1


def test_list_snippets_surfaces_config_errors(tmp_path) -> None:
    result = runner.invoke(app, ["list-snippets", "--config", str(tmp_path / "missing.toml")])

    assert result.exit_code == 2
    assert "config file does not exist" in (result.stdout + result.stderr)


def test_resolve_config_applies_cli_overrides(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    config = _resolve_config(None, all_supported=True, fail_fast=True)

    assert config.require_directive is False
    assert config.fail_fast is True
