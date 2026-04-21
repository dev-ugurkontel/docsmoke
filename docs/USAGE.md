# Usage

## Marking snippets

Only explicitly marked snippets run by default.

````markdown
```bash docsmoke
# docsmoke: expect-contains=hello
printf 'hello\n'
```
````

## Common commands

```bash
docsmoke scan README.md docs
docsmoke scan --config docsmoke.toml
docsmoke list-snippets README.md docs --json
```

## Output file

```bash
docsmoke scan README.md docs -o docsmoke-report.json -f json
docsmoke scan README.md docs -o docsmoke-report.md -f markdown
```

## Scan all supported fenced blocks

```bash
docsmoke scan README.md docs --all-supported
```

## Fail fast

```bash
docsmoke scan README.md docs --fail-fast
```

## Typical CI usage

```yaml
- name: Validate docs
  run: |
    pipx install docsmoke
    docsmoke scan README.md docs examples
```
