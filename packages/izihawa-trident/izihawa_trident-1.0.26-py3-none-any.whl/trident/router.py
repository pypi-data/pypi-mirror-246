import mimetypes

from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

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
    return await request.app.state.storage.store(key, value, dry_run)


@router.get("/kv/{key}")
async def read(
    request: TridentFastAPIRequest,
    key: str,
) -> Response:
    data = await request.app.state.storage.read(key)
    if data:
        return Response(
            content=data,
            media_type=mimetypes.guess_type(key)[0],
            headers={}
        )
    raise HTTPException(status_code=404, detail="not_found")


@router.get("/kv/{key}/exists")
async def exists(request: TridentFastAPIRequest, key: str) -> Response:
    file_shard_name = await request.app.state.storage.exists(key)
    if file_shard_name:
        return JSONResponse(content={"exists": True, "first_file_shard": file_shard_name})
    return JSONResponse(content={"exists": False}, status_code=404)
