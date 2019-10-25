#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from setuptools import find_packages, setup

with open("README.md") as f:
    readme = f.read()

with open("LICENSE") as f:
    license = f.read()

setup(
    name="matscholar_web",
    version="0.0.1",
    description="The Materials Scholar Website and Apps",
    long_description=readme,
    author="Materials Scholar Development Team",
    author_email="jdagdelen@lbl.gov, vahe@tshitoyan.com, lweston@lbl.gov, ardunn@lbl.gov",
    url="https://github.com/materialsintelligence/matscholar-web",
    license=license,
    packages=find_packages(),
    test_suite="matscholar_web",
    tests_require="tests",
)
