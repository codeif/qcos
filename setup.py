#!/usr/bin/env python
from setuptools import find_packages, setup

with open("README.rst") as f:
    readme = f.read()


setup(
    name="qcos",
    version="2.0.1",
    description="腾讯云对象存储库，支持命令行",
    long_description=readme,
    author="codeif",
    author_email="me@codeif.com",
    url="https://github.com/codeif/qcos",
    license="MIT",
    entry_points={"console_scripts": ["qcos = qcos.cli:main"]},
    install_requires=["requests", "termcolor"],
    packages=find_packages(exclude=("tests", "tests.*")),
)
