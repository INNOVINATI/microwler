import os

import click

from microwler.cli.template import TEMPLATE
from microwler.utils import load_project, PROJECT_FOLDER
from microwler.web.backend import start_app


@click.group()
def cli():
    """
    \b
╔╦╗┬┌─┐┬─┐┌─┐┬ ┬┬  ┌─┐┬─┐
║║║││  ├┬┘│ │││││  ├┤ ├┬┘
╩ ╩┴└─┘┴└─└─┘└┴┘┴─┘└─┘┴└─
- powered by INNOVINATI -
    """
    pass


@cli.command('create')
@click.argument('project_name', type=str)
@click.argument('start_url', type=str)
def add_project(project_name, start_url):
    """ Create a new project. """
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


def retrieve_project(ctx, param, project_name):
    project = project_name[:-
                           3] if project_name.endswith('.py') else project_name
    if project + '.py' not in os.listdir(PROJECT_FOLDER):
        raise click.BadArgumentUsage(f'Project "{project}" does not exist')
    return load_project(project)


@cli.command('run')
@click.argument('project', callback=retrieve_project)
@click.option('-v', '--verbose', default=False, is_flag=True)
@click.option('--keep-html', default=False, is_flag=True)
def run_crawler(project, verbose, keep_html):
    """ Run a project's crawler. """
    project.crawler.run(verbose=verbose, keep_source=keep_html)


@cli.group()
def cache():
    """ Subcommand to handle project cache. """
    pass


@cache.command('dump')
@click.argument('project', callback=retrieve_project)
@click.option('-p', '--path')
def dump_cache(project, path):
    """ Dump the project cache to a JSON file. """
    if project.crawler._cache is not None:
        project.crawler.dump_cache(path)
    else:
        click.secho('Cache is disabled for this project', fg='yellow')


@cache.command('clear')
@click.argument('project', callback=retrieve_project)
def clear_cache(project):
    """ Clear the project cache. """
    if project.crawler._cache is not None:
        project.crawler.clear_cache()
    else:
        click.secho('Cache is disabled for this project', fg='yellow')


@cli.command('serve')
@click.option('-p', '--port', type=int, default=5000, metavar='PORT', help='The port to run the webservice on.')
def start_server(port):
    """ Start the built-in webservice. """
    start_app(port)
