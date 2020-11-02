# coding:utf-8

from setuptools import setup, find_packages

setup(
    name="volc",
    version="0.0.31",
    keywords=("pip", "volc", "volc-sdk-python"),
    description="The Volcengine SDK for Python",
    license="MIT Licence",

    url="https://github.com/Volcengine/volc-sdk-python",
    author="TTVcloud SDK",
    author_email="volcplatform@bytedance.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["requests", "pytz", "pycryptodome"]
)
