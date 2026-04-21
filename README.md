# docsmoke

[![CI](https://github.com/dev-ugurkontel/docsmoke/actions/workflows/ci.yml/badge.svg)](https://github.com/dev-ugurkontel/docsmoke/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/docsmoke.svg)](https://pypi.org/project/docsmoke/)
[![Downloads](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fpypistats.org%2Fapi%2Fpackages%2Fdocsmoke%2Frecent&query=%24.data.last_month&label=downloads&suffix=%2Fmo&color=brightgreen)](https://pypistats.org/packages/docsmoke)
[![Release](https://img.shields.io/github/v/release/dev-ugurkontel/docsmoke?label=release&color=blue)](https://github.com/dev-ugurkontel/docsmoke/releases)
[![Last commit](https://img.shields.io/github/last-commit/dev-ugurkontel/docsmoke?color=green)](https://github.com/dev-ugurkontel/docsmoke/commits/main)
[![Python](https://img.shields.io/pypi/pyversions/docsmoke.svg)](https://pypi.org/project/docsmoke/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Checked with mypy](https://img.shields.io/badge/mypy-strict-blue)](https://mypy.readthedocs.io/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

Executable documentation smoke tests for Markdown.

`docsmoke` runs the shell and Python examples you mark in `README.md`,
`docs/`, and onboarding guides, then fails CI when those examples stop
matching reality. It is intentionally small: opt-in fenced blocks,
inline expectations, deterministic timeouts, and reports that fit pull
requests.

## Why Maintainers Use It

- **Docs fail like code** — quickstarts, install commands, and CLI examples
  run in CI instead of quietly rotting.
- **Markdown-native** — authors keep examples in ordinary fenced blocks.
- **Opt-in by default** — only snippets marked for `docsmoke` execute unless
  you explicitly choose `--all-supported`.
- **Assert behavior** — expectations, regexes, timeouts, working directories,
  environment overrides, skips, and shell overrides live next to the example.
- **CI-native** — console, JSON, and Markdown reports work in local terminals,
  GitHub Actions, and release gates.
- **Supply-chain aware** — releases publish to PyPI, GitHub Releases, GHCR,
  and the reusable GitHub Action with SBOMs and Sigstore bundles.

## Use It When

- your README contains copy-paste commands that users rely on
- your docs include shell or Python examples that should keep working
- you want a narrow documentation gate in CI
- you want to verify examples without adopting a full documentation platform

## Reach for Other Tools When

- you need prose style linting or grammar checks
- you need full notebook execution
- you need browser-based end-to-end tests
- you want to run arbitrary untrusted snippets without sandboxing

## Quick Start

```bash
pipx install docsmoke
docsmoke --help
```

Detailed installation: [`docs/INSTALL.md`](docs/INSTALL.md).

## Mark Runnable Snippets

Put `docsmoke` after the language in the fenced block's info string.
The first word, `bash`, still controls Markdown syntax highlighting; the
second word, `docsmoke`, is the opt-in marker that tells the scanner to
execute the block.

````markdown
```bash docsmoke
# docsmoke: name=hello; expect-contains=hello
printf 'hello\n'
```
````

Run a scan:

```bash docsmoke
# docsmoke: name=scan-examples
docsmoke scan examples --quiet
```

List what would run:

```bash docsmoke
# docsmoke: expect-contains=example-snippet
docsmoke list-snippets examples --json
```

## Directive Syntax

Directives live in the first lines of a runnable fenced block:

````markdown
```bash docsmoke
# docsmoke: name=install-check
# docsmoke: cwd=examples
# docsmoke: expect-contains=hello
printf 'hello\n'
```
````

Supported directives:

- `name=<value>`: human-friendly snippet label
- `cwd=<path>`: working directory relative to the project root
- `timeout=<seconds>`: positive per-snippet timeout
- `expect-contains=<text>`: required stdout or stderr substring
- `expect-regex=<pattern>`: required regex match against stdout or stderr
- `env.NAME=<value>`: environment variable override
- `shell=<binary>`: shell override for shell snippets
- `skip[=true|false]`: skip the snippet without removing it

## GitHub Action

Use the moving `@v1` tag to receive compatible `1.x` fixes automatically, or
pin an exact release such as `@v1.0.0` for fully reproducible workflow inputs.

```yaml
- uses: dev-ugurkontel/docsmoke@v1
  with:
    paths: README.md docs examples
```

## Distribution Options

- **PyPI** — best for `pipx`, virtualenvs, and Python-based tooling.
- **GHCR** — best when CI prefers a pinned container image.
- **GitHub Action** — best when docs validation already lives in Actions.

```bash
docker run --rm -v "$PWD:/work" -w /work \
    ghcr.io/dev-ugurkontel/docsmoke:latest scan README.md docs examples
```

Use `:latest` for convenience, `:1` for the moving stable major line, or
`:1.0.0` for a fully pinned container.

## Sample Output

```text
docsmoke
passed  examples/README.md:5  bash  0.004s  ok

Summary: total=1 passed=1 failed=0 skipped=0 errors=0
```

## Project Site

- [Project landing page](https://dev-ugurkontel.github.io/docsmoke/)
- [PyPI package](https://pypi.org/project/docsmoke/)
- [GitHub Releases](https://github.com/dev-ugurkontel/docsmoke/releases)

## Documentation

- [docs/INSTALL.md](docs/INSTALL.md): installation options
- [docs/USAGE.md](docs/USAGE.md): CLI usage and workflows
- [docs/CONFIG.md](docs/CONFIG.md): configuration file reference
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md): internal architecture
- [docs/RECIPES.md](docs/RECIPES.md): CI, Docker, and migration recipes
- [docs/REPORT_SCHEMA.md](docs/REPORT_SCHEMA.md): JSON report contract
- [docs/RELEASE.md](docs/RELEASE.md): release and tag-management process
- [docs/REPOSITORY.md](docs/REPOSITORY.md): repository settings checklist
- [CONTRIBUTING.md](CONTRIBUTING.md): contribution workflow
- [SECURITY.md](SECURITY.md): private vulnerability disclosure
- [SUPPORT.md](SUPPORT.md): usage help and issue routing

## Development

```bash
make all
```

## License

Apache 2.0 licensed. See [LICENSE](LICENSE).
