
from __future__ import annotations
from py7zr import SevenZipFile
from copy import deepcopy
from pathlib import Path
from typing import Union
from io import BytesIO

__all__ = ['PackEncryptor']


class PackEncryptor:
    """
    Pack files and encrypt them with 7zip
    
    Remove file structure and only care about files
    
    Compress all files into 7zip archive with encryption
    
    Then, split the archive into 3 parts:
    
    1. header part
    2. content part in the middle
    3. tail part
    
    the (2.) content part will take up majority of the size
    
    and it is hard to decrypt & extract due to missing file header & tail
    """
    
    def __init__(self):
        self.__archive:SevenZipFile = None
        self.__archive_bio:BytesIO = None
        self.__write_mode:str = None
        self.__file_list:list = None
        self.__head_length:int = -1
        self.__tail_length:int = -1
    
    def __del__(self):
        self.__close()
    
    
    # interfaces
    def create_archive(self, head_length:int, tail_length:int, password:str, write_mode:str='save') -> PackEncryptor:
        """
        create a new archive, old archive will be lost
        
        param:
            
            head_length  => int, length in bytes of head part of archive
            
            tail_length  => int, length in bytes of tail part of archive
            
            password     => str, password of archive
            
            write_mode   => str, mode of writing to archive. Can be either 'save' or 'add'. (default 'save')
                            
                            'save' => write on save, only write to archive when calling save_clear(). Slow save time but take less memory.
                            
                            'add'  => write on add, write to archive every time calling add_file() or add_file_list(). Quick save but take more memory.
        """
        self.__close()
        self.__head_length = head_length
        self.__tail_length = tail_length
        write_mode = write_mode.lower()
        if write_mode != 'save' and write_mode != 'add':
            raise ValueError('Invalid write_mode, it must be either "save" or "add".')
        self.__write_mode = write_mode
        self.__file_list:list = []
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
        if self.__archive is None or self.__archive_bio is None:
            raise ValueError('Fail to save an empty archive.')
        if self.__write_mode == 'save':
            for filepath in self.__file_list:
                self.__archive.write(file=filepath, arcname=filepath.name)
        self.__archive.close()
        raw = self.__archive_bio.getvalue()
        head = raw[:self.__head_length]
        middle = raw[self.__head_length:-1*self.__tail_length]
        tail = raw[-1*self.__tail_length:]
        self.__archive_bio.close()
        self.__archive = None
        self.__archive_bio = None
        return (head, middle, tail)
    
    def clear(self) -> None:
        "clear current archive content"
        self.__archive.close()
        self.__archive_bio.close()
        self.__archive = None
        self.__archive_bio = None
    
    def add_file(self, filepath:Union[str,Path]) -> PackEncryptor:
        "add a single file to current archive"
        if self.__archive is None or self.__archive_bio is None:
            raise ValueError('Archive has not initialized, please call PackEncryptor.create_archive() first.')
        filepath = Path(filepath)
        if filepath.exists() == False:
            raise ValueError(f'File not found: {filepath}')
        self.__file_list.append(filepath)
        if self.__write_mode == 'add':
            self.__archive.write(file=filepath, arcname=filepath.name)
        return self
    
    def add_file_list(self, filelist:list) -> PackEncryptor:
        "add a list of files to current archive"
        if self.__archive is None or self.__archive_bio is None:
            raise ValueError('Archive has not initialized, please call PackEncryptor.create_archive() first.')
        for filepath in filelist:
            filepath = Path(filepath)
            if filepath.exists() == False:
                raise ValueError(f'File not found: {filepath}')
            self.__file_list.append(filepath)
            if self.__write_mode == 'add':
                self.__archive.write(file=filepath, arcname=filepath.name)
        return self
    
    def list_files(self) -> list:
        "list all files in archive"
        return deepcopy(self.__file_list)
    
    
    # private helper functions
    def __close(self):
        try:
            if self.__archive:
                self.__archive.close()
            if self.__archive_bio:
                self.__archive_bio.close()
        except LookupError:
            pass
        self.__archive = None
        self.__archive_bio = None
    
