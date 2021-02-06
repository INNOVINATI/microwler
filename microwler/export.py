import json
import logging
import os
from datetime import datetime

from microwler.settings import Settings

LOG = logging.getLogger(__name__)


class BaseExporter:
    """
    Use this class to build your custom export functionality, i.e. send data per HTTP or SMTP.
    The crawler instance will call `export()` once it's done with everything else.
    You can pass your plugin into the crawler by adding the class to `settings['exporters']`
    """

    def __init__(self, domain: str, data: list, settings: Settings):
        """
        Create a new BaseExporter

        Arguments:
            domain: the domain of this project/crawler
            data: list of processed Page objects
            settings: the current settings of this project/crawler
        """
        self.domain = domain
        self.data = [page.__dict__ for page in data]
        self.settings = settings

    def export(self):
        """
        Export data to target destination
        """
        raise NotImplementedError()


class FileExporter(BaseExporter):
    """
    This exporter will save data to your local filesystem. It currently provides
    exports to JSON, CSV or HTML tables. Take a look at the following exporters
    and their implementation to understand its usage.
    """
    extension = ''

    def convert(self):
        """
        Converts `self.data` to output format specified by `FileExporter.extension`.
        > Must return converted data as `string`
        """
        raise NotImplementedError()

    def export(self):
        """ Writes data to file """
        data = self.convert()
        timestamp = datetime.now().strftime('%Y-%m-%d-%H:%M')
        path = os.path.join(self.settings.export_to, f'{self.domain}_{timestamp}.{self.extension}')
        try:
            os.makedirs(self.settings.export_to, exist_ok=True)
            with open(path, 'w') as file:
                file.write(data)
            LOG.info(f'Exported data as {self.extension.upper()} to: {path} [{self.domain}]')
        except Exception as e:
            LOG.error(f'Error during export: {e} [{self.domain}]')


class JSONExporter(FileExporter):
    """ Exports to JSON files """
    extension = 'json'

    def convert(self):
        data = json.dumps(self.data)
        return data


class CSVExporter(FileExporter):
    """ Exports to CSV files """
    extension = 'csv'

    def convert(self):
        headers = ';'.join([key.upper() for key in self.data[0].keys()])
        rows = '\n'.join([';'.join([str(val) for val in obj.values()]) for obj in self.data])
        table = '\n'.join([headers, rows])
        return table


class HTMLExporter(FileExporter):
    """ Exports data as <table> to HTML files """
    extension = 'html'

    def convert(self):
        styles = 'width: 100%; border: 1px solid grey; text-align: center'
        headers = ''.join([f'<th>{key.upper()}</th>' for key in self.data[0].keys()])
        rows = ''.join([f"<tr>{''.join([f'<td>{val}</td>' for val in obj.values()])}</tr>" for obj in self.data])
        table = f'<!DOCTYPE html><html><body><table style="{styles}"><tr>{headers}</tr><tbody>{rows}</tbody></table><body></html>'
        return table



