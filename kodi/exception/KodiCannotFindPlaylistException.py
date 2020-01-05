class KodiCannotFindPlaylistException(Exception):
    def __init__(self, name: str):
        super().__init__("Cannot find playlist in kodi library \"%s\"" % name)
