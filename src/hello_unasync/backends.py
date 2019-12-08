import typing

from ._async.concurrency_backends.base import ConcurrencyBackend


class _Loader:
    def __init__(
        self,
        name: str,
        loader: typing.Callable[[], ConcurrencyBackend],
        *,
        is_async: bool,
    ) -> None:
        self.name = name
        self.loader = loader
        self.is_async = is_async

    def __call__(self) -> ConcurrencyBackend:
        return self.loader()


def _load_sync_backend() -> ConcurrencyBackend:
    from .concurrency_backends.sync import SyncBackend

    return SyncBackend()


def _load_asyncio_backend() -> ConcurrencyBackend:
    from .concurrency_backends.asyncio import AsyncioBackend

    return AsyncioBackend()


def _get_backend_loaders() -> typing.Dict[str, _Loader]:
    loaders = [
        _Loader(name="sync", loader=_load_sync_backend, is_async=False),
        _Loader(name="asyncio", loader=_load_asyncio_backend, is_async=True),
    ]
    return {loader.name: loader for loader in loaders}


def normalize_backend(name: str = "auto", *, async_mode: bool) -> str:
    if name == "auto":
        if not async_mode:
            backend = "sync"
        else:
            import sniffio

            async_library = sniffio.current_async_library()
            assert async_library == "asyncio"
            backend = async_library
    else:  # pragma: no cover
        backend = name

    loaders_by_name = _get_backend_loaders()
    assert backend in loaders_by_name, "Unknown backend specifier: {backend!r}"
    loader = loaders_by_name[backend]

    if async_mode and not loader.is_async:  # pragma: no cover
        raise ValueError(f"Backend {loader.name!r} needs to be run in sync mode")

    if not async_mode and loader.is_async:  # pragma: no cover
        raise ValueError(f"Backend {loader.name!r} needs to be run in async mode")

    return backend


def load_backend(backend: str) -> ConcurrencyBackend:
    loaders_by_name = _get_backend_loaders()
    loader = loaders_by_name[backend]
    return loader()
