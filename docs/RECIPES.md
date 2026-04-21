# Recipes

Practical patterns for keeping executable documentation honest in local
development, CI, containers, and gradual adoption workflows.

## README smoke test

Use this when a repository has a small set of copy-paste examples in its
README and docs:

```bash
docsmoke scan README.md docs examples
```

Why it works well:

- only marked snippets run by default
- failures include the Markdown file and line number
- expectations live next to the command they validate

## GitHub Action

The repository ships a reusable action at the repo root:

```yaml
- name: Validate executable docs
  uses: dev-ugurkontel/docsmoke@v1
  with:
    paths: README.md docs examples
```

Use `@v1` for the stable major line, or pin an exact action version
such as `@v1.0.0` when you want fully reproducible workflow inputs.

## Pull request report artifact

Write a Markdown report even when the job fails so reviewers can inspect
the exact broken snippets:

```yaml
name: Docs smoke tests

on:
  pull_request:

jobs:
  docsmoke:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - name: Install docsmoke
        run: python -m pip install docsmoke==1.0.0
      - name: Scan docs
        run: |
          mkdir -p reports
          docsmoke scan README.md docs examples \
            --output reports/docsmoke.md \
            --format markdown
      - name: Upload report
        if: always()
        uses: actions/upload-artifact@v7
        with:
          name: docsmoke-report
          path: reports/docsmoke.md
```

## Gradual adoption mode

Start by listing snippets instead of executing them:

```bash
docsmoke list-snippets README.md docs examples
```

Then mark one stable snippet at a time:

````markdown
```bash docsmoke
# docsmoke: name=version-check; expect-regex=docsmoke [0-9]+\.[0-9]+\.[0-9]+
docsmoke --version
```
````

Keep illustrative or incomplete examples unmarked until they are ready
to run.

## Working-directory fixture

When a snippet needs fixture files, keep those files under `examples/`
and set the snippet working directory explicitly:

````markdown
```bash docsmoke
# docsmoke: name=example-fixture
# docsmoke: cwd=examples
# docsmoke: expect-contains=hello
printf 'hello\n'
```
````

`cwd=` is resolved relative to the project root so snippets behave the
same from local shells and CI runners.

## Container usage

Use the published GHCR image when CI should avoid Python dependency
installation:

```bash
docker run --rm -v "$PWD:/work" -w /work \
    ghcr.io/dev-ugurkontel/docsmoke:1.0.0 scan README.md docs examples
```

Use `:latest` for convenience, `:1` for the moving stable major line, or
`:1.0.0` for a fully pinned container.

## JSON report consumers

Machine consumers should use the JSON report:

```bash
docsmoke scan README.md docs examples \
    --output reports/docsmoke.json \
    --format json
```

The report shape is documented in [`REPORT_SCHEMA.md`](REPORT_SCHEMA.md)
and tracked by [`schemas/report.schema.json`](../schemas/report.schema.json).
