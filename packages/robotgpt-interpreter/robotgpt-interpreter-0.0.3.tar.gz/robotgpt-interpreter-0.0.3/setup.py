#!/usr/bin/env python
# coding: utf-8

import setuptools
from setuptools import setup
with open("README1.md", "r", encoding="UTF-8") as fh:
    long_description = fh.read()
setup(
    name='robotgpt-interpreter',
    version='0.0.3',
    author='blaze.zhang',
    author_email='blaze.zhang@cloudminds.com',
    url='https://src.cloudminds.com/ai-api/robotgpt-interpreter',
    description=u'robotgpt-interpreter',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['interpreter'],
)