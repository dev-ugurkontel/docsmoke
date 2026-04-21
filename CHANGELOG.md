# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog and this project adheres to Semantic
Versioning.

## [Unreleased]

Nothing yet.

## [0.1.1] - 2026-04-21

- Enforced 100% line and branch coverage.
- Added Bandit security analysis to local and CI quality gates.
- Hardened GitHub workflows with immutable action pins.
- Added GHCR container publishing, Pages deployment, support docs, and release docs.
- Fixed console report rendering so `docsmoke scan` prints a single report.
- Report missing explicit Markdown paths as clean configuration errors.
- Report invalid regex expectations and invalid snippet working directories
  without tracebacks.
- Hardened fenced-code discovery for nested Markdown examples and tilde fences.
- Documented repository settings, release channels, and moving action tags.
- Added Markdown link regression tests and ignored `.DS_Store` artifacts.

## [0.1.0] - 2026-04-21

- Initial public release of `docsmoke`
- Markdown snippet discovery with explicit `docsmoke` directives
- Built-in shell and Python executors
- Console, JSON, and Markdown reporting
- GitHub Action, CI workflow, release automation, Docker image, and governance files
