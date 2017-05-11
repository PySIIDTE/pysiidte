#!/usr/bin/python
# -*- coding: utf-8 -*-
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

"Utilidad para instalación de paquete de pysiidte"

__author__ = "Daniel Blanco Martín (daniel@blancomartin.cl)"
__copyright__ = "Copyright (C) 2015-2017 Blanco Martín y Asoc. EIRL - BMyA S.A."
__license__ = "AGPL 3.0"

from setuptools import setup, find_packages
import glob
import os
import subprocess
import warnings
import sys

setup(
    name='pysiidte',
    version='0.1',
    url='https://bitbucket.org/hdblanco/pysiidte',
    license='AGPL-3',
    author='Daniel Blanco Martín',
    author_email='daniel@blancomartin.cl',
    description='Utilidades para firma y conexión SII Chile',
    long_description=open('README.rst').read(),
    install_requires=[
        # 'lxml >= 3.6.0, < 3.7',
        # 'defusedxml >= 0.4.1, < 0.5',
        # 'eight >= 0.3.0, < 0.4',
        # 'cryptography >= 1.4, < 1.5',
        # 'pyOpenSSL >= 16.0.0, < 17',
        # 'certifi >= 2015.11.20.1',
        'signxml',
        'logging',
        'suds',
        'bs4',
    ],
    extras_require={
        ':python_version == "2.7"': ['enum34 >= 1.0.4'],
        ':python_version == "3.3"': ['enum34 >= 1.0.4']
    },
    # packages=find_packages(exclude=['test']),
    # packages=['pysiidte'],
    py_modules=['pysiidte'],
    platforms=['MacOS X', 'Posix'],
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: AGPL-3',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)