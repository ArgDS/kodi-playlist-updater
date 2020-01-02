import sys

import yaml
import os.path
import logging

logger = logging.getLogger(__name__)


class AppConfiguration:
    def __init__(self, entities: dict):
        self.ftp = FtpConfiguration(entities['ftp'])
        self.directories = DirectoriesConfiguration(entities['directories'])
        self.playlist = PlaylistConfiguration(entities['playlist'])
        self.kodi = KodiConfiguration(entities['kodi'])


class FtpConfiguration:
    def __init__(self, entities: dict):
        self.host = entities['host']
        self.port = entities['port']
        self.username = entities['username']
        self.passwd = entities['passwd']


class DirectoriesConfiguration:
    def __init__(self, entities: dict):
        self.ftp_source = entities['ftp-source']
        self.store = entities['store']
        self.archive = entities['archive']


class PlaylistConfiguration:
    def __init__(self, entities: dict):
        self.path = entities['path']
        self.remove_delay = entities['remove-delay']


class KodiConfiguration:
    def __init__(self, entities):
        self.host = entities['host']
        self.port = entities['port']
        self.protocol = entities['protocol']
        self.username = entities['username']
        self.passwd = entities['passwd']


def load_configuration(path: str) -> AppConfiguration:
    if not os.path.exists(path):
        logger.error("Configuration file does not find: " + os.path.abspath(path))
        sys.exit(1)
    with open(path, "r") as conf:
        conf_dict = yaml.safe_load(conf)
        return AppConfiguration(conf_dict)
