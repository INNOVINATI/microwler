import asyncio
import logging
import os
from datetime import datetime

from quart import Quart, render_template
from quart_cors import cors

from microwler.utils import load_project, PROJECT_FOLDER
from microwler.web import STATUS, CACHE, load_cache

LOG = logging.getLogger(__name__)

app = Quart('Microwler', template_folder=os.path.join(os.path.dirname(__file__), 'frontend/dist'))
app = cors(app, allow_origin='*')
load_cache()    # TODO: Use something like schedule to run this every couple of minutes


@app.route('/')
async def frontend():
    pass


@app.route('/status')
async def status():
    """
    Return the service status

    - Route: `/status`
    - Method: `GET`
    """
    return {'app': STATUS, 'projects': list(CACHE.keys())}


@app.route('/status/<project_name>')
async def project(project_name):
    """
    Return the project status

    - Route: `/status/<str:project_name>`
    - Method: `GET`
    """
    project = load_project(project_name, project_folder=PROJECT_FOLDER)
    project.crawler.set_cache(force=True)
    history = dict()
    for page in project.crawler.cache:
        history[page['discovered']] = page['discovered'] + 1 if page['discovered'] in history else 1
    return {'data': CACHE[project_name], 'jobs': {'dates': list(history.keys()), 'counts': list(history.values())}}


@app.route('/crawl/<project_name>')
async def crawl(project_name: str):
    """
    Run the project's crawler and return the results

    - Route: `/crawl/<str:project_name>`
    - Method: `GET`
    """
    CACHE[project_name]['last_run']['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M')
    try:
        project = load_project(project_name, project_folder=PROJECT_FOLDER)
        loop = asyncio.get_event_loop()
        project.crawler.set_cache(force=True)
        await project.crawler.run_async(event_loop=loop)
        CACHE[project_name]['last_run']['state'] = 'finished successfully'
        return {'data': project.crawler.results}
    except Exception as e:
        LOG.error(e)
        CACHE[project_name]['last_run']['state'] = 'failed'
        return {'error': str(e)}


@app.route('/data/<project_name>')
async def data(project_name: str):
    """
    Return the project's cached data

    - Route: `/data/<str:project_name>`
    - Method: `GET`
    """
    project = load_project(project_name, project_folder=PROJECT_FOLDER)
    project.crawler.set_cache(force=True)
    cache = project.crawler.cache
    response = {'data': cache}
    return response


def start_app(host='localhost', port=5000):
    from hypercorn.asyncio import serve
    from hypercorn.config import Config

    config = Config()
    config.bind = [f'{host}:{port}']
    asyncio.run(serve(app, config))


if __name__ == '__main__':
    start_app()
