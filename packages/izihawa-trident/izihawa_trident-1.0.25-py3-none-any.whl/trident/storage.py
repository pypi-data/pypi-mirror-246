import asyncio
import random

import confuse
from uhashring import HashRing

from .file_shard import FileShard


class Storage:
    def __init__(self, config: confuse.Configuration):
        nodes = {
            node_config["name"]: {
                "instance": FileShard(node_config["name"], node_config["path"]),
                "weight": node_config["weight"],
            }
            for node_config in config["file_shards"].get(list)
        }
        self._config = config
        self._hash_ring = HashRing(nodes)

    async def store(
        self,
        key: str,
        value: bytes,
        dry_run: bool = False,
    ) -> dict:
        writing_file_shards = []

        for point in self._hash_ring.range(
            key, self._config["replicas"].get(int), unique=True
        ):
            file_shard: FileShard = point["instance"]
            writing_file_shards.append(file_shard)

        if not dry_run:
            await asyncio.gather(
                *[
                    writing_file_shard.write(key, value)
                    for writing_file_shard in writing_file_shards
                ]
            )

        return {
            "file_shards": [
                writing_file_shard.name for writing_file_shard in writing_file_shards
            ]
        }

    async def read(self, key: str) -> bytes:
        points = list(
            self._hash_ring.range(key, self._config["replicas"].get(int), unique=True)
        )
        random.shuffle(points)
        for point in points:
            file_shard: FileShard = point["instance"]
            file = await file_shard.read(key)
            return file

    async def exists(self, key: str) -> str:
        for point in self._hash_ring.range(
            key, self._config["replicas"].get(int), unique=True
        ):
            file_shard: FileShard = point["instance"]
            if await file_shard.exists(key):
                return file_shard.name
