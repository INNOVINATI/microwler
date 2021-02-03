import os
from datetime import datetime


from microwler import PROJECT_FOLDER
from microwler.utils import load_project

STATUS = {
    'version': '0.1.7',
    'up_since': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
}

CACHE = dict()


def load_cache():
    for path in os.listdir(PROJECT_FOLDER):
        if path.endswith('.py'):
            name = path.split('.')[0]
            if name not in CACHE:
                project = load_project(name, PROJECT_FOLDER)
                CACHE[name] = {'name': name, 'start_url': project.crawler.start_url, 'last_run': dict()}


def job_stats():
    history = dict()
    for project_name in CACHE:
        project = load_project(project_name, project_folder=PROJECT_FOLDER)
        project.crawler.set_cache(force=True)
        for page in project.crawler.cache:
            history[page['discovered']] = page['discovered'] + 1 if page['discovered'] in history else 1
    return history
