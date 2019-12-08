# hello-unasync

This repository is a proof-of-concept of code-generating the `sync` version of an `async`-capable Python package while providing all the development tooling now common for 3.6+ Python packages: type hints, linting, code formatting, code coverage.

Code generation is provided by [`unasync`](https://unasync.readthedocs.io/en/latest/).

## Usage

Install locally using:

```
scripts/install
```

To run the tests:

```
scripts/test
```

## Notes

### Compilation

To build the `_sync` version of the code, use:

```
scripts/compile
```

This script:

1. Builds the source/binary distribution. (This stage invokes `unasync`.)
1. Removes any existing installation of `hello-unasync`.
1. Installs `hello-unasync` from the built distribution.

This script should be run after every changes made to the code, so that changes to the code are reflected at run time. (Instead of an edit/run workflow, we now have edit/compile/run.) For this reason, it is automatically run in `scripts/install` and `scripts/test`.

### `_sync` and linting

Anything that lives under the `_async` sub-package will be processed by `unasync` to produce its equivalent sync version in the `_sync` sub-package. (The way this works is mainly by stripping any `async` and `await` annotations.)

This means that the `_sync` sub-package is not present in the source tree, but for linters it shouldn't be a problem.

In particular, mypy and flake8 are able to recognize `_sync` as long as a compiled version of the package is installed (rather than with `pip install .` only).

### Concurrency backends

Concurrency backends (currently AsyncIO and sync) live under the `concurrency_backends` sub-package.

The base class, `ConcurrencBackend`, is located under `_async` so that its synchronous version can be imported and sub-classed by the sync backend while making sure linters are happy.

(If `SyncBackend` was a subclass of the (async) `ConcurrencyBackend`, then linters would complain as it implements the sync versions of all methods. Likewise, if methods of `ConcurrencyBackend` were declared with `def` and annotated to return `Union[T, Awaitable[T]]`, then to linters they wouldn't be awaitable in the async version of the code because they aren't guaranteed to return an awaitable. For all these reasons, we also need to code-gen a synchronous version of `ConcurrencyBackend`.)

### Code coverage

When using `pip install -e`, `coverage.py` is able to map files of the installed package to those of the source tree (*probably* thanks to the `.egg-info` file).

But because we install from a source distribution, that mapping can't be performed any more, and passing `--cov=src` to `coverage.py` won't work. This is because `coverage.py` now runs files from the actual location of the installed package (e.g. `venv/lib/python3.8/site-packages/hello-unasync`) instead of files from the source tree.

To resolve this problem, the location of the installed package is passed as an extra `--cov` option by `scripts/test`.

### Alternatives

This repository builds the `sync` version of the package at build-time, but this is not the only approach.

[python-trio/hip#149](https://github.com/python-trio/hip/issues/149) suggests at least two other options:

- Compile the `sync` version before every commit, and commit it to source control.
- Compile the `sync` version at import-time.

## License

MIT
