import unittest

from accounts.tests import test

def suite():
    tests_loader = unittest.TestLoader().loadTestsFromModule
    test_suites = []
    test_suites.append(tests_loader(test))
    return unittest.TestSuite(test_suites)