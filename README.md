# hello-unasync

This project is a proof-of-concept of using [`unasync`](https://unasync.readthedocs.io/en/latest/) in the context of a modern Python package.

The goal is to figure out how to support sync from async via code generation, while having the following:

- Development workflow: automating code generation to make sure the `_sync` version is available at runtime.
- Type annotations and type checking: ensure the code generation approach works well with mypy.
- Code coverage: ensure that `coverage.py` is able to correctly identify which parts of the code are covered.

## Installation

```
scripts/install
```

## Usage

To build the `_sync` version of the code:

```
scripts/compile
```

This runs `python setup.py sdist bdist_wheel` and generates a (temporary) source distribution in the root directory. Any existing installation of `hello-unasync` is then removed and `hello-unasync` is reinstalled from the built source distribution.

This script should be run so that changes to the code are reflected at run time.

For this reason, it is automatically run in `scripts/install` and `scripts/test`.

## Notes

### `_sync` and linting

Anything that lives under the `_async` sub-package will be processed by `unasync` to produce its equivalent sync version in the `_sync` sub-package. (The way this works is mainly by stripping any `async` and `await` annotations.)

This means that the `_sync` sub-package is not present in the source tree, but for linters it shouldn't be a problem.

In particular, mypy and flake8 are able to recognize `_sync` as long as a compiled version of the package is installed (rather than with `pip install .` only).

### Concurrency backends

Concurrency backends (currently AsyncIO and sync) live under the `concurrency_backends` sub-package.

The base class, `ConcurrencBackend`, is located under `_async` so that its synchronous version can be imported and sub-classed by the sync backend while making sure linters are happy.

(If `SyncBackend` was a subclass of the (async) `ConcurrencyBackend`, then linters would complain as it implements the sync versions of all methods. Likewise, if methods of `ConcurrencyBackend` were declared with `def` and annotated to return `Union[T, Awaitable[T]]`, then to linters they wouldn't be awaitable in the async version of the code because they aren't guaranteed to return an awaitable. For all these reasons, we also need to code-gen a synchronous version of `ConcurrencyBackend`.)

### Code coverage

The current setup doesn't work well with `coverage.py`.

When using `pip install -e`, `coverage.py` is able to map files of the installed package to those of the source tree (*probably* thanks to the `.egg-info` file).

But because we install from a source distribution, that mapping can't be performed any more, and `coverage.py` traces files from the actual location of the installed package (e.g. `venv/lib/python3.8/site-packages/hello-unasync`) instead of files from the source tree.

## License

MIT
