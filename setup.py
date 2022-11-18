# coding:utf-8
import sys

from setuptools import setup, find_packages
from volcengine import VERSION

install_requires = ["requests", "retry", "pytz", "pycryptodome", "protobuf", "google", "six", "lz4a"]

# 在Windows平台上不安装不兼容的第三方库
if sys.platform in ("win32", "cygwin"):
    install_requires.remove("lz4a")

setup(
    name="volcengine",
    version=VERSION,
    keywords=("pip", "volcengine", "volc-sdk-python"),
    description="The Volcengine SDK for Python",
    license="MIT Licence",

    url="https://github.com/Volcengine/volc-sdk-python",
    author="Volcengine SDK",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=install_requires
)
