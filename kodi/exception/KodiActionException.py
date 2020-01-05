class KodiActionException(Exception):
    def __init__(self, action: str):
        super().__init__("Catched error with kodi action \"%s\"" % action)
