import recur_parser, recur
import datetime
p = recur_parser.UnknownParser()


def parseDateTimeWithYearWithDefaults(s):
    "This accepts lots and lots of default options for no real reason other than to handle the starting at alignments"
    t = s.time
    d = s.date
    #Handles things like every 2 weeks starting on monday
    if s.weekday:
        return datetime.datetime.fromordinal(1+parseWeekday(s.weekday))
    return datetime.datetime(
     year=int(d.year) if d and d.year else 1,
     month=parseMonth(d.month) if d and d.month else 1,
     day= int(d.dayofmonth) if d and d.dayofmonth else 1,
     minute=int(t.minute) if t and t.minute else 0,
     hour = int(t.hour) if t and t.hour else 0,
     second=int(t.second) if t and t.second else 0,
     microsecond=int(t.millisecond)*1000 if t and t.millisecond else 0)

def parseOrdinal(s):
    "Given either an int or a string like '1', '1st','10th', etc; return an int"
    o = {'other':2,"first":1,"1st":1,"second":2,"2nd":2,"third":3,"3rd":3}
    if s in o:
        return o[s]
    if s.endswith("th"):
        return(int(s[:-2]))
    return(int(s))

def parseTime(s):
    "Given the AST for a strng like 4:45pm, return a datetime.time"
    return datetime.time(
    int(s.hour)+ (12 if s.ampm =="pm" else 0), int(s.minute) if s.minute else 0, int(s.second) if s.second else 0, s.ms*1000 if s.ms else 0)

def parseWeekday(s):
    return{
    "mon":0, "monday":0,
    "tue":1, "tuesday":1,
    "wed":2, "wednesday":2,
    "thu": 3, "thurs": 3,"thursday":3,
    "fri":4, "friday":4,
    'sat':5,"saturday":5,
    "sun":6,"sunday":6
    }[s.lower()]

def parseMonth(s):
    return{
    "jan":1, "january":1,
    "feb":2, "february":2,
    "mar":3, "march":3,
    "apr":4, "april":1,
    "may":5,
    "jun":6, "june":6,
    "jul":7, "july":7,
    "aug":8, "august":8,
    "sep":9, "september":9,
    "oct":10, "october":10,
    "nov":11, "november":11,
    "dec":12, "december":12
    }[s.lower()]

class semantics():
    "Each function here handles a rule in the PEG. Rules are handled bottom up"
    def nintervalconstraint(self, ast):
        n = parseOrdinal(ast[1])
        i = ast[2]
        return {
        "minute" : recur.minutely,
        "minutes" : recur.minutely,

        "hour" : recur.hourly,
        "hours" : recur.hourly,

        "day" : recur.daily,
        "days" : recur.daily,

        "second" : recur.secondly,
        "seconds" : recur.secondly,

        "month" : recur.monthly,
        "months" : recur.monthly,

        "year" : recur.yearly,
        "years" : recur.yearly,

        "week": recur.weekly,
        "weeks": recur.weekly
        }[i](n)

    def startingat(self,ast):
        self.align = parseDateTimeWithYearWithDefaults(ast)

    def constraint_list(self, ast):
        x = ast
        c = x.pop()
        while x:
            c = c & x.pop()
        return c

    def and_constraint(self, ast):
        x = ast['allof']
        c = x.pop()
        while x:
            c = c | x.pop()
        return c

    def betweentimesofdayconstraint(self,ast):
        s = parseTime(ast[0])
        e = parseTime(ast[1])
        #Start before end means range does not cross midnight
        if s<e:
            return recur.aftertime(s) & recur.beforetime(e)
        else:
            #To deal with ranges that cross midnight, we say things from 6 till midnight OR from midnight till 3am
            return recur.aftertime(s) | recur.beforetime(e)

    def yeardayconstraint(self, ast):
        return recur.yearday(parseOrdinal(ast[1]))

    def monthdayconstraint(self,ast):
        l = []
        for i in ast:
            l.append(parseOrdinal(i))
        return recur.monthday(l)

    def weekdayconstraint(self,ast):
        l = []
        for i in ast:
            l.append(parseWeekday(i))
        return recur.weekday(l)

d = datetime.datetime(2016,9,26)

def getConstraint(c):
    s = semantics()
    c= p.parse(c, rule_name="start",semantics =s )
    a = s.align if hasattr(s,"align") else None
    return recur.Selector(c, a)
