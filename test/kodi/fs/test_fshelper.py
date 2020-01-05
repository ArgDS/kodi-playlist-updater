from typing import Final

import unittest2

from kodi.fs.FileSystemHelper import FileSystemHelper
from test.TestUtils import resolve_path_test_sources


class FileSystemHelperTest(unittest2.TestCase):
    PATH_TEST_SOURCE: Final = resolve_path_test_sources() + "/videos"

    def test_read(self):
        items = FileSystemHelper.read_file_items_from_dir(self.PATH_TEST_SOURCE)
        self.assertEqual(2, len(items))
        for item in items:
            str_dt = item.update_date.strftime("%m/%d/%Y, %H:%M:%S")
            print("path: " + item.path + "; update date: " + str_dt + "; size: " + str(item.size) + " bytes")
