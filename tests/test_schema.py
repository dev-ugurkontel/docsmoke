from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

from docsmoke.config import Config
from docsmoke.runner import scan

_ROOT = Path(__file__).resolve().parent.parent


def test_json_report_matches_schema(tmp_path: Path) -> None:
    markdown_path = tmp_path / "README.md"
    markdown_path.write_text(
        "```bash docsmoke\n# docsmoke: name=hello; expect-contains=hello\nprintf 'hello\\n'\n```\n",
        encoding="utf-8",
    )
    schema = json.loads((_ROOT / "schemas" / "report.schema.json").read_text(encoding="utf-8"))

    report = scan([markdown_path], config=Config())

    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(report.to_dict())
