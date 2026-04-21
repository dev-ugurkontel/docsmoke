# Report Schema

The JSON report produced by `docsmoke scan -f json` is intended as a
stable machine contract for CI annotations, dashboards, and custom
review tooling. Its shape is described by
[`schemas/report.schema.json`](../schemas/report.schema.json), which
uses [JSON Schema 2020-12](https://json-schema.org/draft/2020-12/schema).

Representative `ScanReport.to_dict()` payloads are validated against
that schema in the test suite.

## Top-level fields

| Field              | Type                    | Description                                                  |
| ------------------ | ----------------------- | ------------------------------------------------------------ |
| `started_at`       | RFC 3339 string         | When the scan began.                                         |
| `finished_at`      | RFC 3339 string \| null | When the scan finished, or null before report finalization.  |
| `duration_seconds` | number                  | Wall-clock scan duration.                                    |
| `summary`          | object                  | Counts by result status.                                     |
| `results`          | array                   | Individual snippet results.                                  |

## Summary shape

| Field     | Type    | Description                         |
| --------- | ------- | ----------------------------------- |
| `total`   | integer | Total snippets discovered and run.  |
| `passed`  | integer | Snippets that exited successfully.  |
| `failed`  | integer | Snippets that ran but failed.       |
| `skipped` | integer | Snippets intentionally skipped.     |
| `errors`  | integer | Configuration or execution errors.  |

## Result shape

| Field              | Type           | Description                                      |
| ------------------ | -------------- | ------------------------------------------------ |
| `snippet.id`       | string         | Stable display identifier, usually path + line.  |
| `snippet.name`     | string         | Directive name or fallback identifier.           |
| `snippet.path`     | string         | Markdown file path.                              |
| `snippet.language` | string         | Markdown fence language.                         |
| `snippet.executor` | string         | Runtime used to execute the snippet.             |
| `snippet.start_line` | integer      | First line of the fenced block.                  |
| `snippet.end_line` | integer        | Closing line of the fenced block.                |
| `status`           | enum           | `passed`, `failed`, `skipped`, or `error`.       |
| `duration_seconds` | number         | Snippet execution duration.                      |
| `exit_code`        | integer \| null | Process exit code, if a process was started.    |
| `stdout`           | string         | Captured standard output.                        |
| `stderr`           | string         | Captured standard error.                         |
| `message`          | string         | Human-readable status message.                   |

## Compatibility guarantees

`docsmoke` uses semantic versioning. On the `1.x` line:

- Existing fields will not be removed without a major-version bump.
- Existing field types will not change.
- New fields may be added; consumers should tolerate unknown keys.

Every schema change, even additive, belongs in [`CHANGELOG.md`](../CHANGELOG.md).

## Validating a report

```bash
pip install check-jsonschema
check-jsonschema --schemafile schemas/report.schema.json reports/docsmoke.json
```

Or from Python:

```python
import json
from pathlib import Path
from jsonschema import Draft202012Validator

schema = json.loads(Path("schemas/report.schema.json").read_text())
report = json.loads(Path("reports/docsmoke.json").read_text())
Draft202012Validator(schema).validate(report)
```
