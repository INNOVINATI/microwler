TEMPLATE = """# This file was auto-generated by Microwler

# Use this template as starting point for your new project.
# To find out more about configuration options, read the docs: https://innovinati.github.io/microwler


from microwler import Microwler, scrape, export


select = {
    # add selectors here
}

settings = {
    # add settings here
}


def transform(data: dict):
    # Manipulate data here
    return data


# Microwler expects a variable "crawler" when running from CLI
crawler = Microwler(
    'START_URL',
    selectors=select,
    transformer=transform,
    settings=settings
)
"""
