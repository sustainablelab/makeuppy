"""--- Run unit tests from Vim: ---

VIM USAGE:
    ;ut -- run unit tests for pkgname
        - requires active buffer is test_pkgname.py
"""
import unittest
import pygameapi

class pygameapi_unittest_PlumbingIsOK(unittest.TestCase):
    """Check the plumbing."""
    def test_plumbing(self):
        self.assertTrue(True)
