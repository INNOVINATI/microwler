import os
import sys
from urllib.parse import urlparse

import click
from click.testing import CliRunner

from microwler.cli.template import TEMPLATE
from microwler.utils import load_project, PROJECT_FOLDER
from microwler.web.backend import start_app

HERE = os.path.dirname(os.path.abspath(__file__))
COMMANDS = [
    ('new PROJECT_NAME START_URL', 'Create a new project'),
    ('crawler PROJECT_NAME run', 'Run a project\'s crawler'),
    ('crawler PROJECT_NAME dumpcache', 'Dump project getCache to JSON file'),
    ('crawler PROJECT_NAME clearcache', 'Clear project getCache'),
    ('serve [-p|--port]', 'Start the built-in webservice'),
]


@click.command('microwler')
def show_help():
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
@click.argument('project_name', type=str)
@click.argument('start_url', type=str)
def add_project(project_name, start_url):
    """ Create a new project """
    try:
        os.makedirs(PROJECT_FOLDER, exist_ok=True)
        template = TEMPLATE.replace('START_URL', start_url)
        name = project_name.replace(' ', '_').replace('.', '_').replace('-', '_').lower()
        path = os.path.join(PROJECT_FOLDER, name + '.py')
        if os.path.exists(path):
            question = click.style('A project with this name already exists. Do you want to overwrite it?', fg='yellow')
            if not click.confirm(question):
                exit(0)
        with open(path, 'w') as output:
            output.write(template)
        click.secho(f'Created new project: {path}', fg='green')
    except Exception as e:
        click.secho(f'Failed to create project: {e}', fg='red')
        exit(1)


@click.group()
@click.argument('project_name')
@click.pass_context
def crawler(ctx, project_name):
    ctx.ensure_object(dict)
    project = project_name.split('.')[0] if project_name.endswith('.py') else project_name
    if project + '.py' not in os.listdir(PROJECT_FOLDER):
        click.secho(f'Project "{project}" does not exist', fg='red')
        exit(1)
    ctx.obj['project'] = project


@crawler.command('run')
@click.option('-v', '--verbose', default=False, is_flag=True)
@click.option('-s', '--sort', default=False, is_flag=True)
@click.option('--keep-html', default=False, is_flag=True)
@click.pass_context
def run_crawler(ctx, verbose, sort, keep_html):
    """ Run a project's crawler"""
    project = load_project(ctx.obj['project'])
    project.crawler.run(verbose=verbose, sort_urls=sort, keep_source=keep_html)


@crawler.command('dumpcache')
@click.option('-p', '--path')
@click.pass_context
def dump_cache(ctx, path):
    """ Dump the project getCache to a JSON file """
    project = load_project(ctx.obj['project'])
    if project.crawler._cache is not None:
        project.crawler.dump_cache(path)
    else:
        click.secho('Cache is disabled for this project', fg='yellow')


@crawler.command('clearcache')
@click.pass_context
def clear_cache(ctx):
    """ Clear the project getCache """
    project = load_project(ctx['project'])
    if project.crawler._cache is not None:
        project.crawler.clear_cache()
    else:
        click.secho('Cache is disabled for this project', fg='yellow')


@click.command('serve')
@click.option('-p', '--port', type=int, default=5000, help='The port to run the webservice on.')
def start_server(port):
    """ Start the built-in webservice """
    if not len(os.listdir(PROJECT_FOLDER)):
        click.secho('Running webservice with empty project folder', fg='yellow')
    start_app(port)
