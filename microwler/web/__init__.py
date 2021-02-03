import os
from datetime import datetime

from diskcache import Index

from microwler import PROJECT_FOLDER
from microwler.utils import load_project

STATUS = {
    'version': '0.1.7',
    'up_since': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
}

CACHE = Index(os.path.join(os.getcwd(), '.microwler', 'cache', '__webservice__'))

if not len(CACHE):
    for path in os.listdir(PROJECT_FOLDER):
        if path.endswith('.py'):
            name = path.split('.')[0]
            if name not in CACHE:
                project = load_project(name, PROJECT_FOLDER)
                CACHE[name] = {'name': name, 'start_url': project.crawler.start_url, 'jobs': 0, 'last_run': None}
