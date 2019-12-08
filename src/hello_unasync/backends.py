import typing

from ._async.concurrency_backends.base import ConcurrencyBackend


class _Backend:
    """
    Specifies the desired backend and any arguments passed to its constructor.
    """

    def __init__(self, name: str, **kwargs: typing.Any) -> None:
        self.name = name
        self.kwargs = kwargs

    def __eq__(self, other: typing.Any) -> bool:
        if not isinstance(other, _Backend):
            return False
        return self.name == other.name and self.kwargs == other.kwargs


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


def normalize_backend(name: str = "auto", *, async_mode: bool) -> _Backend:
    if name == "auto":
        if not async_mode:
            backend = _Backend(name="sync")
        else:
            import sniffio

            async_library = sniffio.current_async_library()
            assert async_library == "asyncio"
            backend = _Backend(name=async_library)
    elif not isinstance(backend, _Backend):
        backend = _Backend(name=name)

    loaders_by_name = _get_backend_loaders()

    if backend.name not in loaders_by_name:
        raise ValueError("Unknown backend specifier: {backend.name!r}")

    loader = loaders_by_name[backend.name]

    if async_mode and not loader.is_async:
        raise ValueError(f"Backend {loader.name!r} needs to be run in sync mode")

    if not async_mode and loader.is_async:
        raise ValueError(f"Backend {loader.name!r} needs to be run in async mode")

    return backend


def load_backend(backend: _Backend) -> ConcurrencyBackend:
    loaders_by_name = _get_backend_loaders()
    loader = loaders_by_name[backend.name]
    return loader()
