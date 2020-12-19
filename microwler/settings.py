import os


class Settings(object):
    max_concurrency = 100
    download_delay = 1
    language = 'en-us'
    export_to = os.path.join(os.getcwd(), 'exports')
    exporters = []

    def __init__(self, param_dict=None):
        if param_dict:
            for key, value in param_dict.items():
                setattr(self, key, value)
