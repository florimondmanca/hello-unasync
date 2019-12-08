class ConcurrencyBackend:
    """
    Base class for concurrency backends.

    Needs to be in this directory ('_async/...') so that a sync equivalent is created
    by `unasync` in the '_sync/...' sub-package at build time.
    """

    async def sleep(self, seconds: float) -> None:
        raise NotImplementedError  # pragma: no cover
