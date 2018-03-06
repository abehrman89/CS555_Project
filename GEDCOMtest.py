import unittest
import sys
import datetime
from io import StringIO
from GEDCOM import dateverify
from GEDCOM import us03
from GEDCOM import Person
from GEDCOM import us02
from GEDCOM import Family
from GEDCOM import dbeforecurrent
from GEDCOM import us04
from GEDCOM import deceasedlist

class Test(unittest.TestCase):

    def test42(self):
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

    def test01(self):
        US01d1 = "2 JAN 2018"
        self.assertEqual(dbeforecurrent(US01d1), True)

        US01d2 = "4 AUG 2019"
        self.assertEqual(dbeforecurrent(US01d2), False)

        US01d3 = "3 MAR 2018"
        self.assertEqual(dbeforecurrent(US01d3), True)

        US01d4 = "23 OCT 1987"
        self.assertEqual(dbeforecurrent(US01d4), True)

        US01d5 = "18 NOV 3014"
        self.assertEqual(dbeforecurrent(US01d5), False)
    
    def test04(self):
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

        f1.MARR = date1
        f1.DIV = date2
        self.assertEqual(us04(f1), True)

        f2.MARR = date2
        f2.DIV = date1
        self.assertEqual(us04(f2), False)

        f3.MARR = date3
        f3.DIV = date4
        self.assertEqual(us04(f3), True)

        f4.MARR = date5
        f4.DIV = date4
        self.assertEqual(us04(f4), False)

        f5.MARR = date4
        f5.DIV = date4
        self.assertEqual(us04(f5), False)

    def test29(self):
        us29p1 = Person()
        us29p2 = Person()
        us29p3 = Person()
        us29p4 = Person()
        us29p5 = Person()
        
        us29p1._id = "@I1@"
        us29p2._id = "@I2@"
        us29p3._id = "@I3@"       
        us29p4._id = "@I4@"
        us29p5._id = "@I5@"

        us29p1.NAME = "Person 1"
        us29p2.NAME = "Person 2"
        us29p3.NAME = "Person 3"       
        us29p4.NAME = "Person 4"
        us29p5.NAME = "Person 5"

        us29p1.DEAT = "7 JAN 2010"
        us29p2.DEAT = ""
        us29p3.DEAT = "9 MAR 2012"       
        us29p4.DEAT = "10 APR 2013"
        us29p5.DEAT = "N/A"

        us29dic = {0:us29p1}
        self.assertEqual(deceasedlist(us29dic), ['Person 1, @I1@'])

        us29dic = {"@I1@":us29p1, "@I2@":us29p2}
        self.assertEqual(deceasedlist(us29dic), ['Person 1, @I1@'])

        us29dic = {"@I1@":us29p1, "@I2@":us29p2, "@I3@":us29p3}
        self.assertEqual(deceasedlist(us29dic), ['Person 1, @I1@', 'Person 3, @I3@'])

        us29dic = {"@I1@":us29p1, "@I2@":us29p2, "@I3@":us29p3, "@I4@":us29p4}
        self.assertEqual(deceasedlist(us29dic), ['Person 1, @I1@', 'Person 3, @I3@', 'Person 4, @I4@'])

        us29dic = {"@I1@":us29p1, "@I2@":us29p2, "@I3@":us29p3, "@I4@":us29p4, "@I5@":us29p5}
        self.assertEqual(deceasedlist(us29dic), ['Person 1, @I1@', 'Person 3, @I3@', 'Person 4, @I4@'])
