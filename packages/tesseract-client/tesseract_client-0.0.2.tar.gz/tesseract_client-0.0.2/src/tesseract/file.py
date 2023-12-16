import os
import hashlib
from typing import TextIO
from loguru import logger

from tesseract.chunk import Chunk, ChunkAction


class File:
    """ Represents a file on the client machine. """
    def __init__(self, file_path: str, hash: str):
        self.file_path = file_path
        self.hash = hash
        logger.info(f"Initialized File object for {file_path}")

    def split_into_chunks(
        self,
        fd: TextIO,
        chunk_size: int
    ) -> list[tuple[Chunk, bytes]]:
        """
        Returns a list of Chunk objects along with their data
        for the given file.
        """
        chunks = []
        chunk_num = 1
        while True:
            data = fd.read(chunk_size)
            if not data:
                break

            chunk_hash = hashlib.sha256(data).hexdigest()
            chunk = Chunk(
                file_path=self.file_path,
                order=chunk_num,
                hash=chunk_hash
            )
            chunks.append((chunk, data))
            chunk_num += 1
        logger.info(f"Split {self.file_path} into {len(chunks)} chunks")
        return chunks

    def get_updated_chunks(
        self,
        fd: TextIO,
        indexed_chunks: list[Chunk],
        chunk_size: int
    ) -> list[tuple[Chunk, bytes], ChunkAction]:
        """
        Returns a list of chunks that have been updated since the last time
        the file was indexed.
        """
        updated_chunks = []
        chunks = self.split_into_chunks(fd, chunk_size)
        if len(chunks) > len(indexed_chunks):
            # File has been appended to
            for chunk in chunks[len(indexed_chunks):]:
                updated_chunks.append((chunk, ChunkAction.CREATE))
        elif len(chunks) < len(indexed_chunks):
            # File has been truncated
            for chunk in indexed_chunks[len(chunks):]:
                updated_chunks.append(((chunk, None), ChunkAction.DELETE))
        if len(indexed_chunks) > 0:
            for i, chunk in enumerate(chunks[:len(indexed_chunks)]):
                if chunk[0].hash != indexed_chunks[i].hash:
                    updated_chunks.append((chunk, ChunkAction.UPDATE))
        logger.info(f"Found {len(updated_chunks)} updated chunks")
        return updated_chunks

    @staticmethod
    def get_relative_path(file_path, root_folder) -> str:
        """Returns relative file path to the root folder."""
        relative_path = os.path.relpath(file_path, root_folder)
        logger.debug(f"Relative path for {file_path} is {relative_path}")
        return relative_path

    @staticmethod
    def get_file_hash(file_path: str) -> str:
        """Returns the hash of a file."""
        with open(file_path, 'rb') as file:
            file_hash = hashlib.sha256(file.read()).hexdigest()
        logger.debug(f"File hash for {file_path} is {file_hash}")
        return file_hash

    @classmethod
    def from_local_file(cls, file_path: str, root_folder: str):
        """Returns a File object from an absolute file path."""
        logger.info(f"Created File object from local file {file_path}")
        return cls(
            cls.get_relative_path(file_path, root_folder),
            cls.get_file_hash(file_path)
        )
