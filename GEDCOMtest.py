import unittest
import sys
import datetime
from io import StringIO
from GEDCOM import dateverify
from GEDCOM import us03
from GEDCOM import Person
from GEDCOM import us02
from GEDCOM import Family

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
        p1 = Person()
        p2 = Person()
        p3 = Person()       
        p4 = Person()
        p5 = Person()

        date1 = "7 JAN 2010"
        date2 = "8 FEB 2011"
        date3 = "9 MAR 2012"
        date4 = "10 APR 2013"
        date5 = "11 MAY 2014"

        p1.BIRT = date1
        p1.DEAT = date2
        self.assertEqual(us03(p1), True)

        p2.BIRT = date2
        p2.DEAT = date1
        self.assertEqual(us03(p2), False)

        p3.BIRT = date3
        p3.DEAT = date4
        self.assertEqual(us03(p3), True)

        p4.BIRT = date5
        p4.DEAT = date4
        self.assertEqual(us03(p4), False)

        p5.BIRT = date4
        p5.DEAT = date4
        self.assertEqual(us03(p5), False)

    def test02(self):
        p1 = Person()
        p2 = Person()
        p3 = Person()       
        p4 = Person()
        p5 = Person()

        f1 = Family()
        f2 = Family()
        f3 = Family()
        f4 = Family()
        f5 = Family()

        date1 = "7 JAN 2010"
        date2 = "8 FEB 2011"
        date3 = "9 MAR 2012"
        date4 = "10 APR 2013"
        date5 = "11 MAY 2014"

        p1.BIRT = date1
        f1.MARR = date2
        self.assertEqual(us02(p1, f1), True)
        
        p2.BIRT = date2
        f2.MARR = date1
        self.assertEqual(us02(p2, f2), False)

        p3.BIRT = date3
        f3.MARR = date4
        self.assertEqual(us02(p3, f3), True)

        p4.BIRT = date5
        f4.MARR = date4
        self.assertEqual(us02(p4, f4), False)

        p5.BIRT = date4
        f5.MARR = date4
        self.assertEqual(us02(p5, f5), False)
