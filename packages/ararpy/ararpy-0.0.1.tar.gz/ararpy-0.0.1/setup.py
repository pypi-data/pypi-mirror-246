#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# ==========================================
# Copyright 2023 Yang 
# ararpy - setup
# ==========================================
#
#
#

import setuptools  # 导入setuptools打包工具

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ararpy",  #
    version="0.0.1",  # version
    author="Yang Wu",
    author_email="wuycug@hotmail.com",
    description="A package for Ar-Ar geochronology",  # short description
    long_description=long_description,  # detailed description in README.md
    long_description_content_type="text/markdown",
    url="https://github.com/wuyangchn/ararpy.git",  # github url
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # 对python的最低版本要求
)
