#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools,distutils,shutil,re,os

with open("README.md", "r",encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="pz7z8",
    version="0.1.8",
    author="Chen chuan",
    author_email="kcchen@139.com",
    description="一些零碎的小工具集",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    zip_safe= False,
    include_package_data = True,
    entry_points={
        'console_scripts':  [
            'dsync=z7z8.dsync:dsync',
            'dfslow=z7z8.dfslow:dfslow',
            'smod=z7z8.smod:main',
            'md2pdf=z7z8.md2pdf:main',
            'chgver=z7z8.chgver:main',
            'sshall=z7z8.sshall:main',
        ],
    },
)
