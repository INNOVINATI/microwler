# Contributing to Microwler

## Branch Model

This project uses **trunk-based development**. `main` is the only long-lived branch and is always shippable.

```
feat/foo ──┐
fix/bar ───┼──▶  PR → main  ──▶  Release Please PR → tag + PyPI
chore/baz ─┘
```

| Branch | Purpose |
|---|---|
| `main` | Protected. Every commit is a candidate for release. |
| `feat/<name>` | New features — branch from `main`, PR back to `main` |
| `fix/<name>` | Bug fixes — branch from `main`, PR back to `main` |
| `chore/<name>` | Tooling, dependencies, configuration |
| `docs/<name>` | Documentation-only changes |
| `refactor/<name>` | Code refactoring without behavior change |
| `ci/<name>` | CI/CD workflow changes |

Topic branches should be short-lived (hours to days, not weeks).

## Commit Convention

This project uses [Conventional Commits](https://www.conventionalcommits.org/). Every commit must follow:

```
<type>(<scope>): <description>
```

**Types that trigger a version bump:**
- `feat:` → bumps **minor** (`0.1.x` → `0.2.0`)
- `fix:` → bumps **patch** (`0.1.8` → `0.1.9`)
- `feat!:` or body with `BREAKING CHANGE:` footer → bumps **major** (`0.x.y` → `1.0.0`)

**Types that appear in CHANGELOG but don't bump the version:**
- `docs:`, `style:`, `refactor:`, `test:`, `chore:`, `ci:`, `perf:`

### Examples

```
feat(crawler): add configurable request timeout per domain
fix(settings): move mutable class defaults to __init__
chore(deps): bump aiohttp to 3.10
ci: pin setup-uv to v5
docs(changelog): bootstrap CHANGELOG.md
```

## Development Setup

```bash
# Requires uv: https://docs.astral.sh/uv/
uv sync --group dev

# Run tests
uv run pytest

# Lint
uv run ruff check microwler/ tests/

# Format
uv run ruff format microwler/ tests/

# Type check
uv run ty check microwler/
```

## Pull Request Process

1. Branch from `main` using the naming convention above
2. Write conventional commits throughout (each commit should be atomic and meaningful)
3. Open a PR targeting `main`
4. All CI checks must pass (lint, typecheck, test matrix across Python 3.10–3.12)
5. At least one approval required
6. Squash and merge into `main`

Releases are fully automated via [Release Please](https://github.com/googleapis/release-please).
When your PR merges, Release Please opens or updates a release PR that batches all pending
changes. Merging that PR cuts the release and publishes to PyPI.
