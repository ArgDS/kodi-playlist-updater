import logging
from typing import List

from kodi.fs.FileItem import FileItem
from kodi.fs.FileItemUtils import FileItemsResponse

logger = logging.getLogger(__package__)


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
