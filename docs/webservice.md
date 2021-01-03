# Web Service

**Microwler** comes with a production-ready JSON API 
built with [Quart](https://pypi.org/project/Quart/). It provides 
a simple way to run your crawlers and retrieve their scraped data via HTTP.

## Usage
To start the webservice, activate your workspace and run the following command:
```bash
serve
```

> This will start a production-ready ASGI server on `localhost:5000` using `Quart` with `hypercorn`.

You can also define a different port:
```bash
serve [-p|--port] 8080
```

## Endpoints

::: microwler.webservice.status
    rendering:
          show_root_heading: true
          
::: microwler.webservice.crawl
    rendering:
          show_root_heading: true
          
::: microwler.webservice.data
    rendering:
          show_root_heading: true