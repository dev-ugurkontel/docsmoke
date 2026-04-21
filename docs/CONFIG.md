# Configuration

`docsmoke` reads configuration from either:

1. `docsmoke.toml`
2. `pyproject.toml` under `[tool.docsmoke]`

CLI flags override file configuration.

## Example

In `pyproject.toml`:

```toml
[tool.docsmoke]
include = ["README.md", "docs/**/*.md", "examples/**/*.md"]
exclude = [".venv/**", "build/**", "dist/**"]
default_timeout = 10.0
fail_fast = false
require_directive = true
```

## Fields

- `include`: globs used when no explicit scan path is provided
- `exclude`: globs ignored during discovery
- `default_timeout`: positive snippet timeout in seconds
- `fail_fast`: stop the scan after the first failure
- `require_directive`: only execute snippets explicitly marked for docsmoke

## Precedence

Command-line flags override file configuration:

- `--config` selects a specific `docsmoke.toml` or `pyproject.toml`
- `--all-supported` sets `require_directive = false`
- `--fail-fast` and `--no-fail-fast` override `fail_fast`

## Include and exclude behavior

When no explicit paths are passed to `docsmoke scan`, `include` globs
decide what Markdown files are scanned. Explicit paths are still filtered
for supported Markdown files, so passing a directory remains safe.

`exclude` globs are matched against repository-relative paths. Keep
virtual environments, build artifacts, generated reports, and package
output out of the scan set.
