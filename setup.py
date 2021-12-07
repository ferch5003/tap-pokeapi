#!/usr/bin/env python
from setuptools import setup

setup(
    name="tap-pokeapi",
    version="0.1.0",
    description="Extract Pokemon Data through PokeAPI",
    author="Stitch",
    url="http://singer.io",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["tap_pokeapi"],
    install_requires=[
        # NB: Pin these to a more specific version for tap reliability
        "singer-python",
        "requests",
    ],
    entry_points="""
    [console_scripts]
    tap-pokeapi=tap_pokeapi:main
    """,
    packages=["tap_pokeapi"],
    package_data = {
        "schemas": ["tap_pokeapi/schemas/*.json"]
    },
    include_package_data=True,
)
