import unittest
import sys
import datetime
from io import StringIO
from GEDCOM import dateverify

class Test(unittest.TestCase):

    def test_dateverify(self):
        US42d1 = "2 JAN 2018"
        self.assertEqual(dateverify(US42d1), True)
        
        US42d2 = "29 FEB 2018"
        self.assertEqual(dateverify(US42d2), False)

        US42d3 = "29 FEB 2016"
        self.assertEqual(dateverify(US42d3), True)

        US42d4 = "31 JUN 2016"
        self.assertEqual(dateverify(US42d4), False)

        US42d5 = "31 DEC 2010"
        self.assertEqual(dateverify(US42d5), True)