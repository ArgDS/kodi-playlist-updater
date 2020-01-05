import logging
from typing import List

from kodi.AppConfiguration import load_configuration, AppConfiguration
from kodi.fs.FileItem import FileItem
from kodi.fs.FileItemUtils import FileItemUtils, FileItemsResponse
from kodi.fs.FileSystemHelper import FileSystemHelper
from kodi.ftp.FtpService import FtpService

logger = logging.getLogger(__name__)


def run(path):
    logger.info("Start application")
    app_config = load_configuration(path)
    ftp_service = FtpService(app_config.ftp)
    ftp_files = ftp_service.read_file_items(app_config.directories.ftp_source)
    store_files = FileSystemHelper.read_file_items_from_dir(app_config.directories.store)
    # example_download_file(app_config, ftp_service)
    delta_file_items = FileItemUtils.detect_new_files_on_ftp(store_files, ftp_files)
    print_delta(delta_file_items)

    ftp_service.close()


def example_download_file(app_config: AppConfiguration, ftp_service: FtpService):
    download_file = "24001-Qi Fast Charger White, 10W.mp4"
    ftp_file = app_config.directories.ftp_source + "/" + download_file
    store_file = app_config.directories.store + "/" + download_file
    downloaded_file = ftp_service.download_file(ftp_file, store_file)
    logger.info(downloaded_file)


def print_delta(delta: FileItemsResponse):
    logger.info("NEW items:")
    print_file_items(delta.new_items)
    logger.info("UPDATED items:")
    print_file_items(delta.updated_items)
    logger.info("DELETED items")
    print_file_items(delta.deleted_items)


def print_file_items(items: List[FileItem]):
    for item in items:
        logger.info(item)
