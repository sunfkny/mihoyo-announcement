import httpx
from aiocache import Cache, cached
from loguru import logger


@cached(ttl=60, cache=Cache.MEMORY)
async def request_async(url: str, params: dict | None = None) -> dict:
    async with httpx.AsyncClient() as client:
        logger.info(f"Requesting {url}")
        response = await client.get(url, params=params)
        response.raise_for_status()
        response_data: dict = response.json()
        retcode = response_data.get("retcode")
        if retcode != 0:
            raise ValueError(response_data.get("message") or response.text)
        return response_data
