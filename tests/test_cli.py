from __future__ import annotations

import json

from typer.testing import CliRunner

from docsmoke.cli import app

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
