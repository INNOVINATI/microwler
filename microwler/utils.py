from urllib.parse import urlparse

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]

UAFactory = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)


def get_headers(language: str):
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
    url_obj = urlparse(url)
    path_stripped = "".join([p for p in url_obj.path.split("/")])
    fp = hash(f'{url_obj.scheme}://{url_obj.netloc}{path_stripped}')
    return fp


def urldiff(urls1: [str], urls2: [str]):
    return list(set(urls1).difference(set(urls2)))
