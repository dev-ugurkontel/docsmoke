# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog and this project adheres to Semantic
Versioning.

## [Unreleased]

- Expanded README, installation, usage, architecture, and repository docs to
  match the release/documentation quality bar of `surface-audit`.
- Added practical CI, Docker, gradual-adoption, and JSON-consumer recipes.
- Added a JSON report schema and schema validation regression test.
- Refreshed the GitHub Pages site with richer project positioning, release
  surfaces, sample output, and documentation links.
- Added Dependabot tracking for Dockerfile base image updates.

## [1.0.0] - 2026-04-21

- Initial public release of `docsmoke`
- Markdown snippet discovery with explicit `docsmoke` directives
- Built-in shell and Python executors
- Per-snippet timeouts, expectations, environment variables, working
  directories, shell overrides, and skips
- Console, JSON, and Markdown reporting
- Clean user-facing errors for missing paths, invalid regex expectations, and
  invalid snippet working directories
- CommonMark-aware fenced-code discovery for nested Markdown examples and tilde
  fences
- Typed Python package with strict linting, mypy, Bandit, pre-commit, and 100%
  line and branch coverage
- GitHub Action, CI workflow, release automation, GHCR container publishing,
  Pages deployment, support docs, and repository-governance files
- Apache 2.0 licensing aligned with the companion `surface-audit` project
