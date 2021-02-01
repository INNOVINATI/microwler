import asyncio
import logging
import os
import time
from datetime import datetime
import aiohttp
from quart import Quart, render_template
from quart_cors import cors

from microwler.utils import load_project, PROJECT_FOLDER

LOG = logging.getLogger(__name__)

app = Quart('Microwler', template_folder=os.path.dirname(__file__))
app = cors(app, allow_origin='*')

PROJECTS = dict()

for path in os.listdir(PROJECT_FOLDER):
    if path.endswith('.py'):
        name = path.split('.')[0]
        PROJECTS[name] = {'name': name, 'jobs': 0, 'last_run': None}


@app.route('/')
async def frontend():
    return await render_template('frontend.html')


@app.route('/status')
async def status():
    """
    Return the service status

    - Route: `/status`
    - Method: `GET`
    """
    status = {
        'version': '0.1.7',
        'up_since': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    
    return {'app': status, 'projects': list(PROJECTS.keys())}


@app.route('/status/<project_name>')
async def project(project_name):
    """
    Return the project status

    - Route: `/status/<str:project_name>`
    - Method: `GET`
    """
    project = load_project(project_name, project_folder=PROJECT_FOLDER)
    project.crawler._init_cache()

    return {**PROJECTS[project_name], 'cache_size': len(project.crawler._cache)}


@app.route('/crawl/<project_name>')
async def crawl(project_name: str):
    """
    Run the project's crawler and return the results

    - Route: `/crawl/<str:project_name>`
    - Method: `GET`
    """
    try:
        start = time.time()
        project = load_project(project_name, project_folder=PROJECT_FOLDER)
        PROJECTS[project_name]['jobs'] += 1
        loop = asyncio.get_event_loop()
        project.crawler._session = aiohttp.ClientSession(loop=loop)
        # Force disk caching
        project.crawler._settings.caching = True
        project.crawler._init_cache()
        # Note: instead of using crawler.run() we use crawler._crawl directly to gain control over the whole workflow
        await loop.create_task(project.crawler._crawl())
        project.crawler._process()
        PROJECTS[project_name]['last_run'] = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'successful': True
        }
        PROJECTS[project_name]['jobs'] -= 1
        return {
            'project': project_name,
            'duration': f'{round(time.time() - start, 3)}s',
            'results': [page.__dict__ for page in project.crawler.pages]
        }
    except Exception as e:
        LOG.error(e)
        PROJECTS[project_name]['jobs'] -= 1
        PROJECTS[project_name]['last_run'] = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'successful': False
        }
        return {'error': str(e)}


@app.route('/data/<project_name>')
async def data(project_name: str):
    """
    Return the project's cached data

    - Route: `/data/<str:project_name>`
    - Method: `GET`
    """
    project = load_project(project_name, project_folder=PROJECT_FOLDER)
    return {
        'project': project_name,
        'last_run': PROJECTS[project_name]['last_run'],
        'results': [page.__dict__ for page in project.crawler.cache]
    }


def start_app(host='localhost', port=5000):
    from hypercorn.asyncio import serve
    from hypercorn.config import Config

    config = Config()
    config.bind = [f'{host}:{port}']
    asyncio.run(serve(app, config))


if __name__ == '__main__':
    start_app()
