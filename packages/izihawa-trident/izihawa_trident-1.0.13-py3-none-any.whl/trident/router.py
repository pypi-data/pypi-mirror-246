import asyncio
import random

from fastapi import Depends, APIRouter, HTTPException
from starlette.requests import Request

from .configs import config
from .file_shard import FileShard
from .lifespan import TridentFastAPIRequest

router = APIRouter()


async def parse_body(request: Request):
    data: bytes = await request.body()
    return data


@router.put("/kv/{key}")
async def store(
    request: TridentFastAPIRequest,
    key: str,
    value: bytes = Depends(parse_body),
    dry_run: bool = False,
):
    writing_file_shards = []

    for point in request.app.state.hash_ring.range(
        key, config["replicas"].get(int), unique=True
    ):
        file_shard: FileShard = point["instance"]
        writing_file_shards.append(file_shard)

    if not dry_run:
        await asyncio.gather(
            *[
                writing_file_shard.write_file(key, value)
                for writing_file_shard in writing_file_shards
            ]
        )

    return {
        "file_shards": [
            writing_file_shard.name for writing_file_shard in writing_file_shards
        ]
    }


@router.get("/kv/{key}")
async def read(request: TridentFastAPIRequest, key: str) -> bytes:
    points = list(
        request.app.state.hash_ring.range(key, config["replicas"].get(int), unique=True)
    )
    random.shuffle(points)
    for point in points:
        file_shard: FileShard = point["instance"]
        file = await file_shard.read_file(key)
        if file:
            return file
    raise HTTPException(status_code=404, detail="not_found")
