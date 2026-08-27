---
name: release-pypi
description: "Release a new version of pdf-extraction-tool to PyPI. Use when: bumping version, publishing a release, tagging a release, or automating PyPI publishing. Covers version bumping, changelog, GitHub release creation, and trusted publishing workflow."
---

# Release to PyPI

## Prerequisites

- Trusted publishing is configured on PyPI → GitHub (OIDC, no tokens needed)
- All tests passing, CI green on `main`

## Release Steps

### 1. Bump Version

Edit `pyproject.toml`:
```toml
version = "0.X.0"
```

### 2. Commit & Push

```powershell
git add pyproject.toml
git commit -m "chore: bump version to 0.X.0"
git push
```

### 3. Create GitHub Release

```powershell
gh release create vX.X.0 --generate-notes
```

The `.github/workflows/publish.yml` workflow automatically:
- Checks out the tagged commit
- Builds sdist + wheel with `python -m build`
- Publishes to PyPI via `pypa/gh-action-pypi-publish` (trusted publishing)

### 4. Verify

Visit: https://pypi.org/project/pdf-extraction-tool/vX.X.0/

## Semantic Versioning

| Change | Version Bump |
|---|---|
| Bug fixes | PATCH (0.1.**0** → 0.1.**1**) |
| New features | MINOR (0.1.0 → **0.2**.0) |
| Breaking changes | MAJOR (**1.0**.0) |

## Troubleshooting

- **Name taken**: Change `name` in `pyproject.toml` (must match PyPI project name)
- **Trusted publishing not working**: Verify publisher is linked at https://pypi.org/manage/projects/pdf-extraction-tool/publishing/
- **Build fails**: Run `python -m build` locally to debug