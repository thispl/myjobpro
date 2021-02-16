# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in myjobpro/__init__.py
from myjobpro import __version__ as version

setup(
	name='myjobpro',
	version=version,
	description='Frappe Backend for MyjobPRO Mobile App',
	author='TeamPRO',
	author_email='erp@groupteampro.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
