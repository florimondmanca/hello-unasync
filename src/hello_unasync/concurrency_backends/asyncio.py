import asyncio

from .._async.concurrency_backends.base import ConcurrencyBackend


class AsyncioBackend(ConcurrencyBackend):
    async def sleep(self, seconds: float) -> None:
        await asyncio.sleep(seconds)
