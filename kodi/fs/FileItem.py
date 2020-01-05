import os.path
from datetime import datetime

from kodi.DateTimeUtils import DateTimeUtils


class FileItem:
    def __init__(self, path: str, update_date: datetime, size: int):
        self.path = path
        self.update_date = update_date
        self.size = size
        self.name = os.path.basename(path)

    def __str__(self):
        return "Name: \"%s\", Path: \"%s\", size: %d bytes, modification date: %s" \
               % (self.name, self.path, self.size, DateTimeUtils.datetime_to_str(self.update_date))
