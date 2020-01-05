import os.path

from kodi.playlist.playlist_constant import TITLE_ITEM


class PlaylistItem:
    def __init__(self, path: str):
        self.path = path
        self.name = os.path.basename(path)

    def to_item(self) -> str:
        title = TITLE_ITEM + "0," + self.name
        return "\n" + title.rstrip() + "\n" + self.path.rstrip()
