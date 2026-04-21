# Usage

`docsmoke` is designed around one rule: examples only run when the
author made that intent visible in Markdown.

## Marking snippets

Only explicitly marked snippets run by default.

````markdown
```bash docsmoke
# docsmoke: name=hello; expect-contains=hello
printf 'hello\n'
```
````

In a fenced block whose info string is `bash docsmoke`, `bash` is the
syntax-highlighting language and `docsmoke` is the execution marker.
GitHub and most Markdown renderers still highlight the block as shell.

Python snippets use the same pattern:

````markdown
```python docsmoke
# docsmoke: name=python-hello; expect-contains=hello
print("hello")
```
````

## Common commands

```bash
docsmoke scan README.md docs examples
docsmoke scan --config docsmoke.toml
docsmoke list-snippets README.md docs examples --json
```

## Output file

```bash
docsmoke scan README.md docs examples -o docsmoke-report.json -f json
docsmoke scan README.md docs examples -o docsmoke-report.md -f markdown
```

The JSON report shape is documented in
[`REPORT_SCHEMA.md`](REPORT_SCHEMA.md).

## Scan all supported fenced blocks

```bash
docsmoke scan README.md docs --all-supported
```

Use this mode only when the repository's fenced shell and Python blocks
are already written as executable examples. The default opt-in mode is
safer for READMEs that also contain illustrative fragments.

## Fail fast

```bash
docsmoke scan README.md docs --fail-fast
```

## Working directories and environment

Directives are parsed only from the first lines of a marked block:

````markdown
```bash docsmoke
# docsmoke: name=fixture-check
# docsmoke: cwd=examples
# docsmoke: env.GREETING=hello
# docsmoke: expect-contains=hello
printf '%s\n' "$GREETING"
```
````

Paths in `cwd=` are resolved relative to the project root, not relative
to the Markdown file. Invalid working directories become clean
configuration errors in the report instead of Python tracebacks.

## Expectations

Use `expect-contains=` for stable text and `expect-regex=` when the
output contains paths, timing, or values that may vary:

````markdown
```bash docsmoke
# docsmoke: expect-regex=docsmoke [0-9]+\.[0-9]+\.[0-9]+
docsmoke --version
```
````

Expectations are matched against stdout and stderr combined.

## Typical CI usage

```yaml
- name: Validate docs
  run: |
    pipx install docsmoke
    docsmoke scan README.md docs examples
```

Prefer the reusable action when the repository should consume the
released tool and action together:

```yaml
- name: Validate docs
  uses: dev-ugurkontel/docsmoke@v1
  with:
    paths: README.md docs examples
```
