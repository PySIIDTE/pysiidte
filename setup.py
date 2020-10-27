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

import glob
import os
import subprocess
import sys
import warnings

from setuptools import find_packages, setup

data_files = [
    ("xsd", ["xsd/ConsumoFolio_v10.xsd", "xsd/DTE_v10.xsd", "xsd/EnvioBOLETA_v11.xsd",
             "xsd/EnvioDTE_v10.xsd", "xsd/EnvioRecibos_v10.xsd", "xsd/LceCal_v10.xsd",
             "xsd/LceCoCertif_v10.xsd", "xsd/LceSiiTypes_v10.xsd", "xsd/LibroBOLETA_v10.xsd",
             "xsd/LibroCVS_v10.xsd", "xsd/LibroCV_v10.xsd", "xsd/LibroGuia_v10.xsd",
             "xsd/Recibos_v10.xsd", "xsd/RespSII_v10.xsd", "xsd/RespuestaEnvioDTE_v10.xsd",
             "xsd/SiiTypes_v10.xsd", "xsd/xmldsignature_v10.xsd", ]),
    ]


setup(
    name='pysiidte',
    version='0.2',
    url='https://github.com/PySIIDTE/pysiidte',
    license='AGPL-3',
    author='Daniel Blanco Martín',
    author_email='daniel@blancomartin.cl',
    description='Utilidades para firma y conexión SII Chile',
    long_description=open('README.md').read(),
    install_requires=[
        # 'lxml >= 3.6.0, < 3.7',
        # 'defusedxml >= 0.4.1, < 0.5',
        # 'eight >= 0.3.0, < 0.4',
        # 'pyOpenSSL == 17.0.0',
        # 'hashlib',
        'cchardet',
        'cryptography == 3.2',
        'lxml',
        'pyOpenSSL == 16.2.0',
        # 'certifi >= 2015.11.20.1',
        'signxml >= 2.4',
        'suds-jurko == 0.6',
        'bs4',
        'pytz'
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
    data_files=data_files,
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
