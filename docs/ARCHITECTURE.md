# Architecture

`docsmoke` is organized as a small typed Python application with four
layers:

1. `cli.py`: user interface and exit-code policy
2. `runner.py`: file discovery and scan orchestration
3. `markdown.py` and `executor.py`: snippet discovery and execution
4. `reporting/`: format-specific output rendering

## Core flow

1. Load configuration from `docsmoke.toml` or `pyproject.toml`
2. Resolve Markdown files from explicit paths or configured include globs
3. Discover runnable fenced blocks
4. Strip and parse leading `docsmoke` directives
5. Execute snippets with the matching executor
6. Evaluate expectations and render the final report

## Safety model

- Supported executors are intentionally small and explicit: shell and
  Python.
- Snippets are opt-in by default through the fence info string marker,
  for example `bash docsmoke`.
- Each snippet has a timeout.
- Execution occurs relative to the project root unless overridden.
- Missing paths, invalid working directories, invalid directive values,
  and invalid expectation regexes are reported as user-facing errors.

## Extension points

- Add new executors.
- Add new report formats.
- Add richer discovery heuristics for docs linting and drift risk
  analysis.

## Release surfaces

The project has four distribution surfaces:

- PyPI package: `docsmoke==1.0.0`
- GitHub Release assets: `v1.0.0`
- GHCR images: `1.0.0`, `1.0`, `1`, and `latest`
- GitHub Action refs: `v1.0.0` and moving `v1`

The release workflow builds the Python distributions once, generates a
CycloneDX SBOM, signs the distributions with Sigstore, publishes GHCR
tags, publishes to PyPI through Trusted Publishing, and updates the
moving `v1` action tag.
