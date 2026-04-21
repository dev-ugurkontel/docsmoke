# docsmoke

[![CI](https://github.com/dev-ugurkontel/docsmoke/actions/workflows/ci.yml/badge.svg)](https://github.com/dev-ugurkontel/docsmoke/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/docsmoke.svg)](https://pypi.org/project/docsmoke/)
[![Release](https://img.shields.io/github/v/release/dev-ugurkontel/docsmoke?label=release&color=blue)](https://github.com/dev-ugurkontel/docsmoke/releases)
[![Python](https://img.shields.io/pypi/pyversions/docsmoke.svg)](https://pypi.org/project/docsmoke/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Checked with mypy](https://img.shields.io/badge/mypy-strict-blue)](https://mypy.readthedocs.io/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

`docsmoke` validates executable Markdown snippets before they drift out of sync
with the software they document.

It is built for maintainers who want docs to fail like code: run the fenced
shell and Python examples in `README.md` and `docs/`, assert on expected
output, and fail CI when installation guides or CLI examples stop working.

## Highlights

- Markdown-native snippet discovery with explicit `docsmoke` opt-in markers
- Built-in shell and Python executors
- Per-snippet directives for timeouts, expectations, environment variables,
  working directories, and skips
- CLI, JSON, and Markdown reporting
- GitHub Action for CI usage
- Typed Python package with strict linting, mypy, pytest, pre-commit, Docker,
  and release automation

## Quick start

```bash
python3.11 -m pip install docsmoke
docsmoke --help
```

Mark runnable snippets in Markdown:

````markdown
```bash docsmoke
# docsmoke: name=quickstart; expect-contains=passed
docsmoke scan README.md --quiet
```
````

Run a scan:

```bash docsmoke
# docsmoke: expect-contains=list-snippets
docsmoke --help
```

List what would run:

```bash docsmoke
# docsmoke: expect-contains=example-snippet
docsmoke list-snippets examples --json
```

## Directive syntax

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

## Documentation

- [docs/INSTALL.md](docs/INSTALL.md): installation options
- [docs/USAGE.md](docs/USAGE.md): CLI usage and workflows
- [docs/CONFIG.md](docs/CONFIG.md): configuration file reference
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md): internal architecture
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
