# Getting Started

## Installation
Before you start, create a workspace/folder for **Microwler** projects and enter it:
```bash
mkdir microwler && cd $_
```

Now, create a virtual environment using Python 3.7 or higher and activate it:
```bash
virtualenv venv -p python3.x && source venv/bin/activate
```

Install `microwler` from PyPI:
```bash
pip install microwler
```

## Usage
### CLI (recommended)
#### Create a project
Make sure you created a workspace as suggested in the [previous section](#installation). 
Within that folder, create a new project providing a name and the URL to start crawling with:
```bash
new quotes https://quotes.toscrape.com/
```
Microwler will create a `projects/` folder in your current working directory and place
a file called `quotes.py` within it. This file contains your [crawler configuration](/microwler/configuration).

#### Run the project/crawler
To run this project, execute the following command:
```bash
crawler quotes run
```
> Note: Depending on your setup, this will create a `.microwler` folder in your workspace
> where internal stuff like caches will be stored. Mess with it at your own risk!

#### Check available commands
You can check available commands with:
```bash
microwler
```

### Script
> **Important**: If you're planning on using the webservice or the "project" system in general, you should use the CLI
as recommended above. It will create an optimized workspace in which you can develop and run your projects.

#### Run directly

Simply create a crawler instance and `run` it:

```python
from microwler import Microwler

crawler = Microwler('https://quotes.toscrape.com/')
crawler.run(verbose=True)
for page in crawler.results:
    print(page)
```

#### Run from asyncio app

If you want to start your crawler from an application that is already running an `asyncio` event loop,
you should use `Microwler.run_async(loop)`. Here's a simple example:

```python
...
crawler = Microwler(...)
loop = asyncio.get_event_loop()
await crawler.run_async(event_loop=loop)
print(crawler.results)
```
