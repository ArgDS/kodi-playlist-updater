class KodiCannotGetActivePlayerException(Exception):
    def __init__(self):
        super().__init__("Cannot get active player in kodi")
