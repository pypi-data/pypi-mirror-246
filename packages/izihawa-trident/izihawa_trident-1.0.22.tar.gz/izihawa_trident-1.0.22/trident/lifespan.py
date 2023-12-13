import dataclasses
from contextlib import asynccontextmanager

from fastapi import FastAPI
from izihawa_loglib import configure_logging
from starlette.requests import Request
from uhashring import HashRing

from .configs import config
from .file_shard import FileShard


@dataclasses.dataclass
class State:
    hash_ring: HashRing


class TridentFastAPI(FastAPI):
    state: State


class TridentFastAPIRequest(Request):
    app: TridentFastAPI


@asynccontextmanager
async def lifespan(app: TridentFastAPI):
    configure_logging(config.get(dict))
    nodes = {
        node_config["name"]: {
            "instance": FileShard(node_config["name"], node_config["path"]),
            "weight": node_config["weight"],
        }
        for node_config in config["file_shards"].get(list)
    }
    app.state = State(hash_ring=HashRing(nodes))
    yield
