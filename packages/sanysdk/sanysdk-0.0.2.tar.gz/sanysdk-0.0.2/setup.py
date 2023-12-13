#############################################
# File Name: setup.py
# Author: liuxb
# Mail: llxiangbin@163.com
# Created Time:  2023-12-11 16:28:34
#############################################


from setuptools import setup, find_packages
import sys
import importlib

importlib.reload(sys)

setup(
    name="sanysdk",
    version="0.0.2",
    keywords=["pip", "sanysdk", "liuxb", "sdk", "sany"],
    description="Encapsulateing Interface",
    long_description=" Encapsulating Interface",
    license="MIT Licence",

    url="https://gitlab.sanywind.net/bigdata/dmo-client-python-sdk",
    author="liuxb",
    author_email="llxiangbin@163.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=['requests', 'pandas', 'retry']
)