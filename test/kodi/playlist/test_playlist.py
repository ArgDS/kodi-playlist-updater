import os.path
from typing import Final

import unittest2

from kodi.exception.WrongTypePlaylistException import WrongTypePlaylistException
from kodi.playlist.Playlist import Playlist
from kodi.playlist.PlaylistUtils import PlaylistUtils
from test.TestUtils import resolve_path_test_sources


class PlaylistTest(unittest2.TestCase):
    PATH_TEST_SOURCES: Final = resolve_path_test_sources() + "/playlists"

    def test_not_exist_file(self):
        path = self.PATH_TEST_SOURCES + "/not_exists.m3u"
        playlist = PlaylistUtils.load_from_file(path)
        self.assertEqual(0, len(playlist.items))

    def test_empty_file(self):
        path = self.PATH_TEST_SOURCES + "/empty_file.m3u"
        playlist = PlaylistUtils.load_from_file(path)
        self.assertEqual(0, len(playlist.items))

    def test_bad_playlist(self):
        path = self.PATH_TEST_SOURCES + "/bad_playlist.m3u"
        try:
            PlaylistUtils.load_from_file(path)
            self.fail("It can not finished")
        except WrongTypePlaylistException:
            print("Test finished success")

    def test_empty_playlist(self):
        path = self.PATH_TEST_SOURCES + "/empty_playlist.m3u"
        try:
            playlist = PlaylistUtils.load_from_file(path)
            self.assertEqual(0, len(playlist.items))
        except WrongTypePlaylistException:
            print("Test finished success")

    def test_full_playlist(self):
        path = self.PATH_TEST_SOURCES + "/full_playlist.m3u"
        playlist = PlaylistUtils.load_from_file(path)
        self.assertEqual(3, len(playlist.items))

    def test_save_playlist(self):
        path_new_playlist = self.PATH_TEST_SOURCES + "/new_playlist.m3u"
        self.remove_file(path_new_playlist)
        new_playlist = Playlist(path_new_playlist, list())
        new_playlist_item_file = "/data/video/v1.mp3"
        new_playlist.add(new_playlist_item_file)
        path_saved_playlist = PlaylistUtils.save_to_file(new_playlist)
        saved_playlist = PlaylistUtils.load_from_file(path_saved_playlist)
        self.assertEqual(os.path.abspath(path_new_playlist), saved_playlist.path)
        self.assertEqual(1, len(saved_playlist.items))
        self.assertEqual(new_playlist_item_file, saved_playlist.items[0].path)
        self.remove_file(path_new_playlist)

    @staticmethod
    def remove_file(path: str):
        if os.path.exists(path):
            os.remove(path)
