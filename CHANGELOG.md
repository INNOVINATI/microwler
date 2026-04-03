# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
