import json
import logging
import os
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


class BaseExporter:

    def __init__(self, crawler):
        self.crawler = crawler

    def convert(self):
        raise NotImplementedError()

    def export(self, data: str, extension: str):
        timestamp = datetime.now().strftime('%Y-%m-%d-%H:%M')
        path = os.path.join(self.crawler.settings.export_to, f'{timestamp}.{extension}')
        try:
            if not os.path.exists(self.crawler.settings.export_to):
                os.mkdir(self.crawler.settings.export_to)
            with open(path, 'w') as file:
                file.write(data)
            logging.info(f'Exported data to: {path}')
        except Exception as e:
            logging.error(f'Error during export: {e}')


class JSONExporter(BaseExporter):

    def convert(self):
        data = json.dumps(self.crawler.data)
        self.export(data, 'json')


class CSVExporter(BaseExporter):

    def convert(self):
        # Flatten the result dicts and throw away the links
        flat = map(lambda obj: {'url': obj['url'], 'depth': obj['depth'], **obj.get('data', {})}, self.crawler.data)
        data = list(flat)
        headers = ';'.join([key for key in data[0].keys()])
        rows = [';'.join([val for val in obj.values()]) for obj in data]
        table = '\n'.join([headers, rows])
        self.export(table, 'csv')


