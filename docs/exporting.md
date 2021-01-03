# Data Exports
**Microwler** allows you to export scraped data to various formats.
You can build custom export plugins or use on of its pre-defined exporters:

- `microwler.export.JSONExporter`
- `microwler.export.CSVExporter`
- `microwler.export.HTMLExporter`

> Use the `export_to` and `exporters` settings to configure the export behaviour.


::: microwler.export.BaseExporter
    rendering:
      show_source: true
      show_root_heading: true

::: microwler.export.FileExporter
    rendering:
      show_source: true
      show_root_heading: true
