# Extensions
**Microwler** allows you to extend its functionality on-demand. For now, you can
create custom exporters. More extension points will follow soon.

## Transformers
It sounds more complex than it really is: a *transformer* is any Python callable
which works on a data dictionary. **Microwler** will inject every crawled page's data
into a given transformer function in order to provide a way for manipulating data after it has been scraped.

An example can be found [here](https://github.com/INNOVINATI/microwler/blob/master/examples/advanced.py).

## Exporters

### BaseExporter

::: microwler.export.BaseExporter
    rendering:
      show_source: true
      
### FileExporter

::: microwler.export.FileExporter
    rendering:
      show_source: true