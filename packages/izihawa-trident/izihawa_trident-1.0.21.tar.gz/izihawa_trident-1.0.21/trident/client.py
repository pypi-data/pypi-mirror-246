from aiobaseclient import BaseClient
from aiobaseclient.exceptions import ExternalServiceError


class TridentClient(BaseClient):
    async def response_processor(self, response):
        if response.status == 404:
            return None
        elif response.status != 200:
            data = await response.read()
            if hasattr(response, 'request'):
                raise ExternalServiceError(response.request.url, response.status, data)
            else:
                raise ExternalServiceError(None, response.status, data)
        return response

    async def store(self, key: str, data: bytes) -> dict:
        url = f'/kv/{key}'
        response = await self.put(url, data=data)
        return await response.json()

    async def read(self, key: str) -> bytes:
        url = f'/kv/{key}'
        response = await self.get(url)
        return await response.read()

    async def exists(self, key: str) -> bool:
        url = f'/kv/{key}/exists'
        response = await self.get(url)
        response = await response.json()
        return response['exists']
