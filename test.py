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
import unittest


class TestMethods(unittest.TestCase):
    def test_add(self):
        self.assertEqual(pysiidte.char_replace(u'á'), "a")

if __name__ == '__main__':
    unittest.main()
