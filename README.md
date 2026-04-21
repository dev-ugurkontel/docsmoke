# docsmoke

[![CI](https://github.com/dev-ugurkontel/docsmoke/actions/workflows/ci.yml/badge.svg)](https://github.com/dev-ugurkontel/docsmoke/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/docsmoke.svg)](https://pypi.org/project/docsmoke/)
[![Python](https://img.shields.io/pypi/pyversions/docsmoke.svg)](https://pypi.org/project/docsmoke/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

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
- `timeout=<seconds>`: per-snippet timeout
- `expect-contains=<text>`: required stdout or stderr substring
- `expect-regex=<pattern>`: required regex match against stdout or stderr
- `env.NAME=<value>`: environment variable override
- `shell=<binary>`: shell override for shell snippets
- `skip[=true|false]`: skip the snippet without removing it

## GitHub Action

```yaml
- uses: dev-ugurkontel/docsmoke@v0.1.1
  with:
    paths: README.md docs examples
```

## Documentation

- [docs/INSTALL.md](docs/INSTALL.md): installation options
- [docs/USAGE.md](docs/USAGE.md): CLI usage and workflows
- [docs/CONFIG.md](docs/CONFIG.md): configuration file reference
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md): internal architecture
- [CONTRIBUTING.md](CONTRIBUTING.md): contribution workflow
- [SECURITY.md](SECURITY.md): private vulnerability disclosure
- [SUPPORT.md](SUPPORT.md): usage help and issue routing

## Development

```bash
make all
```

## License

MIT licensed. See [LICENSE](LICENSE).
