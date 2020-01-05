import logging
import os.path
from typing import List

from kodi.AppConfiguration import AppConfiguration
from kodi.exception.WrongTypePlaylistException import WrongTypePlaylistException
from kodi.fs.FileItem import FileItem
from kodi.fs.FileItemUtils import FileItemsResponse
from kodi.playlist.Playlist import Playlist
from kodi.playlist.PlaylistItem import PlaylistItem
from kodi.playlist.playlist_constant import TITLE_TYPE, TITLE_ITEM

logger = logging.getLogger(__name__)


class PlaylistUtils:
    @classmethod
    def load_from_file(cls, path: str) -> Playlist:
        a_path = os.path.abspath(path)
        if not os.path.exists(a_path):
            logger.error("Does not find playlist file: " + a_path)
            return Playlist(a_path, list())
        playlist_items = list()
        with open(a_path, "r") as playlist_file:
            line = playlist_file.readline()
            if not line:
                logger.warning("Found empty file of playlist: " + a_path)
                return Playlist(a_path, list())
            if line.rstrip() != TITLE_TYPE:
                raise WrongTypePlaylistException(path)
            cnt = 0
            line = playlist_file.readline()
            while line:
                if line.startswith(TITLE_ITEM):
                    line = playlist_file.readline()
                    playlist_items.append(PlaylistItem(line))
                    cnt += 1
                line = playlist_file.readline()
            if cnt == 0:
                logger.info("Playlist is empty")
            else:
                logger.info("Playlist contains " + str(cnt) + " items")

        return Playlist(a_path, playlist_items)

    @staticmethod
    def save_to_file(playlist: Playlist) -> str:
        with open(playlist.path, "w") as dest_playlist:
            dest_playlist.write(playlist.to_playlist())
        return playlist.path

    @staticmethod
    def create_actual_playlist(app_config: AppConfiguration, delta: FileItemsResponse,
                               store_items: List[FileItem],
                               current_playlist: Playlist) -> Playlist:
        new_playlist = Playlist(current_playlist.path, list())
        current_playlist_items = current_playlist.items.copy()
        sync_playlist_items = list()
        for store_item in store_items:
            existed = False
            for current_playlist_item in current_playlist_items:
                if store_item.name == current_playlist_item.name:
                    existed = True
                    sync_playlist_items.append(current_playlist_item)
                    continue
            if not existed:
                sync_playlist_items.append(PlaylistItem(store_item.path))

        for new_file_item in delta.new_items:
            new_playlist.items.append(PlaylistItem(os.path.join(app_config.directories.store, new_file_item.name)))

        cleaned_playlist_items = list()
        for playlist_item in sync_playlist_items:
            deleted = False
            for deleted_file_item in delta.deleted_items:
                if playlist_item.name == deleted_file_item.name:
                    deleted = True
            if not deleted:
                cleaned_playlist_items.append(playlist_item)

        for updated_file_item in delta.updated_items:
            existed = False
            for new_playlist_item in cleaned_playlist_items:
                if new_playlist_item.name == updated_file_item:
                    existed = True
            if not existed:
                cleaned_playlist_items.append(updated_file_item)

        new_playlist.items += cleaned_playlist_items
        return new_playlist
