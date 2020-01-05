from datetime import datetime
from os import scandir, DirEntry, stat_result, path, stat
from typing import List, Iterator

from kodi.fs.FileItem import FileItem


class FileSystemHelper:

    @classmethod
    def read_file_items_from_dir(cls, pth: str) -> List[FileItem]:
        a_path = path.abspath(pth)
        items = list()
        entries: Iterator[DirEntry] = scandir(a_path)
        for entry in entries:
            if entry.is_file():
                items.append(cls.__create_file_item(entry.path, entry.stat()))
        return items

    @classmethod
    def read_file_item(cls, pth: str) -> FileItem:
        a_path = path.abspath(pth)
        return cls.__create_file_item(a_path, stat(a_path))

    @staticmethod
    def __create_file_item(pth: str, info: stat_result) -> FileItem:
        update_date = datetime.utcfromtimestamp(info.st_mtime).replace(microsecond=0)
        return FileItem(pth, update_date, info.st_size)
