class UnknownFtpProtocolException(Exception):
    def __init__(self, protocol: str) -> None:
        super().__init__("Unknown ftp protocol: " + protocol)
