from ..backends import load_backend, normalize_backend
from .utils import is_async_mode

_ASYNC_MODE = is_async_mode()


class Manager:
    def __init__(self, message: str, delay: float, backend: str = "auto") -> None:
        self.message = message
        self.delay = delay
        self._backend = load_backend(normalize_backend(backend, async_mode=_ASYNC_MODE))

    async def run(self) -> str:
        await self._backend.sleep(self.delay)
        return self.message
