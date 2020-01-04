class WrongTypePlaylistException(Exception):
    def __init__(self, path: str):
        super(WrongTypePlaylistException, self).__init__("Playlist have wrong type: " + path)
