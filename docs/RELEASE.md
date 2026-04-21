# Release process

This document describes how `docsmoke` releases are managed across PyPI,
GitHub Releases, GHCR, and the reusable GitHub Action.

## Version identifiers

`docsmoke` uses two related but different versioning surfaces:

- **Package release tags** such as `v0.1.1` are immutable release markers for
  the Python package, GitHub Release assets, SBOMs, signatures, and GHCR image
  tags.
- **Major action tags** such as `v0` are moving compatibility tags for the
  reusable GitHub Action. `v0` points to the latest compatible `0.x` release.

Users can choose:

```yaml
uses: dev-ugurkontel/docsmoke@v0
uses: dev-ugurkontel/docsmoke@v0.1.1
```

## Channels

Each tagged release publishes:

- **PyPI**: the canonical Python package for `pip`, `pipx`, and virtualenvs.
- **GitHub Releases**: wheel, sdist, CycloneDX SBOM, and Sigstore bundles.
- **GHCR**: container tags for `latest`, major, major/minor, and exact version.
- **GitHub Action**: the repository root `action.yml`.

## Required checks

Changes to `main` should pass:

- Python 3.10, 3.11, 3.12, and 3.13 test matrix
- Ruff lint and format checks
- mypy strict type checks
- Bandit static analysis
- 100% line and branch coverage
- `docsmoke scan README.md docs examples`

## Release steps

1. Update `pyproject.toml` and `src/docsmoke/__init__.py` with the new version.
2. Add release notes to `CHANGELOG.md`.
3. Merge the release commit to `main` after CI passes.
4. Create and push the exact release tag:

   ```bash
   git tag -a vX.Y.Z -m "docsmoke vX.Y.Z"
   git push origin vX.Y.Z
   ```

5. Approve the `pypi` environment deployment when the workflow pauses.
6. Confirm PyPI, GitHub Release assets, GHCR tags, and the moving major action
   tag.

## Post-release checklist

- `gh release view vX.Y.Z` lists wheel, sdist, SBOM, and Sigstore JSON files.
- PyPI reports the new version.
- GHCR exposes `latest`, major, major/minor, and exact version tags.
- `git rev-parse v0^{commit}` matches `git rev-parse vX.Y.Z^{commit}` for
  `0.x` releases.
- The local tree is clean after `make clean`.
