# Contributing to Microwler

Microwler is maintained as a solo-developer FOSS project and accepts outside pull requests.
Keep changes small, keep branches short-lived, and let automation do the repetitive work.

## Tooling Baseline

- Python `3.12+` is required locally and in CI.
- Use Astral tools for Python and backend workflows: `uv`, `ruff`, and `ty`.
- Install the dev environment and hooks before opening a PR:

```bash
uv sync --group dev
uv run prek install
uv run prek install-hooks
```

## Local Checks

Run these before you push:

```bash
uv run prek run --all-files
uv run ty check microwler/
uv run pytest
uv build --no-sources
uv run zensical build
```

`prek` is the local entry point for repo hygiene, GitHub Actions linting, Ruff fixes, and Ruff formatting.

## Branching And Commits

Microwler uses trunk-based development. `main` is the only long-lived branch.

| Branch | Purpose |
|---|---|
| `main` | Protected and always shippable |
| `feat/<name>` | New features |
| `fix/<name>` | Bug fixes |
| `chore/<name>` | Tooling, dependency, or maintenance work |
| `docs/<name>` | Documentation-only changes |
| `refactor/<name>` | Internal code cleanup without an intended behavior change |
| `ci/<name>` | CI/CD workflow changes |

Use short-lived topic branches and open PRs directly against `main`.

All commits must follow [Conventional Commits](https://www.conventionalcommits.org/):

```text
<type>(<scope>): <description>
```

Examples:

```text
feat(crawler): add configurable request timeout per domain
fix(settings): move mutable defaults into __init__
chore(tooling): upgrade project baseline to Python 3.12
ci(release): switch PyPI publishing to trusted publishing
docs(contributing): document prek and Release Please workflow
```

Prefer one conventional commit per completed unit of work. Maintainer-generated commits should not include `Co-authored-by` trailers.

## Pull Requests

1. Branch from `main`.
2. Make atomic commits as you complete each step.
3. Run the local checks listed above.
4. Open a PR to `main`.
5. Wait for CI to pass on:
   - `uv run prek run --all-files`
   - `uv run ty check microwler/`
   - `uv run pytest` on Python 3.12 and 3.13
   - `uv build --no-sources`
   - `uv run zensical build`

Fork-based PRs are welcome. The CI workflow is safe to run for external contributors because it does not require secrets.

## Releases

Microwler uses:

- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
- [Release Please](https://github.com/googleapis/release-please)

Release Please reads conventional commits on `main`, updates `CHANGELOG.md`, opens a release PR, and proposes the next version. Merging that release PR creates the GitHub release and triggers package publication to PyPI via trusted publishing.

### Maintainer Setup

Two one-time repository settings are required for fully automated releases:

1. Add a fine-grained `RELEASE_PLEASE_TOKEN` GitHub Actions secret with permission to create and update pull requests and releases.
2. Configure a PyPI trusted publisher for this repository and the `.github/workflows/release-please.yml` workflow.

If either setting is missing, release automation will stop at the missing boundary instead of falling back to long-lived credentials.
