import logging
from datetime import datetime
from ftplib import FTP, FTP_TLS
from os import path as pth
from typing import List

from kodi.AppConfiguration import FtpConfiguration
from kodi.exception.CannotConnectToFtpException import CannotConnectToFtpException
from kodi.exception.UnknownFtpProtocolException import UnknownFtpProtocolException
from kodi.fs.FileItem import FileItem
from kodi.fs.FileSystemHelper import FileSystemHelper

logger = logging.getLogger(__name__)


class FtpService:

    def __init__(self, config: FtpConfiguration):
        self.config = config
        self.__connect()

    def __connect(self) -> None:
        if self.config.protocol == "FTP":
            self.ftp = FTP()
        elif self.config.protocol == "SFTP":
            self.ftp = FTP_TLS()
        else:
            raise UnknownFtpProtocolException(self.config.protocol)
        self.ftp.connect(host=self.config.host, port=self.config.port, timeout=10)
        resp: str = self.ftp.login(self.config.username, self.config.passwd)
        if resp.startswith("230"):
            logger.info("Successfully connect to FTP server")
        else:
            raise CannotConnectToFtpException(self.config)

    def read_file_items(self, path: str) -> List[FileItem]:
        files = list()
        items = list()
        self.ftp.cwd(path)
        self.ftp.dir(items.append)
        for item in items:
            name, is_file, size = self.__parse_list_line(item)
            if is_file:
                file_path = path + "/" + name
                mdt = self.ftp.sendcmd("MDTM " + file_path)
                dt = self.__parse_mdt(mdt)
                files.append(FileItem(file_path, dt, int(size)))
        return files

    def download_file(self, ftp_path: str, store_path: str) -> FileItem:
        a_store_path = pth.abspath(store_path)
        logger.info("Try download file from ftp \"%s\" to \"%s\"" % (ftp_path, a_store_path))
        try:
            self.ftp.retrbinary("RETR " + ftp_path, open(a_store_path, 'wb').write)
        except Exception as ex:
            logger.error("Cannot download file", ex)
            raise ex
        return FileSystemHelper.read_file_item(a_store_path)

    def close(self):
        self.ftp.close()
        logger.info("Close ftp connection with server")

    @staticmethod
    def __parse_list_line(line: str) -> tuple:
        items = line.split()
        is_file = True
        if items[0].startswith("d"):
            is_file = False
        size = items[4]
        name = items[8:]
        return str.join(" ", name), is_file, size

    @staticmethod
    def __parse_mdt(mdt: str) -> datetime:
        items = mdt.split()
        dt = items[1]
        year = int(dt[0:4])
        month = int(dt[4:6])
        day = int(dt[6:8])
        hour = int(dt[8:10])
        minute = int(dt[10:12])
        second = int(dt[12:14])
        return datetime(year, month, day, hour, minute, second)
