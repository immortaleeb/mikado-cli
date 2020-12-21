#!/usr/bin/env python3

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mikado-cli",
    version="0.0.1",
    author="Enver Bral",
    author_email="enverbral@gmail.com",
    description="A cli tool for managing tasks based on the mikado method",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
    ],
    scripts=['bin/mikado'],
    packages=setuptools.find_namespace_packages(include=['mikado.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)

