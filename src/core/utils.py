from http import HTTPStatus

import aiohttp

from src.core.settings import logger


async def make_request(host: str, port: int, path: str, params: dict = None):
    params = params or {}
    url = '{protocol}://{host}:{port}/api/v1/{path}'.format(
        protocol='http',
        host=host,
        port=port,
        path=path
    )
    async with aiohttp.ClientSession() as session:

        async with session.get(url, params=params) as response:
            code = response.status
            if code == HTTPStatus.INTERNAL_SERVER_ERROR:
                print('Service error: {0}'.format(HTTPStatus.INTERNAL_SERVER_ERROR))
                logger.info('Service error: {0}'.format(HTTPStatus.INTERNAL_SERVER_ERROR))
                return '', HTTPStatus.INTERNAL_SERVER_ERROR
            message = await response.json(content_type=None)
        return message, code
