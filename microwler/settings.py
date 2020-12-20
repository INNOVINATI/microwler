import os


class Settings(object):
    max_depth = 10
    max_concurrency = 20
    language = 'en-us'
    export_to = os.path.join(os.getcwd(), 'exports')
    exporters = []

    def __init__(self, param_dict=None):
        if param_dict:
            for key, value in param_dict.items():
                setattr(self, key, value)
