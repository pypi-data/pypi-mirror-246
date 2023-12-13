from aiobaseclient import BaseClient
from aiobaseclient.exceptions import ExternalServiceError


class TridentClient(BaseClient):
    async def response_processor(self, response):
        data = await response.read()
        if response.status == 404:
            return None
        elif response.status != 200:
            if hasattr(response, 'request'):
                raise ExternalServiceError(response.request.url, response.status, data)
            else:
                raise ExternalServiceError(None, response.status, data)
        return data

    async def store(self, key: str, data: bytes):
        url = f'/kv/{key}'
        return await self.put(url, data=data)

    async def read(self, key: str) -> bytes:
        url = f'/kv/{key}'
        return await self.get(url)
