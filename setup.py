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

# import glob
# import os
# import subprocess
# import sys
# import warnings

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
    version='0.5',
    url='https://github.com/PySIIDTE/pysiidte',
    license='AGPL-3',
    author='Daniel Blanco Martín',
    author_email='daniel@blancomartin.cl',
    description='Utilidades para firma y conexión SII Chile',
    long_description=open('README.md').read(),
    install_requires=[
        'bs4 == 0.0.1',
        'cchardet == 2.1.1',
        'cryptography == 2.3.1',
        'pyOpenSSL == 16.2.0',
        'signxml >= 2.5.2',
        'suds - jurko ==0.6',
        'pytz == 2016.7',
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
