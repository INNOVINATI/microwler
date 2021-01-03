# Data Exports
**Microwler** allows you to export scraped data to various formats.
You can build custom export plugins or use on of its pre-defined exporters:

- `microwler.core.export.JSONExporter`
- `microwler.core.export.CSVExporter`
- `microwler.core.export.HTMLExporter`

> Use the `export_to` and `exporters` settings to configure the export behaviour.


::: microwler.core.export.BaseExporter
    rendering:
      show_source: true
      show_root_heading: true

::: microwler.core.export.FileExporter
    rendering:
      show_source: true
      show_root_heading: true
