import json
import logging
import os
from datetime import datetime

from microwler.settings import Settings

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


class BaseExporter:
    """
    Use this class to build your custom export functionality, i.e. send data per HTTP or SMTP.
    The Crawler instance will call export() once it's done with everything else.
    You can plug your Exporter into the crawler by adding the class to settings['exporters']
    """

    def __init__(self, domain: str, data: list, settings: Settings):
        self.domain = domain
        self.data = data
        self.settings = settings

    def export(self):
        raise NotImplementedError()


class FileExporter(BaseExporter):
    extension = ''

    def convert(self):
        raise NotImplementedError()

    def export(self):
        data = self.convert()
        timestamp = datetime.now().strftime('%Y-%m-%d-%H:%M')
        path = os.path.join(self.settings.export_to, f'{self.domain}_{timestamp}.{self.extension}')
        try:
            os.makedirs(self.settings.export_to, exist_ok=True)
            with open(path, 'w') as file:
                file.write(data)
            logging.info(f'Exported data as {self.extension.upper()} to: {path}')
        except Exception as e:
            logging.error(f'Error during export: {e}')


class JSONExporter(FileExporter):
    extension = 'json'

    def convert(self):
        data = json.dumps(self.data)
        return data


class CSVExporter(FileExporter):
    extension = 'csv'

    def convert(self):
        # Flatten the result dicts and throw away the links
        flat = map(lambda obj: {'url': obj['url'], 'depth': obj['depth'], **obj.get('data', {})}, self.data)
        data = list(flat)
        headers = ';'.join([key.upper() for key in data[0].keys()])
        rows = '\n'.join([';'.join([str(val) for val in obj.values()]) for obj in data])
        table = '\n'.join([headers, rows])
        return table


class HTMLExporter(FileExporter):
    extension = 'html'

    def convert(self):
        flat = map(lambda obj: {'url': obj['url'], 'depth': obj['depth'], **obj.get('data', {})}, self.data)
        data = list(flat)
        styles = 'width: 100%; border: 1px solid grey; text-align: center'
        headers = ''.join([f'<th>{key.upper()}</th>' for key in data[0].keys()])
        rows = ''.join([f"<tr>{''.join([f'<td>{val}</td>' for val in obj.values()])}</tr>" for obj in data])
        table = f'<!DOCTYPE html><html><body><table style="{styles}"><tr>{headers}</tr><tbody>{rows}</tbody></table><body></html>'
        return table



