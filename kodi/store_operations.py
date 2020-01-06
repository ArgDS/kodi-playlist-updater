import logging
from os import path as pth, mkdir, rename
from typing import List

from kodi.AppConfiguration import AppConfiguration
from kodi.DateTimeUtils import DateTimeUtils
from kodi.fs.FileItem import FileItem
from kodi.fs.FileItemUtils import FileItemsResponse
from kodi.ftp.FtpService import FtpService

logger = logging.getLogger(__package__)


def download_files_to_buffer_store(delta: FileItemsResponse, app_config: AppConfiguration,
                                   ftp_service: FtpService) -> List[FileItem]:
    logger.info("Download files to buffer store \"%s\"" % app_config.directories.store_buffer)
    if not pth.exists(app_config.directories.store_buffer):
        logger.info("Create buffer store by path \"%s\"" % app_config.directories.store_buffer)
        mkdir(app_config.directories.store_buffer)
    downloaded_files = list()
    for new_item in delta.new_items + delta.updated_items:
        store_buffer_file_path = pth.join(app_config.directories.store_buffer, new_item.name)
        downloaded_files.append(ftp_service.download_file(new_item.path, store_buffer_file_path))
    return downloaded_files


def archive_changed_files(delta: FileItemsResponse, app_config: AppConfiguration) -> List[str]:
    files_for_archiving = delta.updated_items + delta.deleted_items
    if not files_for_archiving:
        logger.info("Found nothing for archiving")
        return list()
    archived_files = list()
    archive_path = app_config.directories.archive
    if not pth.exists(archive_path):
        logger.info("Create parent archive directory \"%s\"" % archive_path)
        mkdir(archive_path)
    new_archive_dir = pth.join(archive_path, DateTimeUtils.generate_dir_name())
    if not pth.exists(new_archive_dir):
        logger.info("Create child archive directory \"%s\"" % new_archive_dir)
        mkdir(new_archive_dir)
    for archive_file_item in files_for_archiving:
        store_file_path = pth.join(app_config.directories.store, archive_file_item.name)
        archive_file_path = pth.join(new_archive_dir, archive_file_item.name)
        rename(store_file_path, archive_file_path)
        logger.info("File with \"%s\" move to archive \"%s\"" % (archive_file_item.name, new_archive_dir))
        archived_files.append(archive_file_item.name)
    return archived_files


def move_files_to_store(download_files: List[FileItem], app_config: AppConfiguration):
    for download_file in download_files:
        store_file_path = pth.join(app_config.directories.store, download_file.name)
        rename(download_file.path, store_file_path)
        logger.info("File moved from buffer store to original store \"%s\"" % download_file.name)
