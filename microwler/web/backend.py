import asyncio
import logging
import os
from asyncio import Task
from datetime import datetime

from diskcache import Index
from quart import Quart, render_template, Response
from quart_cors import cors

from microwler.utils import load_project, PROJECT_FOLDER
from microwler.web.tasks import JOB_CACHE, PROJECT_CACHE, run_background_tasks

LOG = logging.getLogger(__name__)

app = Quart('Microwler', template_folder=os.path.join(os.path.dirname(__file__), 'frontend/dist'))
app = cors(app, allow_origin='*')
STATUS = {
    'version': '0.1.7',
    'up_since': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
}


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

    return {
        'app': STATUS,
        'projects': list(PROJECT_CACHE.keys()),
    }


@app.route('/status/<project_name>')
async def project(project_name):
    """
    Return the project status

    - Route: `/status/<str:project_name>`
    - Method: `GET`
    """

    return PROJECT_CACHE[project_name]


@app.route('/crawl/<project_name>')
async def crawl(project_name: str):
    """
    Run the project's crawler and return the results

    - Route: `/crawl/<str:project_name>`
    - Method: `GET`
    """
    PROJECT_CACHE[project_name]['last_run']['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M')
    try:
        project = load_project(project_name, project_folder=PROJECT_FOLDER)
        loop = asyncio.get_event_loop()
        project.crawler.set_cache(force=True)
        await project.crawler.run_async(event_loop=loop)
        PROJECT_CACHE[project_name]['last_run']['state'] = 'finished successfully'
        return {'data': project.crawler.results}
    except Exception as e:
        LOG.error(e)
        PROJECT_CACHE[project_name]['last_run']['state'] = f'failed because: {e}'
        return Response(str(e), status=500)


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

    LOG.info('Starting webservice...')
    config = Config()
    config.bind = [f'{host}:{port}']
    loop = asyncio.get_event_loop()
    scheduler = run_background_tasks(loop=loop)
    try:
        loop.run_until_complete(serve(app, config))
    finally:
        db = Index(os.path.join(os.getcwd(), '.microwler', 'cache', '__stats__'))
        for date, result_count in JOB_CACHE.items():
            if date not in db:
                db[date] = result_count
        scheduler.cancel()
        loop.close()


if __name__ == '__main__':
    start_app()
