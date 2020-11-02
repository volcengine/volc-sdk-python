# coding:utf-8

from setuptools import setup, find_packages
from volc import VERSION

setup(
    name="volc",
    version=VERSION,
    keywords=("pip", "volc", "volc-sdk-python"),
    description="The Volcengine SDK for Python",
    license="MIT Licence",

    url="https://github.com/Volcengine/volc-sdk-python",
    author="Volcengine SDK",    

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["requests", "pytz", "pycryptodome", "protobuf", "google-api-python-client"]
)
