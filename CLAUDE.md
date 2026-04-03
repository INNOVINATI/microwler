# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install all dependencies including dev tools (requires uv: https://docs.astral.sh/uv/)
uv sync --group dev

# Run all tests
uv run pytest

# Run a single test
uv run pytest tests/test_crawl.py::test_basic_crawl

# Lint (check only)
uv run ruff check microwler/ tests/

# Lint + auto-fix
uv run ruff check --fix microwler/ tests/

# Format
uv run ruff format microwler/ tests/

# Type check
uv run ty check microwler/

# Serve documentation locally
uv run zensical serve

# Build documentation
uv run zensical build

# Build distribution package
uv build
```

## Branch Model

| Branch | Purpose |
|---|---|
| `main` | Protected. Latest published release. Only Release Please PRs merge here. |
| `dev` | Integration branch. All PRs target this. CI must pass before merge. |
| `feat/*`, `fix/*`, `chore/*`, `docs/*` | Short-lived topic branches |

All commits must follow **Conventional Commits** (`feat:`, `fix:`, `chore:`, `docs:`, `ci:`, etc.).
Release Please parses these to auto-bump versions and generate CHANGELOG.md.

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
  `images`, `canonicals`, `schemas`). Built on `parsel.Selector`.

- **`export.py`** — Plugin-based export system. `BaseExporter` is the abstract base; `FileExporter`
  handles file I/O. Built-ins: `JSONExporter`, `CSVExporter`, `HTMLExporter`. Users extend
  `BaseExporter` for custom outputs.

- **`settings.py`** — `Settings` class. All mutable defaults are per-instance (not class-level) to
  prevent shared state. Key fields: `link_filter`, `max_depth` (default 10), `max_concurrency`
  (default 20), `caching`, `delta_crawl`, `exporters`. Enabling `delta_crawl` auto-enables caching.

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

```
User defines Microwler subclass (project file)
  → crawler.py fetches URLs asynchronously (aiohttp)
  → page.py scrapes each response using selectors from scrape.py
  → results collected in _results/_cache
  → export.py writes output via configured exporters
```

### File conventions

- Projects live in `./projects/` (single `.py` files)
- Disk cache stored at `./.microwler/cache/{domain}/`
- Exports written to `./exports/` by default
- Documentation source in `./docs/`, build output in `./site/`
