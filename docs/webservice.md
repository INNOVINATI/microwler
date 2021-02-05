# Web Service

**Microwler** ships with a JSON API 
built with [Quart](https://pypi.org/project/Quart/). It provides 
a simple way to run your crawlers and retrieve their scraped data via HTTP.

## Usage
To start the webservice, activate your workspace and run the following command:
```bash
serve
```

> Per default, this will start a production-ready ASGI application on `localhost:5000` using `Quart` with `hypercorn`.

You can customize the hostname and port:
```bash
serve [-p|--port PORT]
```

## Endpoints

::: microwler.web.backend
    selection:
      members:
        - status
        - project
        - crawl
        - data
    rendering:
        heading_level: 3