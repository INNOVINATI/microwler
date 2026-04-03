import asyncio
import logging
import os
from datetime import datetime
from importlib.metadata import version

from quart import Quart, Response, send_from_directory
from quart_cors import cors

from microwler.utils import PROJECT_FOLDER, load_project

LOG = logging.getLogger(__name__)

app = Quart("Microwler")
app = cors(app, allow_origin="*")

STATIC = os.path.join(os.path.dirname(__file__), "frontend/dist")
PROJECTS: dict = {}

# importlib.metadata reads the installed package version at runtime, so the version
# string stays correct after upgrades without needing manual edits in source code.
STATUS = {
    "version": version("microwler"),
    "up_since": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
}


async def load_projects() -> None:
    global PROJECTS
    copy: dict = {}
    for path in os.listdir(PROJECT_FOLDER):
        if path.endswith(".py"):
            name = path.split(".")[0]
            project = load_project(name, PROJECT_FOLDER)
            if name in PROJECTS:
                PROJECTS[name]["start_url"] = project.crawler.start_url
                copy[name] = PROJECTS[name]
            else:
                copy[name] = {
                    "name": name,
                    "start_url": project.crawler.start_url,
                    "last_run": {},
                }
    PROJECTS = copy
    LOG.info(f"Imported {len(PROJECTS)} projects from filesystem")


@app.before_serving
async def init() -> None:
    await load_projects()


@app.route("/status")
async def status():
    """
    Return the service status.

    - Route: `/status`
    - Method: `GET`
    - Response example:
    ```json
    {
        "app": {
            "up_since": "2021-02-05 17:42:13",
            "version": "0.1.8"
        },
        "projects": ["quotes"]
    }
    ```
    """
    files = [file for file in os.listdir(PROJECT_FOLDER) if file.endswith(".py")]
    if len(files) != len(PROJECTS):
        await load_projects()

    return {
        "app": STATUS,
        "projects": list(PROJECTS.keys()),
    }


@app.route("/status/<project_name>")
async def project(project_name: str):
    """
    Return the project status.

    - Route: `/status/<str:project_name>`
    - Method: `GET`
    - Response example:
    ```json
    {
        "name": "quotes",
        "start_url": "https://quotes.toscrape.com/",
        "last_run": {
            "state": "finished successfully",
            "timestamp": "2021-02-05 17:47"
        }
    }
    ```
    """
    return PROJECTS[project_name]


@app.route("/crawl/<project_name>")
async def crawl(project_name: str):
    """
    Run the project's crawler and return the results.

    - Route: `/crawl/<str:project_name>`
    - Method: `GET`
    - Response example:
    ```json
    {
        "data": [
            {
                "url": "https://quotes.toscrape.com/",
                "status_code": 200,
                "depth": 0,
                "discovered": "2021-02-05",
                "links": ["https://quotes.toscrape.com/tag/inspirational/", "..."],
                "data": {"title": "Quotes to Scrape"}
            }
        ]
    }
    ```
    """
    PROJECTS[project_name]["last_run"]["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    try:
        project = load_project(project_name, project_folder=PROJECT_FOLDER)
        project.crawler.set_cache(force=True)
        # run_async() is awaited directly — Quart's Hypercorn-managed loop owns the
        # scheduling context, so no loop reference needs to be threaded through.
        await project.crawler.run_async()
        PROJECTS[project_name]["last_run"]["state"] = "finished successfully"
        return {"data": project.crawler.results}
    except Exception as e:
        LOG.error(e)
        PROJECTS[project_name]["last_run"]["state"] = f"failed because: {e}"
        return Response(str(e), status=500)


@app.route("/data/<project_name>")
async def data(project_name: str):
    """
    Return the project's cached data.

    - Route: `/data/<str:project_name>`
    - Method: `GET`
    - Response is in the same format as `/crawl/<project_name>`.
    """
    project = load_project(project_name, project_folder=PROJECT_FOLDER)
    project.crawler.set_cache(force=True)
    cache = project.crawler.cache
    return {"data": cache}


@app.route("/<folder>/<file>", methods=["GET"])
async def serve_folder(folder: str, file: str):
    return await send_from_directory(os.path.join(STATIC, folder), file)


@app.route("/<file>", methods=["GET"])
async def serve_file(file: str):
    return await send_from_directory(STATIC, file)


@app.route("/", methods=["GET"])
async def serve_index():
    return await send_from_directory(STATIC, "index.html")


def start_app(port: int = 5000) -> None:
    """
    Start the production ASGI server via Hypercorn.

    Arguments:
        port: TCP port to bind to
    """
    from hypercorn.asyncio import serve
    from hypercorn.config import Config

    LOG.info("Starting webservice...")
    config = Config()
    config.bind = [f"localhost:{port}"]
    config.loglevel = "WARNING"
    try:
        LOG.info(f"Running on http://localhost:{port} (CTRL + C to quit)")
        asyncio.run(serve(app, config))
    except Exception as e:
        LOG.error(e)


if __name__ == "__main__":
    start_app()
