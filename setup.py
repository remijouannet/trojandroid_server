#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(name='android_trojan_server',
	version='1.1',
	author='Rémi Jouannet',
	packages=find_packages(),
	entry_points={
		'console_scripts': ['androidtrojan = app.app:main']
	},
	install_requires=open('requirements.txt').readlines()
)
