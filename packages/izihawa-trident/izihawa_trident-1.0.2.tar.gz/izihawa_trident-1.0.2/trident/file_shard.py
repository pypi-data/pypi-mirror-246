import os
import urllib.parse

import aiofiles


class FileShard:
    def __init__(self, name: str, path: str):
        self._name = name
        self._path = path

    @property
    def name(self) -> str:
        return self._name

    @property
    def path(self) -> str:
        return self._path

    async def read_file(self, key: str) -> bytes:
        file_path = os.path.join(self.path, urllib.parse.quote(key))
        if os.path.exists(file_path):
            async with aiofiles.open(file_path, 'rb') as f:
                return await f.read()

    async def write_file(self, key: str, value: bytes):
        file_path = os.path.join(self.path, urllib.parse.quote(key))
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(value)
