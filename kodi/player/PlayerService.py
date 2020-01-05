import logging
from typing import List

from jsonrpcclient import id_generators
from jsonrpcclient.clients.http_client import HTTPClient
from jsonrpcclient.requests import Request

from kodi.AppConfiguration import KodiConfiguration
from kodi.exception.KodiActionException import KodiActionException
from kodi.exception.KodiCannotFindPlaylistException import KodiCannotFindPlaylistException
from kodi.exception.KodiCannotGetActivePlayerException import KodiCannotGetActivePlayerException
from kodi.exception.KodiServerCheckException import KodiServerCheckException
from kodi.player.KodiFile import KodiFile
from kodi.player.PlayerState import PlayerState

logger = logging.getLogger(__name__)


class PlayerService:
    default_data = ('playlistid', 'speed', 'shuffled', 'repeat')

    def __init__(self, config: KodiConfiguration):
        self.config = config
        self.__check_connection()
        self.__gather_data()

    def pause(self):
        player_state = self.__get_player_state(self.player_id)
        if player_state.speed == 0:
            logger.info("Player has been already paused")
            return
        response = self.client.send(
            Request('Player.PlayPause', self.player_id, 'toggle', id_generator=id_generators.random()))
        if response.data.ok:
            logger.info("Player is paused")
        else:
            raise KodiActionException('Player.PlayPause')

    def play(self):
        player_state = self.__get_player_state(self.player_id)
        if player_state.speed == 1:
            logger.info("Player has been already played")
            return
        response = self.client.send(
            Request('Player.PlayPause', self.player_id, 'toggle', id_generator=id_generators.random()))
        if response.data.ok:
            logger.info("Player is played")
        else:
            raise KodiActionException("Player.PlayPause")

    def clean_current_playlist(self):
        response = self.client.send(
            Request('Playlist.Clear', self.playlist_id, id_generator=id_generators.random()))
        if response.data.ok:
            logger.info('Current playlist has cleaned')
        else:
            raise KodiActionException('Playlist.Clean')

    def add_playlist_by_name(self, name: str):
        kodi_files = self.__get_playlist_files()
        playlist: KodiFile = None
        for kodi_file in kodi_files:
            if kodi_file.label == name:
                playlist = kodi_file
                break
        if not playlist:
            raise KodiCannotFindPlaylistException(name)
        request = dict()
        request['directory'] = playlist.file
        response = self.client.send(
            Request('Playlist.Insert', self.playlist_id, 0, request, id_generator=id_generators.random()))
        if not response.data.ok:
            raise KodiActionException('Playlist.Insert')
        logger.info("Successfully insert playlist \"%s\"" % name)

    def open_playlist(self):
        request = dict()
        request['position'] = 0
        request['playlistid'] = self.playlist_id
        response = self.client.send(Request('Player.Open', id_generator=id_generators.random(), item=request,
                                            options=dict()))
        if not response.data.ok:
            raise KodiActionException('Player.Open')
        player_state = self.__get_player_state(self.player_id)
        if player_state.speed == 0:
            logger.warning("Player has been stopped! Try to play it.")
            self.play()

    def __check_connection(self):
        url = "%s://%s:%s/jsonrpc" % (self.config.protocol, self.config.host, self.config.port)
        self.client = HTTPClient(url)
        self.client.session.auth = (self.config.username, self.config.passwd)
        response = self.client.send(Request('Application.GetProperties', list(), id_generator=id_generators.random()))
        if not response.data.ok:
            raise KodiServerCheckException()

    def __gather_data(self):
        self.player_id = self.__get_player()
        player_state = self.__get_player_state(self.player_id)
        self.playlist_id = player_state.playlist_id

    def __get_player(self) -> int:
        response = self.client.send(Request('Player.GetActivePlayers', id_generator=id_generators.random()))
        if not response.data.ok:
            raise KodiCannotGetActivePlayerException()
        return response.data.result[0]['playerid']

    def __get_player_state(self, player_id: int) -> PlayerState:
        response = self.client.send(
            Request('Player.GetProperties', player_id, self.default_data, id_generator=id_generators.random()))
        if not response.data.ok:
            raise KodiActionException('Player.GetProperties')
        raw_state = response.data.result
        return PlayerState(player_id, raw_state['playlistid'], raw_state['speed'], raw_state['shuffled'],
                           raw_state['repeat'])

    def __get_playlist_files(self) -> List[KodiFile]:
        properties = ('title', 'file', 'mimetype', 'thumbnail', 'dateadded')
        sort = dict()
        sort['method'] = 'none'
        sort['order'] = 'ascending'
        response = self.client.send(Request('Files.GetDirectory', id_generator=id_generators.random(),
                                            directory='special://profile/playlists/video', media='video',
                                            properties=properties, sort=sort))
        if not response.data.ok:
            raise KodiActionException("Files.GetDirectory")
        files = list()
        for file in response.data.result['files']:
            files.append(KodiFile(file['file'], file['filetype'], file['label'], file['mimetype'], file['thumbnail'],
                                  file['title'], file['type']))
        return files
