import logging
from typing import List

from kodi.playlist.PlaylistItem import PlaylistItem
from kodi.playlist.playlist_constant import TITLE_TYPE

logger = logging.getLogger("__name__")


class Playlist:
    def __init__(self, path: str, items: List[PlaylistItem]):
        self.path = path
        self.items = items

    def add(self, item_path: str) -> None:
        self.items.append(PlaylistItem(item_path))

    def to_playlist(self) -> str:
        items = ""
        for item in self.items:
            items += "\n" + item.to_item()
        return TITLE_TYPE + items
