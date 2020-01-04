import logging
import os.path

from kodi.exception.WrongTypePlaylistException import WrongTypePlaylistException
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
