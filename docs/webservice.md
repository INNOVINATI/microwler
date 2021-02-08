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

## API

::: microwler.web.backend
    selection:
      members:
        - status
        - project
        - crawl
        - data
    rendering:
        heading_level: 3
        
## Microwler UI
Once the webservice is started, it will serve a NuxtJS application at `localhost:<PORT>/`

The application can be used as a convenient way to run crawlers and retrieve/monitor their data.
It consumes the API [described above](#api).

<img src="https://github.com/INNOVINATI/microwler/raw/master/docs/static/demo.gif" alt="Microwler UI">
