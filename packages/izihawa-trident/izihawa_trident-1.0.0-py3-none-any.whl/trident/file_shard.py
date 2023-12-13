import os

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

    async def write_file(self, key: str, value: bytes):
        async with aiofiles.open(os.path.join(self.path, key), "wb") as f:
            await f.write(value)
