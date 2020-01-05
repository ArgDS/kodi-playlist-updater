from kodi.AppConfiguration import FtpConfiguration


class CannotConnectToFtpException(Exception):
    def __init__(self, ftpConfig: FtpConfiguration):
        super().__init__("Can not connect to ftp server " + ftpConfig.host + ":" + ftpConfig.port +
                         " by protocol \"" + ftpConfig.protocol + "\" with user \"" + ftpConfig.username + "\"")
