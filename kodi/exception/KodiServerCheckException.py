class KodiServerCheckException(Exception):
    def __init__(self):
        super().__init__("Cannot check kodi server")
