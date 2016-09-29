import datetime,unittest


def incrementByWeek(dt):
    dt = dt+dat
def list_or_int(t):
    if isinstance(t,list):
        return t
    else:
        return [t]
def timeFromArgs(*args):
    if isinstance(args[0], datetime.time):
        return args[0]
    else:
        return datetime.time(*args)

def dt_to_unix(dt):
    return (dt - datetime.datetime(1970, 1, 1)).total_seconds()

def asMinutes(dt):
    return dt.minute+dt.hour*60+ (dt.toordinal()*24*60)

def asHours(dt):
    return dt.hour + dt.toordinal()*24

def asMonths(dt):
    return dt.month + dt.year*12

def asYears(dt):
    return  dt.year

def asWeeks(dt):
    return dt.toordinal()//7

def dayOfYear(d):
    "Given a datetime, get the day of year"
    s = d.replace(day=1, hour=0,minute=0, second=0)
    diff = d-s
    return diff.days+1

class BaseConstraint():
    "This is the base class for all constraints and constraint systems"
    def __init__(self):
        #Self.sort is the average time between matches.
        #It's purpose is to improve efficiency and should never beneeded for correctness
        self.sort = 0

    def __or__(self,other):
        return ORConstraint(self, other)

    def __and__(self,other):
        c = ConstraintSystem()
        c.addConstraint(self)
        c.addConstraint(other)
        return c

    def next(self, inclusive=False):
        self.time = self.after(self.time, inclusive)
        return self.time

    def setTime(self,time):
        self.time = time

class ORConstraint(BaseConstraint):
    """Constraint that represents any time that is matched by constraint a or b.
    Even if times overlap, both shall be considered two separate matches."""

    def __init__(self, a, b):
        self.sort = a.sort if a.sort < b.sort else b.sort
        self.a = a
        self.b = b

    def after(self, time, inclusive=True):
        a = self.a.after(time, inclusive)
        b = self.b.after(time, inclusive)
        return (a if a<b else b)




class ConstraintSystem(BaseConstraint):
    """Class defining one event that repeats at times determined by a set of constraints,
        each one of which must be an object with one required method next(t, inclusive), which
        must return the first time after t as a datetime that matches the constraint.

        if inclusive is true, then if t itself matches, then t or else the start of the matching period t is in
        must be returned.

        If there are no future matches, None must be returned.

        By calling setTime(t) on the constraint system and then calling next repeatedly, one
        can get the next time that matches all constraints.'

        Can be ANDed and ORed together just like a normal constraint.
    """

    def __and__(self,other):
        c = ConstraintSystem()
        for i in self.constraints:
            c.addConstraint(i)
        c.addConstraint(other)
        return c

    def __rand__(self,other):
        c = ConstraintSystem()
        for i in self.constraints:
            c.add(i)
        c.addConstraint(other)
        return c

    def __init__(self, time=None):
        BaseConstraint.__init__(self)
        if not time:
            self.time = datetime.datetime.now()
        self.time = time
        self.constraints = []

    def addConstraint(self,c):
        if self.sort < c.sort:
            self.sort = c.sort
        self.constraints.append(c)
        #Constraints all tell us what their average distance between matches is.
        #This lets us do the bigger ones first.
        self.constraints.sort(key=lambda x: x.sort, reverse=True)

    def match(self,time):
        for i in self.constraints:
            if not i.after(time) <= time:
                return False
            else:
                return True

    def after(self,  time, inclusive=True,align=None):
        #Loop over n constraints n times
        if time==None:
            return None
        #If we want the next one and this one, then loop through all the constraints
        #and find the one that has the soonest next time and start looking from there
        if not inclusive:
            smallest = datetime.timedelta(days=99999)
            for i in self.constraints:
                x = i.after(time, False,align)
                #If any constraint does not have a next, the whole system has no next, so return None
                if not x:
                    return None
                smallest = min(smallest, x-time)

            #increment time to the first matching constraint
            time += smallest

        for i in range(0,500):
            #This gets set to false at the first non-match of an iteration
            x = True
            #For each constraint, get the next occurance after our current time.
            #If the time is not equal to the current time, then this time is not the next occurance of the total system.
            for i in self.constraints:
                #Get either next occurance or start of this occurance
                t = i.after(time,True,align)
                #We check if time is less than or equal to t because constraints return the start of
                #A time period if the time given is within an occurance if inclusive is true
                if not t<=time:
                    x = False
                #time is a var that only moves forwar until we find one that matches everything. Moving backwards
                #Would make an infinite loop in some cases
                if t > time:
                    time = t
                #If any constraint has no next, return None
                if time==None:
                    return None
            if x:
                return time
        raise RuntimeError("Could not satisfy constraints in 500 iterations: "+repr(self.constraints))



    def end(self,  time,align=None):
        #Loop over n constraints n times
        if time==None:
            return None
        #If we want the next one and this one, then loop through all the constraints
        #and find the one that has the soonest next time and start looking from there
        if not inclusive:
            smallest = datetime.timedelta(days=99999)
            for i in self.constraints:
                x = i.end(time, False,align)
                if not x:
                    return None
                smallest = min(smallest, x-time)

        time += smallest

        for i in range(0,250):
            x = True
            for i in self.constraints:
                t = time
                time = i.end(t,align)
                if not time==t:
                    x = False

                if time==None:
                    return None
            if x:
                break

        return time


class weekday(BaseConstraint):
    "Match one day or list of days in every week"
    def __init__(self,day):
        "day must be a list of days of the week as numbers where mon=0 that match the constraint"
        self.day = set(list_or_int(day))
        self.sort = (7*24*60*60)/len(self.day)

    def after(self,dt, inclusive=True,align=None):
        if not(self.day):
            return None

        if not inclusive:
            dt= dt+datetime.timedelta(days=1)

        while(1):
            if dt.weekday() in self.day:
                return dt.replace(hour=0, minute=0,second=0, microsecond=0)
            else:
                dt= dt+datetime.timedelta(days=1)

    def end(self, dt):
        if not dt.weekday() in self.day:
            return dt.replace(hour=0, minute=0,second=0, microsecond=0)
        else:
            return (dt+datetime.timedelta(days=1)).replace(hour=0, minute=0,second=0, microsecond=0)

class hour(BaseConstraint):
    "Match one hour or a list of hours in every day"
    def __init__(self,hour):
        "hour must be an integer in 24 hour time or an iterable of such integers. Matches the entire hour"
        self.hour = set(list_or_int(hour))
        self.sort = (24*60*60)/len(self.hour)

    def after(self,dt, inclusive=True,align=None):
        if not(self.hour):
            return None

        if not inclusive:
            dt= dt + datetime.timedelta(hours=1)

        while(1):
            if dt.hour in self.hour:
                return dt.replace(minute=0,second=0, microsecond=0)
            else:
                dt= dt+datetime.timedelta(hours=1)

    def end(self,dt):
        if not(self.hour):
            return dt

        while(1):
            if not dt.hour in self.hour:
                return dt.replace(minute=0,second=0, microsecond=0)
            else:
                dt= dt+datetime.timedelta(hours=1)

class time(BaseConstraint):
    "Match one exact moment in every day"
    def __init__(self,*time):
        "Match a specific time of day. Arguments must be the same as would be used for datetime.time"
        self.time = timeFromArgs(*time)
        self.sort = 24*60*60

    def after(self,dt, inclusive=True,align=None):
        if not inclusive:
            dt= dt + datetime.timedelta(hours=1)

        if not dt.time() > self.time:
            return dt.replace(hour=self.time.hour, minute=self.time.minute, second=self.time.second, microsecond=self.time.microsecond)
        else:
            return (dt+datetime.timedelta(days=1)).replace(hour=self.time.hour, minute=self.time.minute, second=self.time.second, microsecond=self.time.microsecond)

    def end(dt):
        #Times are one moment in time that don't have any duration
        return dt

class aftertime(BaseConstraint):
    "Match a range of time that ends at midnight in every day"
    def __init__(self,*time):
        "Match any time betweem specific time of day and midnight. Arguments must be the same as would be used for datetime.time"
        self.time = timeFromArgs(*time)
        self.sort = 24*60*60

    def __repr__(self):
        return "<aftertime "+str(self.time)+">"

    def after(self,dt, inclusive=True,align=None):
        #If it is after the time return current if we are inclusive
        if dt.time() >= self.time:
            if inclusive:
                return dt.replace(hour=self.time.hour, minute=self.time.minute, second=self.time.second, microsecond=self.time.microsecond)
        if dt.time() < self.time:
            return dt.replace(hour=self.time.hour, minute=self.time.minute, second=self.time.second, microsecond=self.time.microsecond)
        else:
            return (dt+datetime.timedelta(days=1)).replace(hour=self.time.hour, minute=self.time.minute, second=self.time.second, microsecond=self.time.microsecond)

    def end(dt):
        return (dt+datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)


class beforetime(BaseConstraint):
    "Match a range of time that begins at midnight in every day"
    def __init__(self,*time):
        "Arguments must be the same as would be used for datetime.time"
        self.time = timeFromArgs(*time)
        self.sort = 24*60*60
    def __repr__(self):
        return "<beforetime "+str(self.time)+">"
    def after(self,dt, inclusive=True,align=None):
        #If it is after the time return current if we are inclusive
        if dt.time() <= self.time:
            if inclusive:
                return dt.replace(hour=0, minute=0, second=0, microsecond=0)
        #Return midnight that starts tomorrow
        return (dt+datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)

    def end(dt):
        t = self.time
        #Just return the specified time today
        return dt.replace(hour=self.time.hour, minute=self.time.minute, second=self.time.second, microsecond=self.time.microsecond)


#By Duncan of stackoverflow
def monthdelta(date, delta):
    "Add delta months to date"
    m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
    if not m: m = 12
    d = min(date.day, [31,
        29 if y%4==0 and not y%400==0 else 28,31,30,31,30,31,31,30,31,30,31][m-1])
    return date.replace(day=d,month=m, year=y)




class yearly(BaseConstraint):
    "Matches every Nth hour"
    def __init__(self,interval=1):
        "Match every nth year"
        self.interval = interval
        self.sort = interval*60*60*24*365

    def after(self,dt, inclusive=True, align = None ):
        #Get how far past a multiple of the correct number  the first occurance was.
        #That is our offset, when we Subtract that fron the current time, it should give the right result.
        #Say if we are going every 10min, but we start at minute 7, we subtract 7, so that minute 7 maps to 0 and matches m%10
        align = align.year if align else 0
        #Subtract align from minute so that at align minutes we are at 0 in our offset timespace
        dt_offset = dt.year - (align%(self.interval))

        if inclusive and (dt_offset) % self.interval == 0:

            #Get start of month. Return the actual time not our offset version
            return dt.replace(microsecond=0,second=0,minute=0,hour=0,day=1,month=1)
        else:
            #Increment to next match. We modulo the second of the current time with the interval,
            #Then subtract the result from the interval to get the time left in this interval
            #We do all this in our offset time space.
            #Since the offset space is a constant factor away from real time, deltas valid in one are valid in the other.

            return dt.replace(microsecond=0,second=0,minute=0,hour=0,day=1,month=1, year = dt.year+self.interval-((dt_offset) % self.interval))

    def end(self,dt,align=None):
        #Get start of minute. we already know we are in a match because that is a precondition of end
        #So we just increment the minute
        return dt.replace(microsecond=0,second=0,minute=0,hour=0,day=1,month=1,year=dt.year+1)



class monthly(BaseConstraint):
    "Matches every Nth hour"
    def __init__(self,interval=1):
        "Match every nth month"
        self.interval = interval
        self.sort = interval*60*60*24*30*12

    def after(self,dt, inclusive=True, align = None):
        #Get how far past a multiple of the correct number  the first occurance was.
        #That is our offset, when we Subtract that fron the current time, it should give the right result.
        #Say if we are going every 10min, but we start at minute 7, we subtract 7, so that minute 7 maps to 0 and matches m%10

        align =asMonths(align) if align else 0

        #Subtract align from minute so that at align minutes we are at 0 in our offset timespace
        dt_offset = asMonths(dt) - (align%(self.interval))

        if inclusive and (dt_offset) % self.interval == 0:

            #Get start of hour. Return the actual time not our offset version
            return dt.replace(microsecond=0,second=0,minute=0,hour=0,day=1)
        else:
            #Increment to next match. We modulo the second of the current time with the interval,
            #Then subtract the result from the interval to get the time left in this interval
            #We do all this in our offset time space.
            #Since the offset space is a constant factor away from real time, deltas valid in one are valid in the other.

            dt = monthdelta(dt, self.interval-((dt_offset) % self.interval))
            return dt.replace(microsecond=0,second=0,minute=0,hour=0,day=1)

    def end(self,dt,align=None):
        #Get start of minute. we already know we are in a match because that is a precondition of end
        #So we just increment the minute
        return monthdelta(dt.replace(microsecond=0,second=0,minute=0,hour=0,day=1),1)


class weeks(BaseConstraint):
    """Matches every nth weeks, defaulting to 1 for every week"""
    def __init__(self,interval=1):
        self.interval = interval
        self.sort = (24*60*60)

    def after(self, dt, inclusive=True,align=None):
        if align:
            dt = dt.replace(day= dt.day-dt.weekday(), hour=0, minute=0, second=0,microsecond=0)
        if not inclusive:
            dt= dt + datetime.timedelta(days=self.interval*7)
        else:
            return dt

    def end(self, dt,align=None):
        if align:
            dt = dt.replace(day= dt.day-dt.weekday(), hour=0, minute=0, second=0,microsecond=0)

        return dt + datetime.timedelta(days=self.interval*7)



class minutely(BaseConstraint):
    "Matches every Nth minute."
    def __init__(self,interval=1):
        "Match every nth second"
        self.interval = interval
        self.sort = interval*60

    def after(self,dt, inclusive=True, align = 0):
        #Get how far past a multiple of the correct number  the first occurance was.
        #That is our offset, when we Subtract that fron the current time, it should give the right result.
        #Say if we are going every 10min, but we start at minute 7, we subtract 7, so that minute 7 maps to 0 and matches m%10
        align =asMinutes(align) if align else 0

        #Subtract align from minute so that at align units we are at 0 in our offset timespace
        dt_offset = asMinutes(dt) - (align%(self.interval))

        if inclusive and (dt_offset) % self.interval == 0:
            #Get start of hour. Return the actual time not our offset version
            return dt.replace(microsecond=0,second=0)
        else:
            #Increment to next match. We modulo the second of the current time with the interval,
            #Then subtract the result from the interval to get the time left in this interval
            #We do all this in our offset time space.
            #Since the offset space is a constant factor away from real time, deltas valid in one are valid in the other.

            dt += datetime.timedelta(minutes=self.interval-((dt_offset) % self.interval))
            return dt.replace(microsecond=0,second=0)

    def end(self,dt,align=None):
        #Get start of minute. we already know we are in a match because that is a precondition of end
        #So we just increment the minute
        return dt.replace(microsecond=0,second=0)+  datetime.timedelta(minutes=1)

class secondly(BaseConstraint):
    "Matches every Nth hour"
    def __init__(self,interval=1):
        "Match every nth second"
        self.interval = interval
        self.sort = interval

    def after(self,dt, inclusive=True, align = None):
        #Get how far past a multiple of the correct number  the first occurance was.
        #That is our offset, when we Subtract that fron the current time, it should give the right result.
        #Say if we are going every 10min, but we start at minute 7, we subtract 7, so that minute 7 maps to 0 and matches m%10
        align =dt_to_unix(align) if align else 0

        #Subtract align from minute so that at align minutes we are at 0 in our offset timespace
        dt_offset = dt_to_unix(dt) - (align%(self.interval))

        if inclusive and (dt_offset) % self.interval == 0:
            #Get start of hour. Return the actual time not our offset version
            return dt.replace(microsecond=0)
        else:
            #Increment to next match. We modulo the second of the current time with the interval,
            #Then subtract the result from the interval to get the time left in this interval
            #We do all this in our offset time space.
            #Since the offset space is a constant factor away from real time, deltas valid in one are valid in the other.

            dt += datetime.timedelta(seconds=self.interval-((dt_offset) % self.interval))
            return dt.replace(microsecond=0)

    def end(self,dt,align=None):
        #Get start of minute. we already know we are in a match because that is a precondition of end
        #So we just increment the minute
        return dt.replace(microsecond=0)+  datetime.timedelta(seconds=1)

class hourly(BaseConstraint):
    "Matches every Nth hour"
    def __init__(self,interval=1):
        "Match every nth second"
        self.interval = interval
        self.sort = interval*60*60

    def after(self,dt, inclusive=True, align = None):
        #Get how far past a multiple of the correct number of minutes the first occurance was.
        #That is our offset, when we Subtract that fron the current time, it should give the right result.
        #Say if we are going every 10min, but we start at minute 7, we subtract 7, so that minute 7 maps to 0 and matches m%10
        align =asHours(align) if align else 0

        #Subtract align from minute so that at align minutes we are at 0 in our offset timespace
        dt_offset = asHours(dt) - (align%(self.interval))

        if inclusive and (dt_offset) % self.interval == 0:
            #Subtract align from minute so that at align minutes
            #Get start of hour. Return the actual time not our offset version
            return dt.replace(microsecond=0,second=0,minute=0)
        else:
            #Increment to next match. We modulo the hour of the current time with the interval,
            #Then subtract the result from the interval to get the time left in this interval
            #We do all this in our offset time space.
            #Since the offset space is a constant factor away from real time, deltas valid in one are valid in the other.

            dt += datetime.timedelta(hours=self.interval-((dt_offset) % self.interval))
            return dt.replace(microsecond=0,second=0,minute=0)

    def end(self,dt,align=None):
        #Get start of minute. we already know we are in a match because that is a precondition of end
        #So we just increment the minute
        return dt.replace(microsecond=0,second=0, minute=0)+  datetime.timedelta(hours=1)


class daily(BaseConstraint):
    "Matches every Nth hour"
    def __init__(self,interval=1):
        "Match every nth second"
        self.interval = interval
        self.sort = interval*60*60*24

    def after(self,dt, inclusive=True, align = None):
        #Get how far past a multiple of the correct number of minutes the first occurance was.
        #That is our offset, when we Subtract that fron the current time, it should give the right result.
        #Say if we are going every 10min, but we start at minute 7, we subtract 7, so that minute 7 maps to 0 and matches m%10
        align =align.toordinal() if align else 0

        #Subtract align from minute so that at align minutes we are at 0 in our offset timespace
        dt_offset = dt.toordinal() - (align%(self.interval))

        if inclusive and (dt_offset) % self.interval == 0:
            #Get start of hour. Return the actual time not our offset version
            return dt.replace(microsecond=0,second=0,minute=0,hour=0)
        else:
            #Increment to next match. We modulo the hour of the current time with the interval,
            #Then subtract the result from the interval to get the time left in this interval
            #We do all this in our offset time space.
            #Since the offset space is a constant factor away from real time, deltas valid in one are valid in the other.

            dt += datetime.timedelta(days=self.interval-((dt_offset) % self.interval))
            return dt.replace(microsecond=0,second=0,minute=0,hour=0)

    def end(self,dt,align=None):
        #Get start of minute. we already know we are in a match because that is a precondition of end
        #So we just increment the minute
        return dt.replace(microsecond=0,second=0, minute=0,hours=0)+  datetime.timedelta(days=1)


class monthday(BaseConstraint):
    "Match one day or list of days in every month, such as the 12th of every month."
    def __init__(self,day):
        self.day = sorted(list_or_int(day))
        self.sort = (24*30*60*60)/len(self.day)

    def after(self,dt, inclusive=True,align=None):
        if not self.day:
            return None

        if not inclusive:
            dt= dt+datetime.timedelta(days=1)

        #If we are past the last in the list of matching days
        if dt.day > self.day[-1]:
            while 1:
                dt = dt.replace(day=self.day[0], hour=0, minute=0,second=0, microsecond=0)
                #Monthdelta saturates at the last day of the month o=if the current day is higher than next month has in days.
                #So, we have to keep checking until we find a matching month
                dt = monthdelta(dt,1)
                if dt.day == self.day[0]:
                    return dt

        #Just increment by day until we find a match
        while(1):
            if dt.day in self.day:
                return dt.replace(hour=0, minute=0,second=0, microsecond=0)
            else:
                dt= dt+datetime.timedelta(days=1)

    def end(self,dt):
        if not self.day:
            return dt

        while(1):
            if not dt.day in self.day:
                return dt.replace(hour=0, minute=0,second=0, microsecond=0)
            else:
                dt= dt+datetime.timedelta(days=1)


def getNthWeekday(n, day, dt):
    "Get the nth weekday in the month that dt is in"
    #The start of month
    som = dt.replace(day=1, hour=0, minute=0,second=0, microsecond=0)
    dt =  dt.replace(hour=0, minute=0,second=0, microsecond=0)

    #Get the weekday of the first of the month
    somwd = som.weekday()

    #Get the days until the next of the specified weekday from the start of the month
    days_till_next_match = day-somwd
    #If we already passed the first weekday we are looking for this month, then increment by 7
    #To get the next one after the one last month
    if days_till_next_match<0:
        days_till_next_match +=7

    #get the first of whatever weekday you specified in that month

    #Add 7 days times n(minus one because we start at the first matching weekday)
    #To get the one we want
    t = som+datetime.timedelta(days=days_till_next_match+(7*(n-1)))

    #if we already went over the limit
    if not t.month == dt.month:
        return None
    else:
        return t

class weekdayofmonth(BaseConstraint):
    "Match the nth weekday of a month, such as first tuesday or third sunday"
    def __init__(self,n, weekday):
        self.n = n
        self.weekday = weekday
        self.sort = 30*24*60*60

    def after(self, dt, inclusive=True,align=None):
        dt = dt.replace(hour=0,minute=0,second=0, microsecond=0)
        if not inclusive:
            dt+= datetime.timedelta(days=1)
        dt2 = dt
        for i in range(12):
            m = getNthWeekday(self.n,self.weekday,dt2)
            if not m or m<dt:
                if dt.month <12:
                    dt2 = dt2.replace(month=dt.month+1)
                else:
                    dt2 = dt2.replace(year=dt.year+1, month=1)
                continue
            else:
                return m

    def end(self, dt):
        if not dt.replace(hour=0,minute=0,second=0, microsecond=0) == getNthWeekday(self.n,self.weekday,dt):
            return dt
        else:
           return (dt+datetime.timedelta(days=1)).replace(hour=0,minute=0,second=0, microsecond=0)

class date(BaseConstraint):
    "Match a specific day of the year, given as a month and day"
    def __init__(self,month, day):
        self.day = day
        self.month = month
        self.sort = (24*365*60*60)

    def after(self,dt, inclusive=True,align=None):
        if not inclusive:
            dt= dt+datetime.timedelta(days=1)

        while(1):
            if dayOfYear(dt) in self.day:
                return dt.replace(hour=0, minute=0,second=0, microsecond=0)
            else:
                dt= dt+datetime.timedelta(days=1)

    def end(self,dt):
        if not self.day:
            return dt

        while(1):
            if not dayOfYear(dt) in self.day:
                return dt.replace(hour=0, minute=0,second=0, microsecond=0)
            else:
                dt= dt+datetime.timedelta(days=1)




class yearday(BaseConstraint):
    "Match a day of the year given as a number"
    def __init__(self,day):
        self.day = set(list_or_int(day))
        self.sort = (24*365*60*60)/len(self.day)

    def after(self,dt, inclusive=True,align=None):
        if not self.day:
            return None

        if not inclusive:
            dt= dt+datetime.timedelta(days=1)

        while(1):
            if dayOfYear(dt) in self.day:
                return dt.replace(hour=0, minute=0,second=0, microsecond=0)
            else:
                dt= dt+datetime.timedelta(days=1)

    def end(self,dt):
        if not self.day:
            return dt

        while(1):
            if not dayOfYear(dt) in self.day:
                return dt.replace(hour=0, minute=0,second=0, microsecond=0)
            else:
                dt= dt+datetime.timedelta(days=1)
