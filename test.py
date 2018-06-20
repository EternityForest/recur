#COPYRIGHT (c) 2016 Daniel Dunn

#GNU GENERAL PUBLIC LICENSE
#   Version 3, 29 June 2007

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.
import tatsu
import unittest
import recur
import recur.recur_parser
import datetime
import time as tt
from recur.recur_dsl import *
from recur.recur import *
p = recur_parser.parser




class Testbefore(unittest.TestCase):
    def setUp(self):
        self.d = getConstraint("before jun 20 2017")
    def test_not_there(self):
        x = self.d.after(datetime.datetime(2017,2,6,9,40))
        y= datetime.datetime(2017,2,6,9,40)
        self.assertEqual(x,y)
    def test_after(self):
        x = self.d.after(datetime.datetime(2017,10,6,9,40))
        y= None
        self.assertEqual(x,y)

class Testmidnight(unittest.TestCase):
    def setUp(self):
        self.d = getConstraint("at midnight")

    def test_not_there(self):
        x = self.d.after(datetime.datetime(2016,9,6,9,40))
        y= datetime.datetime(2017,9,7,0,00)
        self.assertEqual(x,y)



class Testmidnight(unittest.TestCase):
    def setUp(self):
        self.d = getConstraint("at midnight")

    def test_not_there(self):
        x = self.d.after(datetime.datetime(2016,9,6,9,40))
        y= datetime.datetime(2016,9,7,0,00)
        self.assertEqual(x,y)


class Testtimeofday(unittest.TestCase):
    def setUp(self):
        self.d = getConstraint("at 10am")

    def test_not_there(self):
        x = self.d.after(datetime.datetime(2016,9,6,9,40))
        y= datetime.datetime(2016,9,6,10,00)
        self.assertEqual(x,y)

class TestMonth(unittest.TestCase):
    def setUp(self):
        self.d = getConstraint("in february")
    def test_not_there(self):
        x = self.d.after(datetime.datetime(2016,1,6,9,40))
        y= datetime.datetime(2016,2,1,0,00)
        self.assertEqual(x,y)
    def test_before(self):
        x = self.d.before(datetime.datetime(2016,4,6,9,40))
        y= datetime.datetime(2016,2,1,0,00)
        self.assertEqual(x,y)
    def test_exclusive(self):
        x = self.d.after(datetime.datetime(2016,1,6,9,40),inclusive=False)
        y= datetime.datetime(2016,2,1,0,00)
        self.assertEqual(x,y)
    def test_end(self):
        x = self.d.end(datetime.datetime(2016,2,6,9,40),inclusive=False)
        y= datetime.datetime(2016,3,1,0,00)
        self.assertEqual(x,y)
        
class TestMonthUpper(unittest.TestCase):
    def setUp(self):
        self.d = getConstraint("February")
    def test_not_there(self):
        x = self.d.after(datetime.datetime(2016,1,6,9,40))
        y= datetime.datetime(2016,2,1,0,00)
        self.assertEqual(x,y)
    def test_before(self):
        x = self.d.before(datetime.datetime(2016,4,6,9,40))
        y= datetime.datetime(2016,2,1,0,00)
        self.assertEqual(x,y)
    def test_exclusive(self):
        x = self.d.after(datetime.datetime(2016,1,6,9,40),inclusive=False)
        y= datetime.datetime(2016,2,1,0,00)
        self.assertEqual(x,y)
    def test_end(self):
        x = self.d.end(datetime.datetime(2016,2,6,9,40),inclusive=False)
        y= datetime.datetime(2016,3,1,0,00)
        self.assertEqual(x,y)



class TestFiveMinutes(unittest.TestCase):
    def setUp(self):
        pass

    def test_almost(self):
        d= getConstraint("every five minutes")
        print(d.constraint,d.constraint.interval,d.align)
        x = d.after(datetime.datetime(2016,1,6  ,9,37))
        y= datetime.datetime(2016,1,6  ,9,40)
        self.assertEqual(x,y)


class Testsyntaxerrors(unittest.TestCase):
    def setUp(self):
        pass

    def test_syntax_error(self):
        try:
            getConstraint("every 5 minutes blah")
            self.assertTrue(False)
        except ValueError as e:
            print(e)
            self.assertTrue(True)

    def test_syntax_error(self):
        try:
            getConstraint("every 5 minuttes")
            self.assertTrue(False)
        except tatsu.exceptions.FailedParse as e:
            self.assertTrue(True)

class TestNthWeekdayOfMonth(unittest.TestCase):
    def setUp(self):
        self.d = getConstraint("every 3rd tuesday of the month")

    def test_not_there(self):
        x = self.d.after(datetime.datetime(2016,11,1,2,12))
        y= datetime.datetime(2016,11,15,0,0)
        self.assertEqual(x,y)

    def test_almost_there(self):
        x = self.d.after(datetime.datetime(2016,11,14,23,59,59,999999))
        y= datetime.datetime(2016,11,15,0,0)
        self.assertEqual(x,y)

    def test_before(self):
        x = self.d.before(datetime.datetime(2016,11,17,23,59,59,999999))
        y= datetime.datetime(2016,11,15,0,0)
        self.assertEqual(x,y)

    def test_end(self):
        x = self.d.end(datetime.datetime(2016,11,15,22,59,59,999999))
        y= datetime.datetime(2016,11,16,0,0)
        self.assertEqual(x,y)

    def test_end2(self):
        x = self.d.end(datetime.datetime(2016,11,15,2,53,5,9999))
        y= datetime.datetime(2016,11,16,0,0)
        self.assertEqual(x,y)
    def test_exc(self):
        x = self.d.after(datetime.datetime(2016,11,15,6,15),inclusive=False)
        y= datetime.datetime(2016,12,20,0,0)
        self.assertEqual(x,y)



class Testforminutes(unittest.TestCase):
    def setUp(self):
        self.d = getConstraint("every 5 minutes for 10 seconds")

    def test_not_there(self):
        x = self.d.after(datetime.datetime(2016,9,6,2,12))
        y= datetime.datetime(2016,9,6,2,15)
        self.assertEqual(x,y)

    def test_not_there2(self):
        x = self.d.after(datetime.datetime(2016,9,6,2,15))
        y= datetime.datetime(2016,9,6,2,15)
        self.assertEqual(x,y)

    def test_almost_there(self):
        x = self.d.after(datetime.datetime(2016,9,6,2,14,58,999999))
        y= datetime.datetime(2016,9,6,2,15)
        self.assertEqual(x,y)

    def test_almost_there2(self):
        x = self.d.after(datetime.datetime(2016,9,6,2,14,54,999999))
        y= datetime.datetime(2016,9,6,2,15)
        self.assertEqual(x,y)

    def test_already_there(self):
        x = self.d.after(datetime.datetime(2016,9,6,2,15,7))
        y= datetime.datetime(2016,9,6,2,15)
        self.assertEqual(x,y)

    def test_exclusive(self):
        x = self.d.after(datetime.datetime(2016,9,6,2,15),False)
        y= datetime.datetime(2016,9,6,2,20)
        self.assertEqual(x,y)

    def test_end(self):
        x = self.d.end(datetime.datetime(2016,9,6,2,15,6))
        y= datetime.datetime(2016,9,6,2,15,10)
        self.assertEqual(x,y)


class Testaligndatedaysuppercase(unittest.TestCase):
    def setUp(self):
        self.d = getConstraint("every 6 days starting on september 6 2016 at 2:15PM")

    def test_before_almost_there(self):
        x = self.d.before(datetime.datetime(2016,10,6,2,12))
        y= datetime.datetime(2016,9,6,2,15)
        self.assertEqual(x,y)


class Testaligndatedays(unittest.TestCase):
    def setUp(self):
        self.d = getConstraint("every 6 days starting on september 6 2016 at 2:15pm")

    def test_before_almost_there(self):
        x = self.d.before(datetime.datetime(2016,10,6,2,12))
        y= datetime.datetime(2016,9,6,2,15)
        self.assertEqual(x,y)


    def test_after_as_used_in_before_almost_there(self):
        x = self.d.after(datetime.datetime(2016,9,6,2,12)-datetime.timedelta(days=6))
        y= datetime.datetime(2016,9,6,2,15)
        self.assertEqual(x,y)


    def test_before_None(self):
        x = self.d.before(datetime.datetime(2016,9,5))
        y= None
        self.assertEqual(x,y)

    def test_before_None(self):
        x = self.d.before(datetime.datetime(2016,10,5))
        y= datetime.datetime(2016,9,6,2,15)
        self.assertEqual(x,y)

    def test_before_inside(self):
        x = self.d.before(datetime.datetime(2016,9,6,2,17))
        y= datetime.datetime(2016,9,6,2,15)
        self.assertEqual(x,y)

    def test_almost_there(self):
        x = self.d.after(datetime.datetime(2016,9,6,2,12))
        y= datetime.datetime(2016,9,6,2,15)
        self.assertEqual(x,y)

    def test_almost_there2(self):
        x = self.d.after(datetime.datetime(2016,9,8,1))
        y= datetime.datetime(2016,9,12,2,15)
        self.assertEqual(x,y)

    def test_not_there(self):
        x = self.d.after(datetime.datetime(2016,9,5,2,15))
        y= datetime.datetime(2016,9,6,2,15)
        self.assertEqual(x,y)

    def test_not_there2(self):
        x = self.d.after(datetime.datetime(2016,9,5,2,17))
        y= datetime.datetime(2016,9,6,2,15)
        self.assertEqual(x,y)

    def test_not_there3(self):
        x = self.d.after(datetime.datetime(2016,9,5,2,11))
        y= datetime.datetime(2016,9,6,2,15)
        self.assertEqual(x,y)

    def test_not_there4(self):
        x = self.d.after(datetime.datetime(2016,9,4,2,11))
        y= datetime.datetime(2016,9,6,2,15)
        self.assertEqual(x,y)

    def test_not_there5(self):
        x = self.d.after(datetime.datetime(2016,9,8,2,11))
        y= datetime.datetime(2016,9,12,2,15)
        self.assertEqual(x,y)

    def test_already_there(self):
        x = self.d.after(datetime.datetime(2016,9,6,2,15,7))
        y= datetime.datetime(2016,9,6,2,15)
        self.assertEqual(x,y)

    def test_exclusive(self):
        x = self.d.after(datetime.datetime(2016,9,6,2,15),False)
        y= datetime.datetime(2016,9,12,2,15)
        self.assertEqual(x,y)

    def test_end(self):
        x = self.d.end(datetime.datetime(2016,9,6,2,15,6))
        y= datetime.datetime(2016,9,7,2,15)
        self.assertEqual(x,y)


class Testaligndateminute(unittest.TestCase):
    def setUp(self):
        self.d = getConstraint("every minute starting on september 6 2016 at 2:15pm")

    def test_not_there(self):
        x = self.d.after(datetime.datetime(2016,9,6,2,14,59),False)
        y= datetime.datetime(2016,9,6,2,15)
        self.assertEqual(x,y)

    def test_exclusive(self):
        x = self.d.after(datetime.datetime(2016,9,6,2,15),False)
        y= datetime.datetime(2016,9,6,2,16)
        self.assertEqual(x,y)

    def test_end(self):
        x = self.d.end(datetime.datetime(2016,9,6,2,15,6))
        y= datetime.datetime(2016,9,6,2,16)
        self.assertEqual(x,y)

class Testaligndateminute2(unittest.TestCase):
    def setUp(self):
        self.d = getConstraint("every minute starting on september 6 2016 at 11:50pm")

    def test_not_there(self):
        x = self.d.after(datetime.datetime(2016,9,6,11,49,59),False)
        y= datetime.datetime(2016,9,6,11,50)
        self.assertEqual(x,y)

    def test_exclusive(self):
        x = self.d.after(datetime.datetime(2016,9,6,11,50),False)
        y= datetime.datetime(2016,9,6,11,51)
        self.assertEqual(x,y)

    def test_before(self):
        x = self.d.before(datetime.datetime(2016,9,6,11,55,6))
        y= datetime.datetime(2016,9,6,11,50)
        self.assertEqual(x,y)

    def test_end(self):
        x = self.d.end(datetime.datetime(2016,9,6,11,50,6))
        y= datetime.datetime(2016,9,6,11,51)
        self.assertEqual(x,y)

class Testaligndateminutes(unittest.TestCase):
    def setUp(self):
        self.d = getConstraint("every 5 minutes starting on september 6 2016 at 2:15pm")

    def test_not_there(self):
        x = self.d.after(datetime.datetime(2016,9,6,2,12))
        y= datetime.datetime(2016,9,6,2,15)
        self.assertEqual(x,y)

    def test_not_there2(self):
        x = self.d.after(datetime.datetime(2016,9,6,2,15))
        y= datetime.datetime(2016,9,6,2,15)
        self.assertEqual(x,y)

    def test_almost_there(self):
        x = self.d.after(datetime.datetime(2016,9,6,2,14,58,999999))
        y= datetime.datetime(2016,9,6,2,15)
        self.assertEqual(x,y)

    def test_almost_there2(self):
        x = self.d.after(datetime.datetime(2016,9,6,2,14,54,999999))
        y= datetime.datetime(2016,9,6,2,15)
        self.assertEqual(x,y)

    def test_already_there(self):
        x = self.d.after(datetime.datetime(2016,9,6,2,15,7))
        y= datetime.datetime(2016,9,6,2,15)
        self.assertEqual(x,y)

    def test_exclusive(self):
        x = self.d.after(datetime.datetime(2016,9,6,2,15),False)
        y= datetime.datetime(2016,9,6,2,20)
        self.assertEqual(x,y)

    def test_end(self):
        x = self.d.end(datetime.datetime(2016,9,6,2,15,6))
        y= datetime.datetime(2016,9,6,2,16)
        self.assertEqual(x,y)

class Testaligndatemonths3(unittest.TestCase):
    def setUp(self):
        self.d = getConstraint("every 3 months starting on august 6 2016 at 2:15pm")
        print("s",repr(self.d.constraint.constraints))
    def test_not_there(self):
        x = self.d.after(datetime.datetime(2016,7,2,1,9))
        y= datetime.datetime(2016,8,6,2,15)
        self.assertEqual(x,y)

    def test_already_there(self):
        x = self.d.after(datetime.datetime(2016,8,10,1,9))
        y= datetime.datetime(2016,8,6,2,15)
        self.assertEqual(x,y)

    def test_2(self):
        x = self.d.after(datetime.datetime(2016,9,2,7,34))
        y= datetime.datetime(2016,8,6,2,15)
        self.assertEqual(x,y)

    def test_almost_there(self):
        x = self.d.after(datetime.datetime(2016,9,6,2,14,58,999999))
        y= datetime.datetime(2016,8,6,2,15)
        self.assertEqual(x,y)

    def test_blah(self):
        x = self.d.after(datetime.datetime(2016,9,6,2,12,5))
        y= datetime.datetime(2016,8,6,2,15)
        self.assertEqual(x,y)

    def test_3(self):
        x = self.d.after(datetime.datetime(2016,9,6,2,10,5))
        y= datetime.datetime(2016,8,6,2,15)
        self.assertEqual(x,y)

    def test_almost(self):
        x = self.d.after(datetime.datetime(2016,9,6,2,14,59,999999))
        y= datetime.datetime(2016,8,6,2,15)
        self.assertEqual(x,y)

    def test_almost2(self):
        x = self.d.after(datetime.datetime(2016,12,6,2,14,59,999999))
        y= datetime.datetime(2016,11,6,2,15)
        self.assertEqual(x,y)

    def test_already_over(self):
        x = self.d.after(datetime.datetime(2016,9,27,1,7))
        y= datetime.datetime(2016,11,6,2,15)
        self.assertEqual(x,y)

    def test_exclusive(self):
        x = self.d.after(datetime.datetime(2016,8,12,1,9),False)
        y= datetime.datetime(2016,11,6,2,15)
        self.assertEqual(x,y)

    def test_end(self):
        x = self.d.end(datetime.datetime(2016,8,13,1,9))
        y= datetime.datetime(2016,9,6,2,15)
        self.assertEqual(x,y)


    def test_end_almost_there(self):
        x = self.d.end(datetime.datetime(2016,9,6,2,14,59,999999))
        y= datetime.datetime(2016,9,6,2,15)
        self.assertEqual(x,y)

    def test_end_almost_there2(self):
        x = self.d.end(datetime.datetime(2016,12,6,2,14,59,999999))
        y= datetime.datetime(2016,12,6,2,15)
        self.assertEqual(x,y)


class Testaligndatemonths1(unittest.TestCase):
    def setUp(self):
        self.d = getConstraint("every 1 months starting on august 6 2016 at 2:15pm")

    def test_1(self):
        x = self.d.after(datetime.datetime(2016,9,2,1,9))
        y= datetime.datetime(2016,8,6,2,15)
        self.assertEqual(x,y)

    def test_2(self):
        x = self.d.after(datetime.datetime(2016,9,2,7,34))
        y= datetime.datetime(2016,8,6,2,15)
        self.assertEqual(x,y)

    def test_almost_there(self):
        x = self.d.after(datetime.datetime(2016,9,6,2,14,58,999999))
        y= datetime.datetime(2016,8,6,2,15)
        self.assertEqual(x,y)

    def test_almost_there2(self):
        x = self.d.after(datetime.datetime(2016,9,6,2,12,5))
        y= datetime.datetime(2016,8,6,2,15)
        self.assertEqual(x,y)

    def test_almost_there3(self):
        x = self.d.after(datetime.datetime(2016,9,6,2,10,5))
        y= datetime.datetime(2016,8,6,2,15)
        self.assertEqual(x,y)

    def test_almost_over(self):
        x = self.d.after(datetime.datetime(2016,10,6,2,14,59,999999))
        y= datetime.datetime(2016,9,6,2,15)
        self.assertEqual(x,y)

    def test_almost_over2(self):
        x = self.d.after(datetime.datetime(2016,10,6,2,14,59,999999))
        y= datetime.datetime(2016,9,6,2,15)
        self.assertEqual(x,y)

    def test_already_there(self):
        x = self.d.after(datetime.datetime(2016,9,27,1,7))
        y= datetime.datetime(2016,9,6,2,15)
        self.assertEqual(x,y)

    def test_exclusive(self):
        x = self.d.after(datetime.datetime(2016,9,27,1,9),False)
        y= datetime.datetime(2016,10,6,2,15)
        self.assertEqual(x,y)

    def test_end(self):
        x = self.d.end(datetime.datetime(2016,9,2,1,9))
        y= datetime.datetime(2016,9,6,2,15)
        self.assertEqual(x,y)


    def test_end_almost_there(self):
        x = self.d.end(datetime.datetime(2016,9,6,2,14,59,999999))
        y= datetime.datetime(2016,9,6,2,15)
        self.assertEqual(x,y)

    def test_end_almost_there2(self):
        x = self.d.end(datetime.datetime(2016,10,6,2,14,59,999999))
        y= datetime.datetime(2016,10,6,2,15)
        self.assertEqual(x,y)

class Testaligndate(unittest.TestCase):
    def setUp(self):
        self.d = getConstraint("every 1 weeks starting on september 6 2016")

    def test(self):
        x = self.d.after(datetime.datetime(2016,9,26,1,9))
        y= datetime.datetime(2016,9,20)
        self.assertEqual(x,y)

    def test2(self):
        x = self.d.after(datetime.datetime(2016,9,25,1,9))
        y= datetime.datetime(2016,9,20)
        self.assertEqual(x,y)

    def test3(self):
        x = self.d.after(datetime.datetime(2016,9,27,1,7))
        y= datetime.datetime(2016,9,27)
        self.assertEqual(x,y)

    def test4(self):
        x = self.d.after(datetime.datetime(2016,9,26,23,59))
        y= datetime.datetime(2016,9,20)
        self.assertEqual(x,y)

    def test_almost_over(self):
        x = self.d.after(datetime.datetime(2016,9,26,23,59,59,999999))
        y= datetime.datetime(2016,9,20)
        self.assertEqual(x,y)

    def test_exclusive(self):
        x = self.d.after(datetime.datetime(2016,9,27,1,9),False)
        y= datetime.datetime(2016,10,4)
        self.assertEqual(x,y)

    def test_end(self):
        x = self.d.end(datetime.datetime(2016,9,26,1,9))
        y= datetime.datetime(2016,9,27)
        self.assertEqual(x,y)

class Testalign(unittest.TestCase):
    def setUp(self):
        self.d = getConstraint("every 1 weeks starting on tuesday")

    def test(self):
        x = self.d.after(datetime.datetime(2016,9,26,1,9))
        y= datetime.datetime(2016,9,20)
        self.assertEqual(x,y)

    def test2(self):
        x = self.d.after(datetime.datetime(2016,9,25,1,9))
        y= datetime.datetime(2016,9,20)
        self.assertEqual(x,y)

    def test3(self):
        x = self.d.after(datetime.datetime(2016,9,27,1,7))
        y= datetime.datetime(2016,9,27)
        self.assertEqual(x,y)

    def test_exclusive(self):
        x = self.d.after(datetime.datetime(2016,9,27,1,9),False)
        y= datetime.datetime(2016,10,4)
        self.assertEqual(x,y)

    def test_end(self):
        x = self.d.end(datetime.datetime(2016,9,26,1,9))
        y= datetime.datetime(2016,9,27)
        self.assertEqual(x,y)

class Teststringweeks(unittest.TestCase):
    def setUp(self):
        self.d = getConstraint("every 1 weeks")

    def test(self):
        x = self.d.after(datetime.datetime(2016,9,28,1,9))
        y= datetime.datetime(2016,9,26)
        self.assertEqual(x,y)

    def test2(self):
        x = self.d.after(datetime.datetime(2016,10,3,1,9))
        y= datetime.datetime(2016,10,3)
        self.assertEqual(x,y)

    def test4(self):
        x = self.d.after(datetime.datetime(2016,10,3,1,7))
        y= datetime.datetime(2016,10,3)
        self.assertEqual(x,y)

    def test_exclusive(self):
        x = self.d.after(datetime.datetime(2016,10,3,1,9),False)
        y= datetime.datetime(2016,10,10)
        self.assertEqual(x,y)

class Testonweekday(unittest.TestCase):
    def setUp(self):
        self.d = getConstraint("on thursday")

    def test_not_there(self):
        x = self.d.after(datetime.datetime(2016,9,28,1,9))
        y= datetime.datetime(2016,9,29)
        self.assertEqual(x,y)


class Teststringweekdays(unittest.TestCase):
    def setUp(self):
        self.d = getConstraint("every thursday")

    def test_not_there(self):
        x = self.d.after(datetime.datetime(2016,9,28,1,9))
        y= datetime.datetime(2016,9,29)
        self.assertEqual(x,y)

    def test_not_there2(self):
        x = self.d.after(datetime.datetime(2016,9,27,1,9))
        y= datetime.datetime(2016,9,29)
        self.assertEqual(x,y)

    def test_already_there(self):
        x = self.d.after(datetime.datetime(2016,9,29,1,9))
        y= datetime.datetime(2016,9,29)
        self.assertEqual(x,y)

    def test_exclusive(self):
        x = self.d.after(datetime.datetime(2016,9,29,1,9),False)
        y= datetime.datetime(2016,10,6)
        self.assertEqual(x,y)


class Teststringmonths(unittest.TestCase):
    def setUp(self):
        self.d = getConstraint("every 3 months")

    def test_not_there(self):
        x = self.d.after(datetime.datetime(2015,1,1,1,9))
        y= datetime.datetime(2015,3,1)
        self.assertEqual(x,y)

    def test_not_there_2(self):
        x = self.d.after(datetime.datetime(2015,2,1))
        y= datetime.datetime(2015,3,1)
        self.assertEqual(x,y)

    def test_already_there(self):
        x = self.d.after(datetime.datetime(2015,3,1))
        y= datetime.datetime(2015,3,1)
        self.assertEqual(x,y)



class TestStringMonthDay(unittest.TestCase):
    def setUp(self):
        self.d= getConstraint("on the 3rd day of the month")

    def test_not_there(self):
        x = self.d.after(datetime.datetime(2015,9,1,0,3))
        y= datetime.datetime(2015,9,3)
        self.assertEqual(x,y)


    def test_already_there(self):
        x = self.d.after(datetime.datetime(2015,9,3))
        y= datetime.datetime(2015,9,3)
        self.assertEqual(x,y)


    def test_past(self):
        x = self.d.after(datetime.datetime(2015,11,7))
        y= datetime.datetime(2015,12,3)
        self.assertEqual(x,y)

    def test_exclusive(self):
        x = self.d.after(datetime.datetime(2015,9,3,5),inclusive=False)
        y= datetime.datetime(2015,10,3)
        self.assertEqual(x,y)


class TestStringMonthDays(unittest.TestCase):
    def setUp(self):
        self.d= getConstraint("on the 3rd and 4th day of the month")

    def test_not_there(self):
        x = self.d.after(datetime.datetime(2015,9,1,0,3))
        y= datetime.datetime(2015,9,3)
        self.assertEqual(x,y)


    def test_already_there(self):
        x = self.d.after(datetime.datetime(2015,9,3))
        y= datetime.datetime(2015,9,3)
        self.assertEqual(x,y)


    def test_already_there2(self):
        x = self.d.after(datetime.datetime(2015,11,4))
        y= datetime.datetime(2015,11,4)
        self.assertEqual(x,y)

    def test_past(self):
        x = self.d.after(datetime.datetime(2015,11,7))
        y= datetime.datetime(2015,12,3)
        self.assertEqual(x,y)

    def test_exclusive(self):
        x = self.d.after(datetime.datetime(2015,9,4,5),inclusive=False)
        y= datetime.datetime(2015,10,3)
        self.assertEqual(x,y)


class TestStringMonthDays2(unittest.TestCase):
    def setUp(self):
        self.d= getConstraint("on the 28th, 27th, and 14th day of the month")

    def test_not_there(self):
        x = self.d.after(datetime.datetime(2015,9,10,0,3))
        y= datetime.datetime(2015,9,14)
        self.assertEqual(x,y)


    def test_already_there(self):
        x = self.d.after(datetime.datetime(2015,9,14))
        y= datetime.datetime(2015,9,14)
        self.assertEqual(x,y)


    def test_already_there2(self):
        x = self.d.after(datetime.datetime(2015,11,14))
        y= datetime.datetime(2015,11,14)
        self.assertEqual(x,y)

    def test_past(self):
        x = self.d.after(datetime.datetime(2015,11,29))
        y= datetime.datetime(2015,12,14)
        self.assertEqual(x,y)

    def test_exclusive(self):
        x = self.d.after(datetime.datetime(2015,10,14),inclusive=False)
        y= datetime.datetime(2015,10,27)
        self.assertEqual(x,y)


class TestString5min(unittest.TestCase):
    def setUp(self):
        self.d= getConstraint("every 5 minutes")

    def test_not_there(self):
        #That'sa tue, we want next wed
        x = self.d.after(datetime.datetime(2015,9,2,0,3))
        y= datetime.datetime(2015,9,2,0,5)
        self.assertEqual(x,y)


    def test_already_there(self):
        #That'sa wed, we want next wed
        x = self.d.after(datetime.datetime(2015,9,9,0,5))
        y= datetime.datetime(2015,9,9,0,5)
        self.assertEqual(x,y)



class Test5secs(unittest.TestCase):
    def setUp(self):
        self.d= secondly(5)

    def test_not_there(self):
        x = self.d.after(datetime.datetime(2015,9,2,2,2,3))
        y= datetime.datetime(2015,9,2,2,2,5)
        self.assertEqual(x,y)

    def test_already_there(self):
        x = self.d.after(datetime.datetime(2015,9,9,6,5,5))
        y= datetime.datetime(2015,9,9,6,5,5)
        self.assertEqual(x,y)

    def test_exclusive(self):
        x = self.d.after(datetime.datetime(2015,9,2,6,5,5),inclusive=False)
        y= datetime.datetime(2015,9,2,6,5,10)
        self.assertEqual(x,y)

    def test_end(self):
        x = self.d.end(datetime.datetime(2015,9,2, 5,5,5))
        y= datetime.datetime(2015,9,2, 5,5,6)
        self.assertEqual(x,y)

class Test5mins(unittest.TestCase):
    def setUp(self):
        self.d= minutely(5)

    def test_not_there(self):
        x = self.d.after(datetime.datetime(2015,9,2,2,2))
        y= datetime.datetime(2015,9,2,2,5)
        self.assertEqual(x,y)

    def test_already_there(self):
        x = self.d.after(datetime.datetime(2015,9,9,6,5))
        y= datetime.datetime(2015,9,9,6,5)
        self.assertEqual(x,y)

    def test_exclusive(self):
        x = self.d.after(datetime.datetime(2015,9,2,6,5),inclusive=False)
        y= datetime.datetime(2015,9,2,6,10)
        self.assertEqual(x,y)

    def test_end(self):
        x = self.d.end(datetime.datetime(2015,9,2, 5,5))
        y= datetime.datetime(2015,9,2, 5,6)
        self.assertEqual(x,y)

class Test6Hours(unittest.TestCase):
    def setUp(self):
                self.d= hourly(6)

    def test_not_there(self):
        x = self.d.after(datetime.datetime(2015,9,2,2))
        y= datetime.datetime(2015,9,2,6)
        self.assertEqual(x,y)

    def test_already_there(self):
        x = self.d.after(datetime.datetime(2015,9,9,6))
        y= datetime.datetime(2015,9,9,6)
        self.assertEqual(x,y)

    def test_exclusive(self):
        x = self.d.after(datetime.datetime(2015,9,2,6),inclusive=False)
        y= datetime.datetime(2015,9,2,12)
        self.assertEqual(x,y)

    def test_end(self):
        x = self.d.end(datetime.datetime(2015,9,2,6))
        y= datetime.datetime(2015,9,2,7)
        self.assertEqual(x,y)

class TestDOWConstraintWed(unittest.TestCase):
    def setUp(self):
                self.d = weekday([2])

    def test_not_there(self):
        x = self.d.after(datetime.datetime(2015,9,1,1,9))
        y= datetime.datetime(2015,9,2)
        self.assertEqual(x,y)

    def test_not_there_2(self):
        x = self.d.after(datetime.datetime(2015,8,29))
        y= datetime.datetime(2015,9,2)
        self.assertEqual(x,y)

    def test_already_there(self):
        x = self.d.after(datetime.datetime(2015,9,9,5,34))
        y= datetime.datetime(2015,9,9)
        self.assertEqual(x,y)

    def test_end(self):
        x = self.d.end(datetime.datetime(2015,9,2,1,9))
        y= datetime.datetime(2015,9,3)
        self.assertEqual(x,y)

class TestDOWConstraintMondayTuesday(unittest.TestCase):
    def setUp(self):
        self.d = weekday([0,1])

    def test_monday_start(self):
        x = self.d.after(datetime.datetime(2015,9,7,1,9))
        y= datetime.datetime(2015,9,7)
        self.assertEqual(x,y)

    def test_tuesday_start(self):
        x = self.d.after(datetime.datetime(2015,9,1))
        y= datetime.datetime(2015,9,1)
        self.assertEqual(x,y)

    def test_wedensday_start(self):
        x = self.d.after(datetime.datetime(2015,9,10,5,34))
        y= datetime.datetime(2015,9,14)
        self.assertEqual(x,y)

    def test_end_already_there(self):
        x = self.d.end(datetime.datetime(2015,9,2,1,9))
        y= datetime.datetime(2015,9,2)
        self.assertEqual(x,y)

class TestDOMConstraint1(unittest.TestCase):
    def setUp(self):
        self.d = monthday([1])

    def test_not_there(self):
        x = self.d.after(datetime.datetime(2015,9,6,1,9))
        y= datetime.datetime(2015,10,1)
        self.assertEqual(x,y)

    def test_not_there_2(self):
        x = self.d.after(datetime.datetime(2015,8,29))
        y= datetime.datetime(2015,9,1)
        self.assertEqual(x,y)

    def test_already_there(self):
        x = self.d.after(datetime.datetime(2015,9,1,5,34))
        y= datetime.datetime(2015,9,1)
        self.assertEqual(x,y)

    def test_end(self):
        x = self.d.end(datetime.datetime(2015,9,1,1,9))
        y= datetime.datetime(2015,9,2)
        self.assertEqual(x,y)

    def test_end_already_there(self):
        x = self.d.end(datetime.datetime(2015,9,2,1,9))
        y= datetime.datetime(2015,9,2)
        self.assertEqual(x,y)

class TestDOMConstraint1and3(unittest.TestCase):
    def setUp(self):
        self.d = monthday([1,3])

    def test_not_there(self):
        x = self.d.after(datetime.datetime(2015,9,6,1,9))
        y= datetime.datetime(2015,10,1)
        self.assertEqual(x,y)

    def test_not_there_2(self):
        x = self.d.after(datetime.datetime(2015,8,2))
        y= datetime.datetime(2015,8,3)
        self.assertEqual(x,y)

    def test_already_there(self):
        x = self.d.after(datetime.datetime(2015,9,3,5,34))
        y= datetime.datetime(2015,9,3)
        self.assertEqual(x,y)

class TestDOYConstraint(unittest.TestCase):
    def setUp(self):
        self.d = yearday([5, 10])

    def test_not_there(self):
        x = self.d.after(datetime.datetime(2015,1,1,1,9))
        y= datetime.datetime(2015,1,5)
        self.assertEqual(x,y)

    def test_not_there_2(self):
        x = self.d.after(datetime.datetime(2015,1,6,8,5))
        y= datetime.datetime(2015,1,10)
        self.assertEqual(x,y)

    def test_already_there(self):
        x = self.d.after(datetime.datetime(2015,1,5,5,34))
        y= datetime.datetime(2015,1,5)
        self.assertEqual(x,y)



class Test(unittest.TestCase):
    def setUp(self):
        self.d = monthly(3)

    def test_not_there(self):
        x = self.d.after(datetime.datetime(2015,1,1,1,9))
        y= datetime.datetime(2015,3,1)
        self.assertEqual(x,y)

    def test_not_there_2(self):
        x = self.d.after(datetime.datetime(2015,2,1))
        y= datetime.datetime(2015,3,1)
        self.assertEqual(x,y)

    def test_already_there(self):
        x = self.d.after(datetime.datetime(2015,3,1))
        y= datetime.datetime(2015,3,1)
        self.assertEqual(x,y)


class Testhour(unittest.TestCase):
    def setUp(self):
        self.d = hour([5, 10])

    def test_not_there(self):
        x = self.d.after(datetime.datetime(2015,1,1,1,9))
        y= datetime.datetime(2015,1,1,5)
        self.assertEqual(x,y)

    def test_not_there_2(self):
        x = self.d.after(datetime.datetime(2015,1,1,8,5))
        y= datetime.datetime(2015,1,1,10)
        self.assertEqual(x,y)

    def test_already_there(self):
        x = self.d.after(datetime.datetime(2015,1,1,5,34))
        y= datetime.datetime(2015,1,1,5)
        self.assertEqual(x,y)

class TestOredhour(unittest.TestCase):
    def setUp(self):
        self.d = hour([5]) | hour([10])

    def test_not_there(self):
        x = self.d.after(datetime.datetime(2015,1,1,1,9))
        y= datetime.datetime(2015,1,1,5)
        self.assertEqual(x,y)

    def test_not_there_2(self):
        x = self.d.after(datetime.datetime(2015,1,1,8,5))
        y= datetime.datetime(2015,1,1,10)
        self.assertEqual(x,y)

    def test_already_there(self):
        x = self.d.after(datetime.datetime(2015,1,1,5,34))
        y= datetime.datetime(2015,1,1,5)
        self.assertEqual(x,y)


class TestConstraintSystem(unittest.TestCase):
    def setUp(self):
        #Constraint system for finding days that are thursday and the third of the month
        self.s = ConstraintSystem(datetime.datetime(2015,9,1,5,34))
        self.s.addConstraint( monthday([3]))
        self.s.addConstraint(weekday([3]))

    def test_not_there(self):
        x = self.s.next()
        y= datetime.datetime(2015,9,3)
        self.assertEqual(x,y)

        x = self.s.next()
        y= datetime.datetime(2015,12,3)
        self.assertEqual(x,y)

class TestANDConstraint(unittest.TestCase):
    def setUp(self):
        #Constraint system for finding days that are thursday and the third of the month
        self.s =  monthday([3]) & weekday([3])

    def test_not_there(self):
        x = self.s.after(datetime.datetime(2015,9,1,5,34))
        y= datetime.datetime(2015,9,3)
        self.assertEqual(x,y)

        x = self.s.after(datetime.datetime(2015,9,4,5,34))
        y= datetime.datetime(2015,12,3)
        self.assertEqual(x,y)

class TestMinutelyConstraint(unittest.TestCase):
    def setUp(self):
        #Constraint system for finding days that are thursday and the third of the month
        self.s = minutely(1)

    def test_inclusive(self):
        x = self.s.after(datetime.datetime(2015,9,1,5,34))
        y= datetime.datetime(2015,9,1,5,34)
        self.assertEqual(x,y)

    def test_exclusive(self):
        x = self.s.after(datetime.datetime(2015,9,1,5,34), False)
        y= datetime.datetime(2015,9,1,5,35)
        self.assertEqual(x,y)

class TestTime(unittest.TestCase):
    def setUp(self):
        #Constraint system for finding days that are thursday and the third of the month
        self.s = time(8,30)

    def test_sameday(self):
        x = self.s.after(datetime.datetime(2015,9,1,5,34,5))
        y= datetime.datetime(2015,9,1,8,30)
        self.assertEqual(x,y)

    def test_nextday(self):
        x = self.s.after(datetime.datetime(2015,9,1,9,34,5))
        y= datetime.datetime(2015,9,2,8,30)
        self.assertEqual(x,y)

    def test_exclusive(self):
        x = self.s.after(datetime.datetime(2015,9,1,8,30), False)
        y= datetime.datetime(2015,9,2,8,30)
        self.assertEqual(x,y)



class TestNthWeekdayConstraint1stMonday(unittest.TestCase):
    def setUp(self):
        self.s = NthWeekdayConstraint(1, 0)

    def test_not_there(self):
        x = self.s.after(datetime.datetime(2015,9,1,5,34,5))
        y= datetime.datetime(2015,9,7)
        self.assertEqual(x,y)

    def test_already_there(self):
        x = self.s.after(datetime.datetime(2015,9,7))
        y= datetime.datetime(2015,9,7)
        self.assertEqual(x,y)

    def test_next_month(self):
        x = self.s.after(datetime.datetime(2015,9,10,5,34,5))
        y= datetime.datetime(2015,10,5)
        self.assertEqual(x,y)

    def test_next_year(self):
        x = self.s.after(datetime.datetime(2015,12,8,5,34,5))
        y= datetime.datetime(2016,1,4)
        self.assertEqual(x,y)

    def test_exclusive(self):
        x = self.s.after(datetime.datetime(2015,9,7,5,34,17), False)
        y= datetime.datetime(2015,10,5)
        self.assertEqual(x,y)

    def test_end(self):
        x = self.s.end(datetime.datetime(2015,9,7,5,34,17))
        y= datetime.datetime(2015,9,8)
        self.assertEqual(x,y)

    def test_end_not_in(self):
        x = self.s.end(datetime.datetime(2015,10,10,5,34,17))
        y= datetime.datetime(2015,10,10,5,34,17)
        self.assertEqual(x,y)

class TestgetNthWeekday(unittest.TestCase):
    def test_1(self):
        x =getNthWeekday(1,0,datetime.datetime(2015,9,1))
        y= datetime.datetime(2015,9,7)
        self.assertEqual(x,y)

unittest.main()


if __name__ == '__main__':
    import cProfile, pstats, io
    pr = cProfile.Profile()
    pr.enable()
    t = tt.time()
    c = getConstraint("every 2 months every 5 minutes")
    dt = datetime.datetime(2011,5,8)
    for i in range(0,1000):
        c.after(dt)
        #dt += +datetime.timedelta(days=7)
    print("1000 iterations of 'every 2 months every 5 minutes' in "+str((tt.time()-t)*1000)+"us per iteration")

    t = tt.time()
    c = getConstraint(" every 7 minutes")
    dt = datetime.datetime(2011,5,8)
    for i in range(0,1000):
        c.after(dt)
        #dt += +datetime.timedelta(days=7)
    print("1000 iterations of 'every 7 minutes' in "+str((tt.time()-t)*1000)+"us per iteration")


    t = tt.time()
    c = getConstraint(" every 7 minutes every 15 months")
    dt = datetime.datetime(2011,5,8)
    for i in range(0,1000):
        c.after(dt)
        #dt += +datetime.timedelta(days=7)
    print("1000 iterations of 'every 7 minutes every 15 months' in "+str((tt.time()-t)*1000)+"us per iteration")

    t = tt.time()
    c = getConstraint(" every 7 minutes every 40 minutes")
    dt = datetime.datetime(2011,5,8)
    for i in range(0,1000):
        c.after(dt)
        #dt += +datetime.timedelta(days=7)
    print("1000 iterations of 'every 7 minutes every 40 minutes' in "+str((tt.time()-t)*1000)+"us per iteration")

    t = tt.time()
    c = getConstraint("every 20 minutes every sunday and tuesday")
    dt = datetime.datetime(2011,5,8)
    for i in range(0,1000):
        c.after(dt)
        #dt += +datetime.timedelta(days=7)
    print("1000 iterations of 'every 20 minutes every sunday and tuesday' in "+str((tt.time()-t)*1000)+"us per iteration")


    pr.disable()
    s = io.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print (s.getvalue())
