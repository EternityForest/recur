import recur_parser, recur
import datetime
import time as tt
from recur_dsl import *
from recur import *
p = recur_parser.UnknownParser()




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



class TestWeekdayOfMonth1stMonday(unittest.TestCase):
    def setUp(self):
        self.s = weekdayofmonth(1, 0)

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
    unittest.main()
