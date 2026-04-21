# Configuration

`docsmoke` reads configuration from either:

1. `docsmoke.toml`
2. `pyproject.toml` under `[tool.docsmoke]`

CLI flags override file configuration.

## Example

```toml
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
