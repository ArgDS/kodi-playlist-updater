from typing import List, Union

from kodi.fs.FileItem import FileItem


class FileItemsResponse:
    def __init__(self, new_items: List[FileItem], updated_items: List[FileItem], deleted_items: List[FileItem]):
        self.new_items = new_items
        self.updated_items = updated_items
        self.deleted_items = deleted_items


class FileItemUtils:

    @classmethod
    def detect_new_files_on_ftp(cls, store: List[FileItem], ftp: List[FileItem]) -> FileItemsResponse:
        new_items = list()
        for ftp_item in ftp:
            existed_store_item = cls.__find_in_item(ftp_item.name, store)
            if not existed_store_item:
                new_items.append(ftp_item)

        updated_items = list()
        for ftp_item in ftp:
            existed_store_item = cls.__find_in_item(ftp_item.name, store)
            if existed_store_item and (
                    ftp_item.size != existed_store_item.size or ftp_item.update_date > existed_store_item.update_date):
                updated_items.append(ftp_item)

        deleted_items = list()
        for store_item in store:
            existed_ftp_item = cls.__find_in_item(store_item.name, ftp)
            if not existed_ftp_item:
                deleted_items.append(store_item)

        return FileItemsResponse(new_items, updated_items, deleted_items)

    @staticmethod
    def __find_in_item(name: str, items: List[FileItem]) -> Union[FileItem, None]:
        for item in items:
            if item.name == name:
                return item
        return None
