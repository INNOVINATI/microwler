import asyncio
import os
import time
from datetime import datetime
import aiohttp
from quart import Quart

from microwler.utils import load_project, PROJECT_FOLDER

app = Quart('Microwler')

META = {
    'app': {
        'version': '0.1.3',
        'up_since': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    },
    'projects': {path.split('.')[0]: {'running': False, 'last_run': None}
                 for path in os.listdir(PROJECT_FOLDER) if path.endswith('.py')}
}


@app.route('/')
async def status():
    """
    Return the service status

    - Route: `/`
    - Method: `GET`
    """
    return dict(META)


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
        if not META['projects'][project_name]['running']:
            META['projects'][project_name]['running'] = True
        loop = asyncio.get_event_loop()
        project.crawler._session = aiohttp.ClientSession(loop=loop)
        project.crawler._settings.caching = True    # Force disk caching
        await loop.create_task(project.crawler._crawl())
        project.crawler._process()
        META['projects'][project_name]['last_run'] = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'successful': True
        }
        return {'project': project_name, 'duration': time.time() - start, 'results': [page.__dict__ for page in project.crawler.pages]}
    except Exception as e:
        META['projects'][project_name]['last_run'] = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'successful': False
        }
        return {'error': str(e)}
    finally:
        META['projects'][project_name]['running'] = False


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
        'last_run': META['projects'][project_name]['last_run'],
        'results': [page.__dict__ for page in project.crawler.cache]
    }


def start_app(port=5000):
    from hypercorn.asyncio import serve
    from hypercorn.config import Config

    config = Config()
    config.bind = [f'0.0.0.0:{port}']
    asyncio.run(serve(app, config))
