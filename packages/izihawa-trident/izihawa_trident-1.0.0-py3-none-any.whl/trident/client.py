from aiobaseclient import BaseClient
from aiobaseclient.exceptions import ExternalServiceError


class TridentClient(BaseClient):
    async def response_processor(self, response):
        text = await response.text()
        if response.status == 404:
            return None
        elif response.status != 200:
            if hasattr(response, 'request'):
                raise ExternalServiceError(response.request.url, response.status, text)
            else:
                raise ExternalServiceError(None, response.status, text)
        return text
