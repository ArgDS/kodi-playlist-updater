import logging
import os.path
from typing import List

from kodi.AppConfiguration import load_configuration, AppConfiguration
from kodi.DateTimeUtils import DateTimeUtils
from kodi.fs.FileItem import FileItem
from kodi.fs.FileItemUtils import FileItemUtils, FileItemsResponse
from kodi.fs.FileSystemHelper import FileSystemHelper
from kodi.ftp.FtpService import FtpService
from kodi.playlist.PlaylistUtils import PlaylistUtils

logger = logging.getLogger(__name__)


def run(path):
    logger.info("Start application")
    app_config = load_configuration(path)
    ftp_service = FtpService(app_config.ftp)
    ftp_files = ftp_service.read_file_items(app_config.directories.ftp_source)
    store_files = FileSystemHelper.read_file_items_from_dir(app_config.directories.store)
    delta_file_items = FileItemUtils.detect_new_files_on_ftp(store_files, ftp_files)
    if not delta_file_items.is_empty():
        print_delta(delta_file_items)
        current_playlist = PlaylistUtils.load_from_file(app_config.playlist.path)
        new_playlist = PlaylistUtils.create_actual_playlist(app_config, delta_file_items, store_files, current_playlist)
        downloaded_files = download_files_to_buffer_store(delta_file_items, app_config, ftp_service)
        archive_changed_files(delta_file_items, app_config)
        move_files_to_store(downloaded_files, app_config)

        updated_playlist_path = PlaylistUtils.save_to_file(new_playlist)
        logger.info("Playlist saved by path \"%s\"" % updated_playlist_path)
    else:
        logger.info("Does not find anything")
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


def download_files_to_buffer_store(delta: FileItemsResponse, app_config: AppConfiguration,
                                   ftp_service: FtpService) -> List[FileItem]:
    logger.info("Download files to buffer store \"%s\"" % app_config.directories.store_buffer)
    if not os.path.exists(app_config.directories.store_buffer):
        logger.info("Create buffer store by path \"%s\"" % app_config.directories.store_buffer)
        os.mkdir(app_config.directories.store_buffer)
    downloaded_files = list()
    for new_item in delta.new_items + delta.updated_items:
        store_buffer_file_path = os.path.join(app_config.directories.store_buffer, new_item.name)
        # ftp_file_path = app_config.directories.ftp_source + "/" + new_item.name
        downloaded_files.append(ftp_service.download_file(new_item.path, store_buffer_file_path))
    return downloaded_files


def archive_changed_files(delta: FileItemsResponse, app_config: AppConfiguration) -> List[str]:
    files_for_archiving = delta.updated_items + delta.deleted_items
    if not files_for_archiving:
        logger.info("Found nothing for archiving")
        return list()
    archived_files = list()
    archive_path = app_config.directories.archive
    if not os.path.exists(archive_path):
        logger.info("Create parent archive directory \"%s\"" % archive_path)
        os.mkdir(archive_path)
    new_archive_dir = os.path.join(archive_path, DateTimeUtils.generate_dir_name())
    if not os.path.exists(new_archive_dir):
        logger.info("Create child archive directory \"%s\"" % new_archive_dir)
        os.mkdir(new_archive_dir)
    for archive_file_item in files_for_archiving:
        store_file_path = os.path.join(app_config.directories.store, archive_file_item.name)
        archive_file_path = os.path.join(new_archive_dir, archive_file_item.name)
        os.rename(store_file_path, archive_file_path)
        logger.info("File with \"%s\" move to archive \"%s\"" % (archive_file_item.name, new_archive_dir))
        archived_files.append(archive_file_item.name)
    return archived_files


def move_files_to_store(download_files: List[FileItem], app_config: AppConfiguration):
    for download_file in download_files:
        store_file_path = os.path.join(app_config.directories.store, download_file.name)
        os.rename(download_file.path, store_file_path)
        logger.info("File moved from buffer store to original store \"%s\"" % download_file.name)
