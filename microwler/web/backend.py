import asyncio
import logging
import os
from datetime import datetime

from quart import Quart, render_template, Response
from quart_cors import cors

from microwler.utils import load_project, PROJECT_FOLDER

LOG = logging.getLogger(__name__)

app = Quart('Microwler', template_folder=os.path.join(os.path.dirname(__file__), 'frontend/dist'))
app = cors(app, allow_origin='*')

PROJECTS = dict()
STATUS = {
    'version': '0.1.7',
    'up_since': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
}


async def load_projects():
    for path in os.listdir(PROJECT_FOLDER):
        if path.endswith('.py'):
            name = path.split('.')[0]
            project = load_project(name, PROJECT_FOLDER)
            PROJECTS[name] = {'name': name, 'start_url': project.crawler.start_url, 'last_run': dict()}
    LOG.info(f'Imported {len(PROJECTS)} projects')


@app.before_serving
async def init():
    await load_projects()


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
    """

    return PROJECTS[project_name]


@app.route('/crawl/<project_name>')
async def crawl(project_name: str):
    """
    Run the project's crawler and return the results

    - Route: `/crawl/<str:project_name>`
    - Method: `GET`
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
    config.loglevel = 'WARNING'
    try:
        LOG.info(f'Running on http://{host}:{port} (CTRL + C to quit)')
        asyncio.run(serve(app, config))
    except Exception as e:
        LOG.error(e)
        exit(1)


if __name__ == '__main__':
    start_app()
