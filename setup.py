#!/usr/bin/env python
from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()


setup(
    name='qcos',
    version='0.1.1',
    description='腾讯云对象存储库，支持命令行',
    long_description=readme,
    author='codeif',
    author_email='me@codeif.com',
    url='https://github.com/codeif/qcos',
    license='MIT',
    entry_points={
        'console_scripts': [
            'qcos = qcos.cli:main',
        ],
    },
    install_requires=['requests', 'termcolor'],
    packages=find_packages(exclude=("tests", "tests.*")),
)
