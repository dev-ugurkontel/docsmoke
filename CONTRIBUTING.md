# Contributing to docsmoke

Thanks for considering a contribution.

## Development setup

```bash
git clone <your-fork-or-repo-url>
cd docsmoke
make install
make all
```

## Pull requests

1. Open an issue or discussion for substantial changes.
2. Keep changes focused and well-tested.
3. Update docs for user-facing behavior changes.
4. Add or update tests for code changes.
5. Keep commit messages intentional and release-note friendly.

## Tooling

- `ruff` for linting and formatting
- `mypy --strict` for type checking
- `pytest` for tests
- `pre-commit` for local checks

## Branching and releases

- Default branch: `main`
- Feature branches: `feat/<slug>` or `fix/<slug>`
- Release tags: `vMAJOR.MINOR.PATCH`
- Moving GitHub Action tags: `vMAJOR`, for example `v1`
- Changelog entries belong under `[Unreleased]` until release day
- Repository settings are tracked in [docs/REPOSITORY.md](docs/REPOSITORY.md)

## Good first contributions

- Add new snippet fixtures for real-world docs layouts
- Improve renderer output
- Add executor support for another runtime
- Tighten docs around CI and onboarding workflows
