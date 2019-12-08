import time

from .._sync.concurrency_backends.base import ConcurrencyBackend


class SyncBackend(ConcurrencyBackend):
    def sleep(self, seconds: float) -> None:
        time.sleep(seconds)
