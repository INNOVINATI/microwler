import os


class Settings(object):
    max_depth: int = 10
    max_concurrency: int = 20
    language: str = 'en-us'
    export_to = os.path.join(os.getcwd(), 'exports')
    exporters: list = []

    def __init__(self, params: dict):
        if params:
            for key, value in params.items():
                setattr(self, key, value)
