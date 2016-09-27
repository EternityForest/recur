import recur_parser, recur
import datetime
p = recur_parser.UnknownParser()

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

class semantics():
    "Each function here handles a rule in the PEG. Rules are handled bottom up"
    def nintervalconstraint(self, ast):
        n = parseOrdinal(ast[1])
        i = ast[2]
        return {
        "minutes" : recur.minutely
        }[i](n)

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


d = datetime.datetime(2016,9,26)
def getConstraint(c):
    return p.parse(c, rule_name="start",semantics = semantics())
