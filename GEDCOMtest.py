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
   
    def test03(self):
        date1 = datetime.date(2010, 1, 7)
        date2 = datetime.date(2011, 2, 8)
        date3 = datetime.date(2012, 3, 9)
        date4 = datetime.date(2013, 4, 10)
        date5 = datetime.date(2014, 5, 11)

        self.assertEqual(us03(date1, date2), True)
        self.assertEqual(us03(date2, date1), False)
        self.assertEqual(us03(date3, date4), True)
        self.assertEqual(us03(date5, date4), False)
        self.assertEqual(us03(date4, date4), False)
