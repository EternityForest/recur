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
grammar = """
@@left_recursion :: False
start =and_constraint [syntax_error];
#Basic stuff to do with how constraints are combined
atomic_constraint = intervalconstraint|nintervalconstraint|startingat|nthweekdayconstraint|weekdayconstraint|
                    monthdayconstraint|betweentimesofdayconstraint|yeardayconstraint|
                    timeofdayconstraint|aftertimeofdayconstraint|
                    ('(' and_constraint ')')|except_constraint;

syntax_error = /[.\w]+/;
constraint_list = {atomic_constraint}+;
and_constraint = allof+:constraint_list {['and'] allof+:constraint_list} ["for" for:(integer (interval|intervals))];
except_constraint = 'except' atomic_constraint;


#Data types
timeinterval = number ("seconds" | "minutes" |"hours" | "days" | "weeks");
number = /\d+[\.]\d+/;
integer = /\d+/;
ordinal = 'first'|'second'|'third'|'1st'|'2nd'|'3rd'|'other'|/\d\d?th/;

#If it looks like 02:45, assume 24 hour time.
time = (hour:hour [[(':' minute:minute) [(':' second:second) [(':' ms:millisecond)]]]] ampm:('am'|'pm'))|(hour:hour ':' minute:minute [[(':' second:second) [(':' ms:millisecond)]]]);
times = {times:time [',']['and']}+;
hour = /\d\d?/;
minute = /\d\d/;
second = /\d\d/;
millisecond = /\d\d\d\d/;
year = /\d\d\d\d/;
month = 'jan'|'january'|'feb'|'february'|'mar'|'march'|'apr'|'april'|'may'|'jun'|'june'|'jul'|'july'|'aug'|'august'|'sep'|
        'september'| 'nov'| 'november'|'dec'|'december';
dayofmonth = ordinal| /\d\d?/;
date = (month:month dayofmonth:dayofmonth) | (dayofmonth:dayofmonth month:month) | ('the' dayofmonth:dayofmonth 'of' month:month);
dates = {@+:date ','|"and"|/, +and/}+;
datewithyear = (month:month dayofmonth:dayofmonth year:year) | (dayofmonth:dayofmonth month:month year:year);
datetime = (time:time date:date)| (time:time 'on' date:date) | (date:date 'at' time:time);
datetimewithyear = (time:time date:datewithyear)| (time:time 'on' date:datewithyear) | (date:datewithyear 'at' time:time )| date:datewithyear;
timeofdayrange = ('between' time 'and' time)| ('from' time 'to' time)| (time 'to' time);
interval = 'week'|'month'|'year'|'day'|'hour'|'minute'|'second'|'ms'|'millisecond';
intervals = 'weeks'|'months'|'years'|'days'|'hours'|'minutes'|'seconds'|'ms'|'milliseconds';
weekday = 'mon'|'monday'|'tue'|'tuesday'|'wed'|'wednesday'|'thu'|'thursday'|'fri'|'friday'|'sat'|'saturday'|'sun'|'sunday';

#actual constraints
timeofdayconstraint = ['at'] timeofdayconstraint:times;
aftertimeofdayconstraint = 'after' aftertimeofdayconstraint:time;
betweentimesofdayconstraint = ('between' @+:time 'and' @+:time)| ('from' @+:time 'to' @+:time);
nintervalconstraint = ('every' integer intervals) | ('every' ordinal interval);
intervalconstraint = ('every' interval);
dateconstraint = (["on"] dates) | ('every year on') date;
datewithyearconstraint = (["on"] datewithyear);
yeardayconstraint = "on the " ordinal "day of the year";
monthdayconstraint = "on the"  @+:ordinal {[','] @+:ordinal} [[',']'and'  @+:ordinal] ["day of the month"];
weekdayconstraint  = ['every'] @+:weekday {[','] @+:weekday} [[',']'and'  @+:weekday];
nthweekdayconstraint = ('the'|'on the'|'every') @+:ordinal @+:weekday 'of the month';

#Directives
startingat = ("starting" ['at'|'on'] @:datetimewithyear) |"starting on" weekday:weekday;

#constants
predefinedtime = "noon"| "midnight";
"""

parser = tatsu.compile(grammar)
