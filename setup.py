from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='microwler',
    version='0.0.9',
    description='A micro-framework for deep crawls and scraping written in Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/INNOVINATI/microwler',
    author='Maximilian Wolf',
    author_email='maximilian.wolf@innovinati.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],
    package_dir={'': 'microwler'},
    packages=find_packages(where='microwler'),
    python_requires='>=3.6, <4',
    install_requires=['aiohttp', 'lxml', 'prettytable', 'random-user-agent'],
    project_urls={
        'Bug Reports': 'https://github.com/INNOVINATI/microwler/issues',
        'Source': 'https://github.com/INNOVINATI/microwler/',
    },
)