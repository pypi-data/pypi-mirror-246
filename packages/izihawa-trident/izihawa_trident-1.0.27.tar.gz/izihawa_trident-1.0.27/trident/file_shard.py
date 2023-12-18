import asyncio
import glob
import logging
import os
import urllib.parse

import aiofiles.os

from .key_cache import KeyCache


class FileShard:
    def __init__(self, name: str, path: str):
        self._name = name
        self._path = path
        self._key_cache = KeyCache()
        asyncio.get_event_loop().run_in_executor(None, self._fill_key_cache)

    def _fill_key_cache(self):
        for infile in glob.iglob(os.path.join(self._path, '*.*')):
            key = os.path.basename(infile)
            self._key_cache.add(key)
            if key.startswith('~') or key.endswith('~'):
                logging.getLogger('warning').warning({'action': 'found_temporary_file', 'path': infile})

    @property
    def name(self) -> str:
        return self._name

    @property
    def path(self) -> str:
        return self._path

    async def read(self, key: str) -> bytes:
        file_path = os.path.join(self.path, urllib.parse.quote(key))
        if key in self._key_cache or os.path.exists(file_path):
            self._key_cache.add(key)
            async with aiofiles.open(file_path, "rb") as f:
                return await f.read()

    async def exists(self, key: str) -> bool:
        file_path = os.path.join(self.path, urllib.parse.quote(key))
        if key in self._key_cache or os.path.exists(file_path):
            self._key_cache.add(key)
            return True
        return False

    async def write(self, key: str, value: bytes):
        file_path = os.path.join(self.path, urllib.parse.quote(key))
        tmp_file_path = os.path.join(self.path, '~' + urllib.parse.quote(key))
        async with aiofiles.open(tmp_file_path, "wb") as f:
            await f.write(value)
            await f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_file_path, file_path)
        self._key_cache.add(key)
