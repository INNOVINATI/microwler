from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='microwler',
    version='0.1.8',
    description='A micro-framework for asynchronous deep crawls and web scraping written in Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://innovinati.github.io/microwler/',
    author='Maximilian Wolf',
    author_email='maximilian.wolf@innovinati.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Framework :: AsyncIO',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],
    packages=['microwler', 'microwler.cli', 'microwler.web'],
    include_package_data=True,
    python_requires='>=3.7, <4',
    install_requires=[
        'aiohttp', 'lxml', 'diskcache', 'prettytable', 'quart',
        'random-user-agent', 'html-text', 'completely', 'click',
        'parsel', 'chardet', 'quart-cors', 'aiodns'
    ],
    entry_points='''
    [console_scripts]
    microwler=microwler.cli.cmd:show_help
    new=microwler.cli.cmd:add_project
    crawler=microwler.cli.cmd:crawler
    serve=microwler.cli.cmd:start_server
    ''',
    project_urls={
        'Issues': 'https://github.com/INNOVINATI/microwler/issues',
        'Source': 'https://github.com/INNOVINATI/microwler/',
    },
)
