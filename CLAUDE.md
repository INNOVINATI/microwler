# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Tooling Standard

- Python `3.12+` only.
- Use Astral tools for Python and backend workflows:
  - `uv` for dependency management, environments, packaging, and publishing
  - `ruff` for linting and formatting
  - `ty` for static type checking
- Use `prek` for local hooks and repo hygiene automation.

## Commands

```bash
# Install all dependencies including dev tools
uv sync --group dev

# Install local hooks
uv run prek install
uv run prek install-hooks

# Run the full local gate
uv run prek run --all-files
uv run ty check microwler/
uv run pytest
uv build --no-sources
uv run zensical build

# Run a single test
uv run pytest tests/test_crawl.py::test_basic_crawl

# Serve documentation locally
uv run zensical serve
```

## Branch And Commit Rules

Microwler uses trunk-based development. `main` is the only long-lived branch.

| Branch | Purpose |
|---|---|
| `main` | Protected. Always shippable. |
| `feat/*`, `fix/*`, `chore/*`, `docs/*`, `ci/*`, `refactor/*` | Short-lived topic branches targeting `main` |

All commits must use Conventional Commits. Prefer one commit per completed step. Do not add `Co-authored-by` trailers to maintainer-generated commits.

## CI And Release Flow

- CI runs on pull requests and pushes to `main`.
- The expected validation suite is:
  - `uv run prek run --all-files`
  - `uv run ty check microwler/`
  - `uv run pytest`
  - `uv build --no-sources`
  - `uv run zensical build`
- Releases use Semantic Versioning, Keep a Changelog sections, and Release Please.
- Release Please manages the release PR and changelog updates.
- PyPI publication uses trusted publishing from `.github/workflows/release-please.yml`.
- Repository-level prerequisites:
  - `RELEASE_PLEASE_TOKEN` GitHub Actions secret
  - PyPI trusted publisher entry for this repository/workflow

## Architecture

Microwler is an async web crawling/scraping micro-framework. Crawlers are defined as a single
Python file (a project) using a declarative class-based approach and can be controlled via CLI,
Python script, or HTTP API.

### Core modules (`microwler/`)

- **`crawler.py`** — The `Microwler` class: the main crawl engine. Manages the full lifecycle
  (init → fetch → process → export) using `aiohttp` with a `BoundedSemaphore` for concurrency.
  Maintains `_seen_urls`, `_cache`, `_results`, and `_errors`. Entry point for running a crawl.

- **`page.py`** — `Page` object representing a single crawled URL. Applies selectors (XPath strings
  or callables) and transformers to scraped data, then discards raw HTML (unless `keep_source=True`).

- **`scrape.py`** — Built-in selector functions (`title`, `headings`, `paragraphs`, `meta`, `emails`,
  `images`, `canonicals`, `schemas`). Built on `parsel.Selector`. Importable as `from microwler import scrape`.

- **`export.py`** — Plugin-based export system. `BaseExporter` is the abstract base; `FileExporter`
  handles file I/O. Built-ins: `JSONExporter`, `CSVExporter`, `HTMLExporter`. Users extend
  `BaseExporter` for custom outputs.

- **`settings.py`** — `Settings` class. All mutable defaults are per-instance (not class-level) to
  prevent shared state. Keys: `link_filter` (XPath, default `//a/@href`), `max_depth` (10),
  `max_concurrency` (20), `dns_providers`, `language`, `caching`, `delta_crawl`, `export_to`,
  `exporters`. Enabling `delta_crawl` auto-enables `caching`.

- **`utils.py`** — URL normalization (sorted query params, no fragments, absolute URLs), header
  helpers, and misc utilities.

### CLI (`microwler/cli/`)

- **`cmd.py`** — Click-based CLI with commands: `new` (scaffold a project file),
  `crawler run|dumpcache|clearcache`, `serve` (start web service). Entry points are registered
  in `pyproject.toml`.
- **`template.py`** — Template string for generated project files.

### Web service (`microwler/web/`)

- **`backend.py`** — Quart (async ASGI) REST API. Routes: `GET /status`, `GET /status/<project>`,
  `GET /crawl/<project>`, `GET /data/<project>`. Projects are loaded dynamically from the
  filesystem. Serves a Vue.js frontend from `frontend/dist/`.

### Data flow

```text
User defines Microwler subclass (project file)
  -> crawler.py fetches URLs asynchronously (aiohttp)
  -> page.py scrapes each response using selectors from scrape.py
  -> results collected in _results/_cache
  -> export.py writes output via configured exporters
```

### File conventions

- Projects live in `./projects/` (single `.py` files)
- Disk cache stored at `./.microwler/cache/{domain}/`
- Exports written to `./exports/` by default
- Documentation source in `./docs/`, build output in `./site/`
