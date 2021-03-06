#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from pathlib import Path

import unasync
from setuptools import setup, find_packages


def get_version(package: str) -> str:
    version = (Path("src") / package / "__version__.py").read_text()
    match = re.search("__version__ = ['\"]([^'\"]+)['\"]", version)
    assert match is not None
    return match.group(1)


def get_long_description() -> str:
    with open("README.md", encoding="utf8") as readme:
        return readme.read()


setup(
    name="hello-unasync",
    python_requires=">=3.7",
    version=get_version("hello_unasync"),
    url="https://github.com/florimondmanca/hello-unasync",
    license="MIT",
    description=(
        "Example Python package supporting async + sync "
        "via code generation, tooling included"
    ),
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Florimond Manca",
    author_email="florimond.manca@gmail.com",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=["sniffio"],
    cmdclass={"build_py": unasync.build_py},
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Framework :: AsyncIO",
        "Framework :: Trio",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
