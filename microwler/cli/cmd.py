import os
from urllib.parse import urlparse

import click

from microwler.cli.template import TEMPLATE
from microwler.utils import load_project, PROJECT_FOLDER
from microwler.webservice import start_app

HERE = os.path.dirname(os.path.abspath(__file__))
COMMANDS = [
    ('new START_URL', 'Create a new project'),
    ('crawler PROJECT_NAME run', 'Run a project\'s crawler'),
    ('crawler PROJECT_NAME dumpcache', 'Dump project cache to JSON file'),
    ('crawler PROJECT_NAME clearcache', 'Clear project cache'),
    ('serve [-p|--port]', 'Start the built-in webservice'),
]


@click.command()
def microwler():
    """ Show available commands """
    click.echo(
        """
╔╦╗┬┌─┐┬─┐┌─┐┬ ┬┬  ┌─┐┬─┐
║║║││  ├┬┘│ │││││  ├┤ ├┬┘
╩ ╩┴└─┘┴└─└─┘└┴┘┴─┘└─┘┴└─            
- powered by INNOVINATI -                                                                              
        """
    )
    print('USAGE:')
    for cmd, description in COMMANDS:
        print(f'> {description}:\n  {cmd}\n')


@click.command()
@click.argument('start_url', type=str)
def add_project(start_url):
    """ Create a new project """
    project = urlparse(start_url).netloc.replace('.', '_')
    os.makedirs(PROJECT_FOLDER, exist_ok=True)
    template = TEMPLATE.replace('START_URL', start_url)
    with open(os.path.join(PROJECT_FOLDER, project + '.py'), 'w') as output:
        output.write(template)


@click.group()
@click.argument('project_name')
@click.pass_context
def crawler(ctx, project_name):
    ctx.ensure_object(dict)
    project = project_name.split('.')[0] if project_name.endswith('.py') else project_name
    ctx.obj['project'] = project


@crawler.command('run')
@click.option('-v', '--verbose', default=False, is_flag=True)
@click.option('-s', '--sort', default=False, is_flag=True)
@click.option('--keep-html', default=False, is_flag=True)
@click.pass_context
def run(ctx, verbose, sort, keep_html):
    """ Run a project's crawler"""
    project = load_project(ctx.obj['project'])
    project.crawler.run(verbose=verbose, sort_urls=sort, keep_source=keep_html)


@crawler.command('dumpcache')
@click.option('-p', '--path')
@click.pass_context
def dump_cache(ctx, path):
    """ Dump the project cache to a JSON file """
    project = load_project(ctx.obj['project'])
    if len(project.crawler._cache):
        project.crawler.dump_cache(path)
    else:
        click.echo('Cache is disabled for this project')


@crawler.command('clearcache')
@click.pass_context
def clear_cache(ctx):
    """ Clear the project cache """
    project = load_project(ctx['project'])
    if len(project.crawler._cache):
        project.crawler.clear_cache()
    else:
        click.echo('Cache is disabled for this project')


@click.command('serve')
@click.option('-p', '--port', type=int, default=5000, help='The port to run the webservice on.')
def serve(port):
    """ Start the built-in webservice """
    start_app(port)
