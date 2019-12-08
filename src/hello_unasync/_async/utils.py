def is_async_mode() -> bool:  # pragma: no cover
    """
    Return True if we are in the '_async' part of the code,
    or False if we are in the '_sync' part of the code.
    """

    async def f() -> None:
        return None

    coro = f()
    if coro is None:  # `unasync` stripped 'async' from the definition of 'f()'.
        return False

    coro.close()  # Prevent unawaited coroutine warning.
    return True
