import os
from datetime import datetime

from diskcache import Index

from microwler import PROJECT_FOLDER

STATUS = {
    'version': '0.1.7',
    'up_since': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
}

CACHE = Index(os.path.join(os.getcwd(), '.microwler', 'cache', '__webservice__'))

if not len(CACHE):
    for path in os.listdir(PROJECT_FOLDER):
        if path.endswith('.py'):
            name = path.split('.')[0]
            CACHE[name] = {'name': name, 'jobs': 0, 'last_run': None}

