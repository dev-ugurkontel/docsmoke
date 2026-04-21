# Installation

`docsmoke` is a standard Python package for Python `3.10+`.

## End-user CLI

```bash
pipx install docsmoke
docsmoke --help
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

## macOS note

The system `python3` on macOS may still resolve to Python `3.9`. Use an
explicit newer interpreter such as `python3.11`.
