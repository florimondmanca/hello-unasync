def is_async_mode() -> bool:
    """Tests if we're in the async part of the code."""

    async def f() -> None:
        return None

    coro = f()
    if coro is None:
        return False

    coro.close()  # Prevent unawaited coroutine warning.
    return True
