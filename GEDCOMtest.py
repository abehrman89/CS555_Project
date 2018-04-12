import unittest
import sys
import datetime
from io import StringIO
from GEDCOM import dateverify, us03, Person, Family, us02, dbeforecurrent, us04
from GEDCOM import deceasedlist, us05, findage, livingmarriedlist, singlelist, us06, us07
from GEDCOM import us10, us21, childcheck

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
        self.assertEqual(deceasedlist(us29dic), ['@I1@'])

        us29dic = {"@I1@":us29p1, "@I2@":us29p2}
        self.assertEqual(deceasedlist(us29dic), ['@I1@'])

        us29dic = {"@I1@":us29p1, "@I2@":us29p2, "@I3@":us29p3}
        self.assertEqual(deceasedlist(us29dic), ['@I1@', '@I3@'])

        us29dic = {"@I1@":us29p1, "@I2@":us29p2, "@I3@":us29p3, "@I4@":us29p4}
        self.assertEqual(deceasedlist(us29dic), ['@I1@', '@I3@', '@I4@'])

        us29dic = {"@I1@":us29p1, "@I2@":us29p2, "@I3@":us29p3, "@I4@":us29p4, "@I5@":us29p5}
        self.assertEqual(deceasedlist(us29dic), ['@I1@', '@I3@', '@I4@'])

    def test05(self):
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

        p1.DEAT = date1
        f1.MARR = date2
        self.assertEqual(us05(p1, f1), False)
        
        p2.DEAT = date2
        f2.MARR = date1
        self.assertEqual(us05(p2, f2), True)

        p3.DEAT = date3
        f3.MARR = date4
        self.assertEqual(us05(p3, f3), False)

        p4.DEAT = date5
        f4.MARR = date4
        self.assertEqual(us05(p4, f4), True)

        p5.DEAT = date4
        f5.MARR = date4
        self.assertEqual(us05(p5, f5), False)

    def test27(self):
        self.assertEqual(findage("1 AUG 1997"), 20)
        self.assertEqual(findage("15 DEC 1999"), 18)
        self.assertEqual(findage("30 OCT 1897"), 120)
        self.assertEqual(findage("1 SEP 1969"), 48)
        self.assertEqual(findage("14 JUN 2006"), 11)

    def test30(self):
        us30p1 = Person()
        us30p2 = Person()
        us30p3 = Person()
        us30p4 = Person()

        us30f1 = Family()
        us30f2 = Family()
        
        us30p1._id = "@I1@"
        us30p2._id = "@I2@"
        us30p3._id = "@I3@"       
        us30p4._id = "@I4@"

        us30f1._id = "@F1@"
        us30f2._id = "@F2@"

        us30f1.HUSB = us30p1._id
        us30f1.WIFE = us30p2._id
        us30f2.HUSB = us30p3._id
        us30f2.WIFE = us30p4._id

        us30p1.NAME = "Person 1"
        us30p2.NAME = "Person 2"
        us30p3.NAME = "Person 3"       
        us30p4.NAME = "Person 4"

        us30p1.DEAT = "7 JAN 2010"
        us30p2.DEAT = "N/A"
        us30p3.DEAT = "N/A"       
        us30p4.DEAT = "N/A"

        us30f1.MARR = "1 JUN 2009"
        us30f1.DIV = "N/A"

        us30f2.MARR = "1 JUN 2009"
        us30f1.DIV = "N/A"

        us30dic = {"@I1@":us30p1, "@I2@":us30p2}
        us30dicf = {"@F1@":us30f1}
        self.assertEqual(livingmarriedlist(us30dic, us30dicf), [])

        us30p1.DEAT = "N/A"
        us30dic = {"@I1@":us30p1, "@I2@":us30p2}
        us30dicf = {"@F1@":us30f1}
        self.assertEqual(livingmarriedlist(us30dic, us30dicf), ["@I1@", "@I2@"])

        us30dic = {"@I1@":us30p1, "@I2@":us30p2, "@I3@":us30p3, "@I4@":us30p4}
        us30dicf = {"@F1@":us30f1, "@F2@":us30f2}
        self.assertEqual(livingmarriedlist(us30dic, us30dicf), ["@I1@", "@I2@", "@I3@", "@I4@"])

        us30dic = {"@I3@":us30p3, "@I4@":us30p4}
        us30dicf = {"@F2@":us30f2}
        self.assertEqual(livingmarriedlist(us30dic, us30dicf), ["@I3@", "@I4@"])

        us30p1.DEAT = "7 JAN 2010"
        us30f2.DIV = "2 JUN 2009"
        us30dic = {"@I1@":us30p1, "@I2@":us30p2, "@I3@":us30p3, "@I4@":us30p4}
        us30dicf = {"@F1@":us30f1, "@F2@":us30f2}
        self.assertEqual(livingmarriedlist(us30dic, us30dicf), [])

    def test31(self):
        us31p1 = Person()
        us31p2 = Person()
        us31p3 = Person()
        us31p4 = Person()

        us31p1._id, us31p1.AGE = "@I1@", 25
        us31p2._id, us31p2.AGE = "@I2@", 31
        us31p3._id, us31p3.AGE = "@I3@", 45
        us31p4._id, us31p4.AGE = "@I4@", 36

        us31f1 = Family()
        us31f2 = Family()

        us31f1._id = "@F1@"
        us31f2._id = "@F2@"

        us31f1.HUSB = us31p1._id
        us31f1.WIFE = us31p2._id
        us31f2.HUSB = us31p3._id
        us31f2.WIFE = us31p4._id

        us31f1.MARR = "1 JUN 2009"
        us31f1.DIV = "N/A"
        us31f2.MARR = "1 JUN 2009"
        us31f1.DIV = "N/A"

        us31dic = {"@I1@":us31p1, "@I2@":us31p2}
        us31dicf = {"@F1@":us31f1}
        self.assertEqual(singlelist(us31dic, us31dicf), [])

        us31f1.MARR = "N/A"
        us31dic = {"@I1@":us31p1, "@I2@":us31p2}
        us31dicf = {"@F1@":us31f1}
        self.assertEqual(singlelist(us31dic, us31dicf), ["@I2@"])

        us31dic = {"@I3@":us31p3, "@I4@":us31p4}
        us31dicf = {"@F2@":us31f2}
        self.assertEqual(singlelist(us31dic, us31dicf), [])

        us31dic = {"@I1@":us31p1, "@I2@":us31p2, "@I3@":us31p3, "@I4":us31p4}
        us31dicf = {"@F1@":us31f1, "@F2@":us31f2}
        self.assertEqual(singlelist(us31dic, us31dicf), ["@I2@"])

        us31f2.MARR = "N/A"
        us31dic = {"@I1@":us31p1, "@I2@":us31p2, "@I3@":us31p3, "@I4":us31p4}
        us31dicf = {"@F1@":us31f1, "@F2@":us31f2}
        self.assertEqual(singlelist(us31dic, us31dicf), ["@I2@", "@I3@", "@I4@"])
    
    def test06(self):
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

        p1.DEAT = date1
        f1.DIV = date2
        self.assertEqual(us06(p1, f1), False)
        
        p2.DEAT = date2
        f2.DIV = date1
        self.assertEqual(us06(p2, f2), True)

        p3.DEAT = date3
        f3.DIV = date4
        self.assertEqual(us06(p3, f3), False)

        p4.DEAT = date5
        f4.DIV = date4
        self.assertEqual(us06(p4, f4), True)

        p5.DEAT = date4
        f5.DIV = date4
        self.assertEqual(us06(p5, f5), False)

    def test07(self):
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

        date6 = "7 JAN 2170"
        date7 = "8 FEB 2170"
        date8 = "9 MAR 2180"
        date9 = "10 APR 2180"
        date10 = "11 MAY 1795"

        p1.BIRT = date1
        p1.DEAT = date8
        self.assertEqual(us07(p1), False)
        
        p2.BIRT = date2
        p2.DEAT = date5
        self.assertEqual(us07(p2), True)

        p3.BIRT = date3
        p3.DEAT = date9
        self.assertEqual(us07(p3), False)

        p4.BIRT = date4
        p4.DEAT = 'N/A'
        self.assertEqual(us07(p4), True)

        p5.BIRT = date10
        p5.DEAT = 'N/A'
        self.assertEqual(us07(p5), False)

    def test10(self):
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

        date1 = "7 JAN 1980"
        date2 = "8 FEB 1990"
        date3 = "9 MAR 2003"
        date4 = "10 APR 2013"
        date5 = "11 MAY 2014"

        p1.BIRT = date1
        f1.MARR = date2
        self.assertEqual(us10(p1, f1), False)
        
        p2.BIRT = date1
        f2.MARR = date5
        self.assertEqual(us10(p2, f2), True)

        p3.BIRT = date2
        f3.MARR = date3
        self.assertEqual(us10(p3, f3), False)

        p4.BIRT = date2
        f4.MARR = date4
        self.assertEqual(us10(p4, f4), True)

        p5.BIRT = date3
        f5.MARR = date4
        self.assertEqual(us10(p5, f5), False)
    
    def test21(self):
        p1 = Person()
        p1.SEX = 'M'
        p1._id = '1'
        p2 = Person()
        p2.SEX = 'M'
        p2._id = '2'
        p3 = Person() 
        p3.SEX = 'M' 
        p3._id = '3'     
        p4 = Person()
        p4.SEX = 'F'
        p4._id = '4'
        p5 = Person()
        p5.SEX = 'F'
        p5._id = '5'

        f1 = Family()
        f1.WIFE = '1'
        f2 = Family()
        f2.HUSB = '2'
        f3 = Family()
        f3.WIFE = '3'
        f4 = Family()
        f4.HUSB = '4'
        f5 = Family()
        f5.WIFE = '5'

        self.assertEqual(us21(p1, f1), False)
        self.assertEqual(us21(p2, f2), True)
        self.assertEqual(us21(p3, f3), False)
        self.assertEqual(us21(p4, f4), False)
        self.assertEqual(us21(p5, f5), True)

    def test15(self):
        us15p1 = Person()
        us15p2 = Person()
        us15p3 = Person()
        us15p4 = Person()
        us15p5 = Person()
        us15p6 = Person()
        us15p7 = Person()
        us15p8 = Person()
        us15p9 = Person()
        us15p10 = Person()
        us15p11 = Person()
        us15p12 = Person()
        us15p13 = Person()
        us15p14 = Person()
        us15p15 = Person()


        us15f1 = Family()
        fam = {"@F1@":us15f1}

        us15f1.CHIL.append(us15p1)
        self.assertEqual(childcheck(fam), True)

        us15f1.CHIL.append(us15p2)
        us15f1.CHIL.append(us15p3)
        us15f1.CHIL.append(us15p4)
        us15f1.CHIL.append(us15p5)
        us15f1.CHIL.append(us15p6)
        us15f1.CHIL.append(us15p7)
        self.assertEqual(childcheck(fam), True)

        us15f1.CHIL.append(us15p8)
        us15f1.CHIL.append(us15p9)
        us15f1.CHIL.append(us15p10)
        us15f1.CHIL.append(us15p11)
        us15f1.CHIL.append(us15p12)
        self.assertEqual(childcheck(fam), True)

        us15f1.CHIL.append(us15p13)
        us15f1.CHIL.append(us15p14)
        self.assertEqual(childcheck(fam), True)

        us15f1.CHIL.append(us15p15)
        self.assertEqual(childcheck(fam), False)
        