# coding:utf-8
import sys

from setuptools import setup, find_packages
from volcengine import VERSION

install_requires = [
    "requests>=2.25.1",
    "retry>=0.9.2,<1.0.0",
    "pytz>=2020.5",
    "pycryptodome>=3.9.9,<4.0.0",
    "protobuf>=3.18.3",
    "google>=3.0.0",
    "six>=1.0",
    "tenacity>=8.0.0",
    "readerwriterlock>=1.0.9",
]

setup(
    name="volcengine",
    version=VERSION,
    keywords=["pip", "volcengine", "volc-sdk-python"],
    description="The Volcengine SDK for Python",
    license="MIT License",

    url="https://github.com/Volcengine/volc-sdk-python",
    author="Volcengine SDK",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    install_requires=install_requires
)
