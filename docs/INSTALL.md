# Installation

`docsmoke` is a standard Python package for Python `3.10+`.

## End-user CLI

```bash
pipx install docsmoke
docsmoke --help
```

Use an exact pin when you need reproducible local or CI installs:

```bash
pipx install docsmoke==1.0.0
```

## Inside a virtual environment

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install docsmoke
```

## From source

```bash
git clone https://github.com/dev-ugurkontel/docsmoke.git
cd docsmoke
make install PYTHON=python3.11
make all
```

## Docker

```bash
docker build -t docsmoke:local .
docker run --rm -v "$PWD:/work" -w /work docsmoke:local scan README.md docs
```

Tagged releases publish GHCR images:

```bash
docker pull ghcr.io/dev-ugurkontel/docsmoke:latest
docker run --rm -v "$PWD:/work" -w /work \
    ghcr.io/dev-ugurkontel/docsmoke:1.0.0 scan README.md docs examples
```

Use `:latest` for convenience, `:1` for the moving stable major line,
or `:1.0.0` for a fully pinned container.

## GitHub Action

```yaml
- name: Validate executable docs
  uses: dev-ugurkontel/docsmoke@v1
  with:
    paths: README.md docs examples
```

Use `@v1` for compatible fixes on the `1.x` action line or
`@v1.0.0` for an exact action revision.

## macOS note

The system `python3` on macOS may still resolve to Python `3.9`. Use an
explicit newer interpreter such as `python3.11`.
