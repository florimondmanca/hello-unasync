class ConcurrencyBackend:
    async def sleep(self, seconds: float) -> None:
        raise NotImplementedError  # pragma: no cover
