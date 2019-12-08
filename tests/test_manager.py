import contextlib
import time
import typing

import pytest

from hello_unasync import AsyncManager, SyncManager


@contextlib.contextmanager
def assert_timer(expected_duration: float) -> typing.Iterator[None]:
    start = time.time()
    try:
        yield
    finally:
        end = time.time()
        assert end - start == expected_duration


def test_sync_manager() -> None:
    manager = SyncManager("Hello, world!", delay=0.1)
    with assert_timer(pytest.approx(0.1, abs=1e-2)):
        assert manager.run() == "Hello, world!"


@pytest.mark.asyncio
async def test_async_manager() -> None:
    manager = AsyncManager("Hello, world!", delay=0.1)
    with assert_timer(pytest.approx(0.1, rel=1e-2)):
        assert await manager.run() == "Hello, world!"
