import logging
import asyncio
import os
import time

import aioschedule as schedule
from diskcache import Index

from microwler import PROJECT_FOLDER
from microwler.utils import load_project

LOG = logging.getLogger(__name__)

PROJECT_CACHE = dict()
JOB_CACHE = dict()


async def sync_projects():
    for path in os.listdir(PROJECT_FOLDER):
        if path.endswith('.py'):
            name = path.split('.')[0]
            if name not in PROJECT_CACHE:
                project = load_project(name, PROJECT_FOLDER)
                PROJECT_CACHE[name] = {'name': name, 'start_url': project.crawler.start_url, 'last_run': dict()}


schedule.every(5).minutes.do(sync_projects)


async def _init(loop):
    await asyncio.ensure_future(schedule.run_all(), loop=loop)
    LOG.info(len(JOB_CACHE))


async def _run_forever(loop):
    while True:
        await asyncio.ensure_future(schedule.run_pending(), loop=loop)
        time.sleep(0.1)


def run_background_tasks(loop: asyncio.AbstractEventLoop):
    LOG.info('Starting task schedule ...')
    asyncio.ensure_future(_init(loop))
    scheduler = loop.create_task(_run_forever(loop))
    return scheduler
