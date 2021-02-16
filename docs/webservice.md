# Web Service

**Microwler** provides a simple JSON API 
built with [Quart](https://pypi.org/project/Quart/). It provides 
another way to run your crawlers and retrieve their scraped data via HTTP.

## Usage
<div id="termynal" data-termynal>
    <span data-ty="input">serve</span>
    <span data-ty>[INFO] Starting webservice...</span>
    <span data-ty>[INFO] Running on http://localhost:5000 (CTRL + C to quit)</span>
    <span data-ty>[INFO] Imported 1 projects from filesystem</span>
</div>

> Per default, this will start a production-ready ASGI application on `localhost:5000` using `Quart` with `hypercorn`.

You may change the port:
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
<script src="/js/termynal.js" data-termynal-container="#termynal"></script>
