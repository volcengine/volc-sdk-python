# coding:utf-8

from setuptools import setup, find_packages

setup(
    name="ttvcloud",
    version="0.0.31",
    keywords=("pip", "ttvcloud", "vcloud-sdk-python"),
    description="The TTvcloud SDK for Python",
    license="MIT Licence",

    url="https://github.com/TTvcloud/vcloud-sdk-python",
    author="TTVcloud SDK",
    author_email="vcloudplatform@bytedance.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["requests", "pytz", "pycryptodome", "protobuf", "google-api-python-client"]
)
