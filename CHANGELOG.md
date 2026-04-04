# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.9](https://github.com/INNOVINATI/microwler/compare/v0.1.8...v0.1.9) (2026-04-03)


### Features

* **types:** add py.typed marker for PEP 561 compliance ([5847968](https://github.com/INNOVINATI/microwler/commit/58479685b8078a0745a980f98724fcf5040ee269))


### Bug Fixes

* **ci:** add missing zensical dep and fix release-please config ([1dad1d3](https://github.com/INNOVINATI/microwler/commit/1dad1d38e2ee7f0434c4acf3d6f14d3e1fb4c23c))
* **ci:** correct release-please versioning strategy and Pages source ([cceb119](https://github.com/INNOVINATI/microwler/commit/cceb119521977f8f74a0bfe63a28c9673e4ea3d5))
* **ci:** remove unsupported changelog-type from release-please config ([6f421a3](https://github.com/INNOVINATI/microwler/commit/6f421a3b17d01bba9477c2fda722e4a309497993))
* **cli:** use ctx.obj['project'] in clear_cache command ([ebe7ab3](https://github.com/INNOVINATI/microwler/commit/ebe7ab37d1ae59b09e987b6ad66ced5e4cd0501e))
* **crawler:** replace deprecated event loop API with asyncio.run() ([14af65b](https://github.com/INNOVINATI/microwler/commit/14af65b3a7521433fa76ff5d1989f0aba0c1c565))
* **settings:** move mutable class defaults to __init__ ([361dcf2](https://github.com/INNOVINATI/microwler/commit/361dcf2a72f5047b91ef85a75bc22dc8bcc9ef08))
* **web:** remove event_loop param and use importlib.metadata for version ([cb73ebd](https://github.com/INNOVINATI/microwler/commit/cb73ebde958336634d3412c9ceea0e987e0da627))


### Documentation

* **claude:** update CLAUDE.md for modern toolchain ([60985d7](https://github.com/INNOVINATI/microwler/commit/60985d7d32a3e0fcbd99627dc0457178ebef8286))
* **zensical:** replace mkdocs with zensical ([f546377](https://github.com/INNOVINATI/microwler/commit/f54637748b79ab48fd9d4710dce59fdebfde978f))

## [Unreleased]

## [0.1.8] - 2021-04-01

### Added

- Initial public release
- Async web crawling engine (`Microwler` class) with configurable depth and concurrency
- Built-in CSS/XPath selectors (`title`, `headings`, `paragraphs`, `meta`, `emails`, `images`, `schemas`, `canonicals`)
- Plugin-based export system (`JSONExporter`, `CSVExporter`, `HTMLExporter`)
- Disk-based caching and delta-crawl support
- Click-based CLI (`microwler`, `new`, `crawler`, `serve`)
- Quart/Hypercorn REST API with Vue.js frontend
- MkDocs documentation site

[Unreleased]: https://github.com/INNOVINATI/microwler/compare/v0.1.8...HEAD
[0.1.8]: https://github.com/INNOVINATI/microwler/releases/tag/v0.1.8
