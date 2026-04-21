# Repository settings

This checklist captures the GitHub settings that cannot be enforced from the
source tree alone. Keep it in sync with branch rules and release automation.

## General

- Default branch: `main`
- Merge strategy: squash merge enabled; merge commits disabled
- Discussions enabled for support and ideas
- Issues enabled with blank issues disabled
- Projects and wiki disabled unless they become actively maintained

## Branch protection

Protect `main` with:

- Require a pull request before merging
- Require at least one approving review
- Require review from Code Owners
- Dismiss stale approvals when new commits are pushed
- Require conversation resolution before merging
- Require status checks to pass before merging
- Require branches to be up to date before merging
- Require linear history
- Restrict force pushes and deletions

Required checks:

- `Python 3.10`
- `Python 3.11`
- `Python 3.12`
- `Python 3.13`
- `Build distribution`
- `pages / Build Pages artifact`

## Actions

- Allow GitHub Actions and reusable workflows
- Allow actions from GitHub, verified creators, and pinned third-party actions
- Require approval for first-time contributors
- Set workflow token permissions to read-only by default
- Allow selected workflows to request elevated permissions explicitly

## Environments

Create a `pypi` environment:

- Required reviewers: maintainers
- Deployment branches/tags: release tags matching `v*.*.*`
- Used by `.github/workflows/release.yml` for PyPI Trusted Publishing

Create a `github-pages` environment:

- Used by `.github/workflows/pages.yml`
- Deployment source: GitHub Actions

## Security

Enable:

- Private vulnerability reporting
- Dependabot alerts
- Dependabot security updates
- Secret scanning
- Push protection for detected secrets
- Code scanning alerts when CodeQL is enabled for the repository

## Labels

Baseline labels expected by issue templates:

- `bug`
- `enhancement`
- `needs-triage`
- `documentation`
- `security`
- `ci`

## Release tags

- Exact package/action tags use `vMAJOR.MINOR.PATCH`, for example `v1.0.0`
- Moving action tags use `vMAJOR`, for example `v1`
- Exact release tags should be immutable after a successful release
- Moving action tags are force-updated by release automation
