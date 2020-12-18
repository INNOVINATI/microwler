class Settings(object):

    def __init__(self, params: dict):
        self.max_concurrency = params.get('max_concurrency', 100),
        self.download_delay = params.get('download_delay', 3),
        self.language = params.get('language', 'en-us'),
        self.storage = params.get('storage', None)
