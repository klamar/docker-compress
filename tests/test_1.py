#!/usr/bin/python
# -*- coding: UTF-8 -*-
r"""
@author: Martin Klapproth <martin.klapproth@googlemail.com>
"""
from genericpath import isfile
import os
from shutil import copy

import unittest
import subprocess
import sys
from tests import rm


class MyTestCase(unittest.TestCase):
    def setUp(self):
        rm("/work/cc_logo.png.gz")

        rm("/work/test.png.gz")
        rm("/work/test.png.br")
        rm("/work/test.png.orig")

        copy("/work/cc_logo.png", "/work/test.png")

    def test_something(self):
        self.assertFalse(isfile("/work/test.png.gz"))
        self.assertFalse(isfile("/work/test.png.br"))
        self.assertFalse(isfile("/work/test.png.orig"))

        with open("/work/test.png", "rb") as f:
            orig_contents = f.read()

        os.chown("/work/test.png", 7777, 7777)
        rcode = subprocess.call([sys.executable, "/data/app/compress.py", "-v", "/work", "-e", "cc_logo.*"])
        self.assertEqual(0, rcode)

        with open("/work/test.png.orig", "rb") as f:
            new_orig_contents = f.read()

        self.assertEqual(orig_contents, new_orig_contents)

        # should have been excluded
        self.assertFalse(isfile("/work/cc_logo.png.gz"))

        self.assertTrue(isfile("/work/test.png"))
        self.assertTrue(isfile("/work/test.png.gz"))
        self.assertTrue(isfile("/work/test.png.br"))
        self.assertTrue(isfile("/work/test.png.orig"))

        stat_orig = os.stat("/work/test.png")
        stat_br = os.stat("/work/test.png.gz")
        stat_gz = os.stat("/work/test.png.br")
        stat_png_orig = os.stat("/work/test.png.orig")

        self.assertEqual(stat_orig.st_mode, stat_br.st_mode)
        self.assertEqual(stat_orig.st_mode, stat_gz.st_mode)
        self.assertEqual(stat_orig.st_mode, stat_png_orig.st_mode)

        self.assertEqual(stat_orig.st_uid, stat_br.st_uid)
        self.assertEqual(stat_orig.st_uid, stat_gz.st_uid)
        self.assertEqual(stat_orig.st_uid, stat_png_orig.st_uid)

        self.assertEqual(stat_orig.st_gid, stat_br.st_gid)
        self.assertEqual(stat_orig.st_gid, stat_gz.st_gid)
        self.assertEqual(stat_orig.st_gid, stat_png_orig.st_gid)

        self.assertEqual(int(stat_orig.st_atime), int(stat_br.st_atime))
        self.assertEqual(int(stat_orig.st_atime), int(stat_gz.st_atime))
        self.assertEqual(int(stat_orig.st_atime), int(stat_png_orig.st_atime))

        self.assertEqual(int(stat_orig.st_mtime), int(stat_br.st_mtime))
        self.assertEqual(int(stat_orig.st_mtime), int(stat_gz.st_mtime))
        self.assertEqual(int(stat_orig.st_mtime), int(stat_png_orig.st_mtime))

        self.assertLess(stat_orig.st_size, stat_png_orig.st_size) # .png < .png.orig


if __name__ == '__main__':
    unittest.main()
