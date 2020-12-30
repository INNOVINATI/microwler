from setuptools import setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='microwler',
    version='0.1.2',
    description='A micro-framework for asynchronous deep crawls and web scraping written in Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://innovinati.github.io/microwler/',
    author='Maximilian Wolf',
    author_email='maximilian.wolf@innovinati.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Framework :: AsyncIO',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],
    packages=['microwler'],
    python_requires='>=3.6, <4',
    install_requires=[
        'aiohttp', 'lxml', 'diskcache',
        'prettytable', 'random-user-agent',
        'html-text', 'completely', 'click'
    ],
    entry_points='''
    [console_scripts]
    microwler=microwler.cmd:microwler
    new=microwler.cmd:add_project
    crawler=microwler.cmd:crawler
    ''',
    project_urls={
        'Bug Reports': 'https://github.com/INNOVINATI/microwler/issues',
        'Source': 'https://github.com/INNOVINATI/microwler/',
    },
)
