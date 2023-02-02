
from __future__ import annotations
from py7zr import SevenZipFile
from pathlib import Path
from typing import Union
from io import BytesIO


class PackEncryptor:
    
    def __init__(self):
        self.__archive:SevenZipFile = None
        self.__archive_bio:BytesIO = BytesIO(b'')
        self.__head_length:int = -1
        self.__tail_length:int = -1
    
    def __del__(self):
        self.__close()
    
    
    # interfaces
    def create_archive(self, head_length:int, tail_length:int, password:str) -> PackEncryptor:
        "create a new archive, old archive will lost"
        self.__close()
        self.__head_length = head_length
        self.__tail_length = tail_length
        self.__archive_bio = BytesIO(b'')
        self.__archive = SevenZipFile(self.__archive_bio, mode='w', password=password)
        self.__archive.set_encrypted_header(True)
        return self
    
    def save_clear(self) -> tuple:
        """
        save current archive and clear current archive content
        Returns:
            tuple( head: bytes, middle: bytes, tail: bytes )
        """
        self.__archive.close()
        raw = self.__archive_bio.getvalue()
        head = raw[:self.__head_length]
        middle = raw[self.__head_length:-1*self.__tail_length]
        tail = raw[-1*self.__tail_length:]
        self.__archive_bio.close()
        self.__archive = None
        self.__archive_bio = None
        return (head, middle, tail)
    
    def add_file(self, filepath:Union[str,Path]) -> PackEncryptor:
        filepath = Path(filepath)
        if filepath.exists() == False:
            raise ValueError(f'File not found: {filepath}')
        self.__archive.write(file=filepath, arcname=filepath.name)
        return self
    
    def add_file_list(self, filelist:list) -> PackEncryptor:
        for filepath in filelist:
            self.add_file(filepath)
        return self
    
    
    # private helper functions
    def __close(self):
        if self.__archive:
            self.__archive.close()
        if self.__archive_bio:
            self.__archive_bio.close()
    
