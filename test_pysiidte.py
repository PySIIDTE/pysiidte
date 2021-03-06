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
import pysiidte
try:
    from ctest.certs import *
except ImportError:
    pk, ct = False, False
    pass


def test_char_replace():
    total = pysiidte.char_replace(u'á')
    assert total == 'a'


def test_check_digest():
    testtype = ['0', '1', '20']
    for t in testtype:
        fileuri = 'testdata/dte%s.xml' % t
        file = open(fileuri, 'r')
        xml = file.read()
        assert pysiidte.check_digest(xml)


def test_sii_token():
    if pk and ct:
        assert len(pysiidte.sii_token('SIIHOMO', pk, ct)) == 13
    else:
        assert True
