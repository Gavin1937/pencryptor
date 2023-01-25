
from py7zr import SevenZipFile
from pathlib import Path
from typing import Union
import sqlite3


class PackEncryptor:
    
    def __init__(self):
        self.__archive:SevenZipFile = None
        self.__connector:sqlite3.Connection = None
        # self.__init_archive("", "")
        pass
    
    def __del__(self):
        self.close()
    
    # interfaces
    def close(self):
        if self.__archive:
            self.__archive.close()
        if self.__connector:
            self.__connector.close()
    
    def write_dir(self, dirpath:Union[str,Path]):
        self.__archive.writeall(dirpath)
    
    
    # private helper functions
    def __init_archive(self, path:Union[str,Path], password:str):
        self.__archive:SevenZipFile = SevenZipFile(path, mode='w', password=password)
        self.__archive.set_encrypted_header(True)
    
