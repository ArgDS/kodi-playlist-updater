import logging

from kodi.AppConfiguration import load_configuration

logger = logging.getLogger(__name__)


def run(path):
    app_config = load_configuration(path)
    logger.info(app_config.__str__())
