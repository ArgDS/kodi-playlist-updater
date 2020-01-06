import logging
import os.path

from kodi.AppConfiguration import load_configuration
from kodi.fs.FileItemUtils import FileItemUtils
from kodi.fs.FileSystemHelper import FileSystemHelper
from kodi.ftp.FtpService import FtpService
from kodi.player.PlayerService import PlayerService
from kodi.playlist.PlaylistUtils import PlaylistUtils
from kodi.print_operations import print_delta
from kodi.store_operations import download_files_to_buffer_store, archive_changed_files, move_files_to_store

logger = logging.getLogger(__name__)


def run(path):
    logger.info("Start application")
    app_config = load_configuration(path)
    player_service = PlayerService(app_config.kodi)
    ftp_service = FtpService(app_config.ftp)
    ftp_files = ftp_service.read_file_items(app_config.directories.ftp_source)
    store_files = FileSystemHelper.read_file_items_from_dir(app_config.directories.store)
    delta_file_items = FileItemUtils.detect_new_files_on_ftp(store_files, ftp_files)
    if not delta_file_items.is_empty():
        print_delta(delta_file_items)
        current_playlist = PlaylistUtils.load_from_file(app_config.playlist.path)
        new_playlist = PlaylistUtils.create_actual_playlist(app_config, delta_file_items, store_files, current_playlist)
        downloaded_files = download_files_to_buffer_store(delta_file_items, app_config, ftp_service)
        player_service.pause()
        player_service.clean_current_playlist()
        archive_changed_files(delta_file_items, app_config)
        move_files_to_store(downloaded_files, app_config)
        updated_playlist_path = PlaylistUtils.save_to_file(new_playlist)
        logger.info("Playlist saved by path \"%s\"" % updated_playlist_path)
        player_service.add_playlist_by_name(os.path.basename(app_config.playlist.path))
        player_service.open_playlist()
    else:
        logger.info("Does not find anything")
    ftp_service.close()


def init(path):
    logger.info("Start application for initialize playlist")
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
