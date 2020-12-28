from urllib.parse import urlparse, urlencode, parse_qsl

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]

UAFactory = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)


def get_headers(language: str):
    """ Constructs request headers with given language header and random user-agent """
    return {
        'User-Agent': UAFactory.get_random_user_agent(),
        'Accept-Language': language,
        'Accept-Encoding': 'deflate, gzip;q=1.0, *;q=0.5',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }


# Mostly copied from scrapy.contrib.linkextractor
IGNORED_EXTENSIONS = [
    # images
    'mng', 'pct', 'bmp', 'gif', 'jpg', 'jpeg', 'png', 'pst', 'psp', 'tif',
    'tiff', 'ai', 'drw', 'dxf', 'eps', 'ps', 'svg',

    # audio
    'mp3', 'wma', 'ogg', 'wav', 'ra', 'aac', 'mid', 'au', 'aiff',

    # video
    '3gp', 'asf', 'asx', 'avi', 'mov', 'mp4', 'mpg', 'qt', 'rm', 'swf', 'wmv', 'm4a',

    # other
    'css', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'dmg', 'exe', 'bin', 'rss', 'zip', 'rar',
]


def fingerprint(url: str):
    """ Fingerprint function for page identification """
    url_obj = urlparse(url)
    path_stripped = "".join([p for p in url_obj.path.split("/")])
    fp = hash(f'{url_obj.scheme}://{url_obj.netloc}{path_stripped}')
    return fp


def urldiff(urls1: [str], urls2: [str]):
    """ Finds the difference between two set of URLs [WIP] """
    return list(set(urls1).difference(set(urls2)))


def norm_url(url: str):
    parsed = urlparse(url)
    # Sort query parameters if there are any
    query = '?' + urlencode(sorted(parse_qsl(parsed.query))) if parsed.query else ''
    # Drop fragments and rebuild URL
    return f'{parsed.scheme}://{parsed.netloc}{parsed.path}{query}'


def get_first_or_list(from_result):
    """ Return the first element, if there's only one, otherwise returns the whole list """
    return from_result[0] if (type(from_result) == list and len(from_result) == 1) else from_result


def remove_multi_whitespace(string_or_list):
    """ Cleans redundant whitespace from extracted data """
    if type(string_or_list) == str:
        return ' '.join(string_or_list.split())
    return list(map(lambda x: ' '.join(x.split()), string_or_list))
