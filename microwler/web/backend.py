import asyncio
import logging
import os
from datetime import datetime

from quart import Quart, Response, send_from_directory
from quart_cors import cors

from microwler.utils import load_project, PROJECT_FOLDER

LOG = logging.getLogger(__name__)

app = Quart('Microwler')
app = cors(app, allow_origin='*')

STATIC = os.path.join(os.path.dirname(__file__), 'frontend/dist')
PROJECTS = dict()
STATUS = {
    'version': '0.1.8',
    'up_since': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
}


async def load_projects():
    global PROJECTS
    copy = dict()
    for path in os.listdir(PROJECT_FOLDER):
        if path.endswith('.py'):
            name = path.split('.')[0]
            project = load_project(name, PROJECT_FOLDER)
            if name in PROJECTS:
                PROJECTS[name]['start_url'] = project.crawler.start_url
                copy[name] = PROJECTS[name]
            else:
                copy[name] = {'name': name, 'start_url': project.crawler.start_url, 'last_run': dict()}
    PROJECTS = copy
    LOG.info(f'Imported {len(PROJECTS)} projects from filesystem')


@app.before_serving
async def init():
    await load_projects()


@app.route('/status')
async def status():
    """
    Return the service status

    - Route: `/status`
    - Method: `GET`
    - Response example:
    ```json
    {
        app: {
            up_since: "2021-02-05 17:42:13",
            version: "0.1.7"
        },
        projects: [
            "quotes"
        ]
    }
    ```
    """
    files = [file for file in os.listdir(PROJECT_FOLDER) if file.endswith('.py')]
    if len(files) != len(PROJECTS):
        await load_projects()

    return {
        'app': STATUS,
        'projects': list(PROJECTS.keys()),
    }


@app.route('/status/<project_name>')
async def project(project_name):
    """
    Return the project status

    - Route: `/status/<str:project_name>`
    - Method: `GET`
    - Response example:
    ```json
    {
        name: "quotes",
        start_url: "https://quotes.toscrape.com/"
        last_run: {
            state: "finished successfully",
            timestamp: "2021-02-05 17:47"
        },
    }
    ```
    """

    return PROJECTS[project_name]


@app.route('/crawl/<project_name>')
async def crawl(project_name: str):
    """
    Run the project's crawler and return the results

    - Route: `/crawl/<str:project_name>`
    - Method: `GET`
    - Response example:
    ```
    {
        data: [
            {
                url: "https://quotes.toscrape.com/"
                status_code: 200,
                depth: 0,
                discovered: "2021-02-05",
                links: [
                    "https://quotes.toscrape.com/tag/inspirational/",
                    "https://quotes.toscrape.com/author/Jane-Austen",
                    "https://quotes.toscrape.com/tag/obvious/page/1/",
                    "https://quotes.toscrape.com/tag/friends/",
                    "https://quotes.toscrape.com/tag/misattributed-eleanor-roosevelt/page/1/",
                    ...
                ],
                data: {
                    title: "Quotes to Scrape"
                    headings: {
                        h1: ["Quotes to Scrape"],
                        h2: ["Top Ten tags"],
                        h3: [""]
                    },
                },
            },
            ...
        ]
    }
    ```
    """
    PROJECTS[project_name]['last_run']['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M')
    try:
        project = load_project(project_name, project_folder=PROJECT_FOLDER)
        loop = asyncio.get_event_loop()
        project.crawler.set_cache(force=True)
        await project.crawler.run_async(event_loop=loop)
        PROJECTS[project_name]['last_run']['state'] = 'finished successfully'
        return {'data': project.crawler.results}
    except Exception as e:
        LOG.error(e)
        PROJECTS[project_name]['last_run']['state'] = f'failed because: {e}'
        return Response(str(e), status=500)


@app.route('/data/<project_name>')
async def data(project_name: str):
    """
    Return the project's cached data

    - Route: `/data/<str:project_name>`
    - Method: `GET`
    - Response is in the same format as [above][microwler.web.backend.crawl]
    """
    project = load_project(project_name, project_folder=PROJECT_FOLDER)
    project.crawler.set_cache(force=True)
    cache = project.crawler.cache
    response = {'data': cache}
    return response


@app.route('/<folder>/<file>', methods=['GET'])
async def serve_folder(folder, file):
    return await send_from_directory(os.path.join(STATIC, folder), file)


@app.route('/<file>', methods=['GET'])
async def serve_file(file):
    return await send_from_directory(STATIC, file)


@app.route('/', methods=['GET'])
async def serve_index():
    return await send_from_directory(STATIC, 'index.html')


def start_app(port: int = 5000):
    """
    Starts the production-ready ASGI application using Hypercorn
    Arguments:
         port: the port to run on
    """
    from hypercorn.asyncio import serve
    from hypercorn.config import Config

    LOG.info('Starting webservice...')
    config = Config()
    config.bind = [f'localhost:{port}']
    config.loglevel = 'WARNING'
    try:
        LOG.info(f'Running on http://localhost:{port} (CTRL + C to quit)')
        asyncio.run(serve(app, config))
    except Exception as e:
        LOG.error(e)


if __name__ == '__main__':
    start_app()
