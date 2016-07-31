#! /usr/bin/env python3

import unittest
import os
from context import GetIniStrings

class TestGetIniStrings(unittest.TestCase):

    def test_basic(self):
        parser = GetIniStrings(os.getcwd())
        res = parser.parse()
        self.assertTrue(parser.findString('A_RANDOM_STRING'))

if __name__ == '__main__':
    unittest.main()
