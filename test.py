#!/usr/bin/python
# -*- coding: UTF-8 -*-
r"""
@author: Martin Klapproth <martin.klapproth@googlemail.com>
"""
import unittest

testmodules = [
    'tests.test_1',
    ]

suite = unittest.TestSuite()

for t in testmodules:
    try:
        # If the module defines a suite() function, call it to get the suite.
        mod = __import__(t, globals(), locals(), ['suite'])
        suitefn = getattr(mod, 'suite')
        suite.addTest(suitefn())
    except (ImportError, AttributeError):
        # else, just load all the test cases from the module.
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

result = unittest.TextTestRunner().run(suite)

exit_code = 0 if result.errors == 0 and result.failures == 0 else 1
exit(exit_code)
