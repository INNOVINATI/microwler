# Contributing to Microwler

## Branch Model

| Branch | Purpose |
|---|---|
| `main` | Protected. Represents the latest published release. Only Release Please PRs merge here. |
| `dev` | Integration branch. All feature/fix branches target this via PR. CI must pass before merge. |
| `feat/<name>` | New features |
| `fix/<name>` | Bug fixes |
| `chore/<name>` | Tooling, dependencies, configuration |
| `docs/<name>` | Documentation-only changes |
| `refactor/<name>` | Code refactoring without behavior change |

## Commit Convention

This project uses [Conventional Commits](https://www.conventionalcommits.org/). Every commit must follow the format:

```
<type>(<scope>): <description>
```

**Types** that trigger a version bump:
- `feat:` — new feature → bumps **minor** version
- `fix:` — bug fix → bumps **patch** version
- `feat!:` or body with `BREAKING CHANGE:` → bumps **major** version

**Types** that appear in the changelog but don't bump the version:
- `docs:`, `style:`, `refactor:`, `test:`, `chore:`, `ci:`, `perf:`

### Examples

```
feat(crawler): add configurable request timeout per domain
fix(settings): move mutable class defaults to __init__
chore(deps): migrate to pyproject.toml with uv + hatchling
ci: add unified CI workflow with lint, typecheck, and test matrix
docs(changelog): bootstrap CHANGELOG.md in Keep a Changelog format
```

## Development Setup

```bash
# Install dependencies (requires uv: https://docs.astral.sh/uv/)
uv sync --group dev

# Run tests
uv run pytest

# Lint
uv run ruff check microwler/

# Format
uv run ruff format microwler/

# Type check
uv run ty check microwler/
```

## Pull Request Process

1. Branch from `dev` using the naming convention above
2. Write conventional commits throughout
3. Open a PR targeting `dev`
4. All CI checks must pass (lint, typecheck, test matrix)
5. At least one approval required
6. Squash and merge into `dev`

Releases to `main` are automated via [Release Please](https://github.com/googleapis/release-please).
