#!/usr/bin/env python
# -*- coding: utf-8 -*-

# CAVEAT UTILITOR
#
# This file was automatically generated by Grako.
#
#    https://pypi.python.org/pypi/grako/
#
# Any changes you make to it will be overwritten the next time
# the file is generated.


from __future__ import print_function, division, absolute_import, unicode_literals

from grako.buffering import Buffer
from grako.parsing import graken, Parser
from grako.util import re, RE_FLAGS, generic_main  # noqa


__all__ = [
    'UnknownParser',
    'UnknownSemantics',
    'main'
]

KEYWORDS = set([])


class UnknownBuffer(Buffer):
    def __init__(
        self,
        text,
        whitespace=None,
        nameguard=None,
        comments_re=None,
        eol_comments_re=None,
        ignorecase=None,
        namechars='',
        **kwargs
    ):
        super(UnknownBuffer, self).__init__(
            text,
            whitespace=whitespace,
            nameguard=nameguard,
            comments_re=comments_re,
            eol_comments_re=eol_comments_re,
            ignorecase=ignorecase,
            namechars=namechars,
            **kwargs
        )


class UnknownParser(Parser):
    def __init__(
        self,
        whitespace=None,
        nameguard=None,
        comments_re=None,
        eol_comments_re=None,
        ignorecase=None,
        left_recursion=True,
        parseinfo=True,
        keywords=None,
        namechars='',
        buffer_class=UnknownBuffer,
        **kwargs
    ):
        if keywords is None:
            keywords = KEYWORDS
        super(UnknownParser, self).__init__(
            whitespace=whitespace,
            nameguard=nameguard,
            comments_re=comments_re,
            eol_comments_re=eol_comments_re,
            ignorecase=ignorecase,
            left_recursion=left_recursion,
            parseinfo=parseinfo,
            keywords=keywords,
            namechars=namechars,
            buffer_class=buffer_class,
            **kwargs
        )

    @graken()
    def _start_(self):
        self._and_constraint_()
        with self._optional():
            self._syntax_error_()

    @graken()
    def _atomic_constraint_(self):
        with self._choice():
            with self._option():
                self._forconstraint_()
            with self._option():
                self._intervalconstraint_()
            with self._option():
                self._nintervalconstraint_()
            with self._option():
                self._startingat_()
            with self._option():
                self._nthweekdayconstraint_()
            with self._option():
                self._weekdayconstraint_()
            with self._option():
                self._monthdayconstraint_()
            with self._option():
                self._betweentimesofdayconstraint_()
            with self._option():
                self._yeardayconstraint_()
            with self._option():
                self._timeofdayconstraint_()
            with self._option():
                self._aftertimeofdayconstraint_()
            with self._option():
                with self._group():
                    self._token('(')
                    self._and_constraint_()
                    self._token(')')
            with self._option():
                self._except_constraint_()
            self._error('no available options')

    @graken()
    def _syntax_error_(self):
        self._pattern(r'[.\w]+')

    @graken()
    def _constraint_list_(self):

        def block0():
            self._atomic_constraint_()
        self._positive_closure(block0)

    @graken()
    def _and_constraint_(self):
        self._constraint_list_()
        self.add_last_node_to_name('allof')

        def block1():
            with self._optional():
                self._token('and')
            self._constraint_list_()
            self.add_last_node_to_name('allof')
        self._closure(block1)
        self.ast._define(
            [],
            ['allof']
        )

    @graken()
    def _except_constraint_(self):
        self._token('except')
        self._atomic_constraint_()

    @graken()
    def _forconstraint_(self):
        self._atomic_constraint_()
        self._token('for')
        self._integer_()
        with self._group():
            with self._choice():
                with self._option():
                    self._interval_()
                with self._option():
                    self._intervals_()
                self._error('no available options')

    @graken()
    def _timeinterval_(self):
        self._number_()
        with self._group():
            with self._choice():
                with self._option():
                    self._token('seconds')
                with self._option():
                    self._token('minutes')
                with self._option():
                    self._token('hours')
                with self._option():
                    self._token('days')
                with self._option():
                    self._token('weeks')
                self._error('expecting one of: days hours minutes seconds weeks')

    @graken()
    def _number_(self):
        self._pattern(r'\d+[\.]\d+')

    @graken()
    def _integer_(self):
        self._pattern(r'\d+')

    @graken()
    def _ordinal_(self):
        with self._choice():
            with self._option():
                self._token('first')
            with self._option():
                self._token('second')
            with self._option():
                self._token('third')
            with self._option():
                self._token('1st')
            with self._option():
                self._token('2nd')
            with self._option():
                self._token('3rd')
            with self._option():
                self._token('other')
            with self._option():
                self._pattern(r'\d\d?th')
            self._error('expecting one of: 1st 2nd 3rd \\d\\d?th first other second third')

    @graken()
    def _time_(self):
        with self._choice():
            with self._option():
                with self._group():
                    self._hour_()
                    self.name_last_node('hour')
                    with self._optional():
                        with self._optional():
                            with self._group():
                                self._token(':')
                                self._minute_()
                                self.name_last_node('minute')
                            with self._optional():
                                with self._group():
                                    self._token(':')
                                    self._second_()
                                    self.name_last_node('second')
                                with self._optional():
                                    with self._group():
                                        self._token(':')
                                        self._millisecond_()
                                        self.name_last_node('ms')
                    with self._group():
                        with self._choice():
                            with self._option():
                                self._token('am')
                            with self._option():
                                self._token('pm')
                            self._error('expecting one of: am pm')
                    self.name_last_node('ampm')
            with self._option():
                with self._group():
                    self._hour_()
                    self.name_last_node('hour')
                    self._token(':')
                    self._minute_()
                    self.name_last_node('minute')
                    with self._optional():
                        with self._optional():
                            with self._group():
                                self._token(':')
                                self._second_()
                                self.name_last_node('second')
                            with self._optional():
                                with self._group():
                                    self._token(':')
                                    self._millisecond_()
                                    self.name_last_node('ms')
            self._error('no available options')
        self.ast._define(
            ['ampm', 'hour', 'minute', 'ms', 'second'],
            []
        )

    @graken()
    def _times_(self):

        def block0():
            self._time_()
            self.name_last_node('times')
            with self._optional():
                self._token(',')
            with self._optional():
                self._token('and')
        self._positive_closure(block0)
        self.ast._define(
            ['times'],
            []
        )

    @graken()
    def _hour_(self):
        self._pattern(r'\d\d?')

    @graken()
    def _minute_(self):
        self._pattern(r'\d\d')

    @graken()
    def _second_(self):
        self._pattern(r'\d\d')

    @graken()
    def _millisecond_(self):
        self._pattern(r'\d\d\d\d')

    @graken()
    def _year_(self):
        self._pattern(r'\d\d\d\d')

    @graken()
    def _month_(self):
        with self._choice():
            with self._option():
                self._token('jan')
            with self._option():
                self._token('january')
            with self._option():
                self._token('feb')
            with self._option():
                self._token('february')
            with self._option():
                self._token('mar')
            with self._option():
                self._token('march')
            with self._option():
                self._token('apr')
            with self._option():
                self._token('april')
            with self._option():
                self._token('may')
            with self._option():
                self._token('jun')
            with self._option():
                self._token('june')
            with self._option():
                self._token('jul')
            with self._option():
                self._token('july')
            with self._option():
                self._token('aug')
            with self._option():
                self._token('august')
            with self._option():
                self._token('sep')
            with self._option():
                self._token('september')
            with self._option():
                self._token('nov')
            with self._option():
                self._token('november')
            with self._option():
                self._token('dec')
            with self._option():
                self._token('december')
            self._error('expecting one of: apr april aug august dec december feb february jan january jul july jun june mar march may nov november sep september')

    @graken()
    def _dayofmonth_(self):
        with self._choice():
            with self._option():
                self._ordinal_()
            with self._option():
                self._pattern(r'\d\d?')
            self._error('expecting one of: \\d\\d?')

    @graken()
    def _date_(self):
        with self._choice():
            with self._option():
                with self._group():
                    self._month_()
                    self.name_last_node('month')
                    self._dayofmonth_()
                    self.name_last_node('dayofmonth')
            with self._option():
                with self._group():
                    self._dayofmonth_()
                    self.name_last_node('dayofmonth')
                    self._month_()
                    self.name_last_node('month')
            with self._option():
                with self._group():
                    self._token('the')
                    self._dayofmonth_()
                    self.name_last_node('dayofmonth')
                    self._token('of')
                    self._month_()
                    self.name_last_node('month')
            self._error('no available options')
        self.ast._define(
            ['dayofmonth', 'month'],
            []
        )

    @graken()
    def _dates_(self):

        def block0():
            with self._choice():
                with self._option():
                    self._date_()
                    self.add_last_node_to_name('@')
                    self._token(',')
                with self._option():
                    self._token('and')
                with self._option():
                    self._pattern(r', +and')
                self._error('expecting one of: , +and and')
        self._positive_closure(block0)

    @graken()
    def _datewithyear_(self):
        with self._choice():
            with self._option():
                with self._group():
                    self._month_()
                    self.name_last_node('month')
                    self._dayofmonth_()
                    self.name_last_node('dayofmonth')
                    self._year_()
                    self.name_last_node('year')
            with self._option():
                with self._group():
                    self._dayofmonth_()
                    self.name_last_node('dayofmonth')
                    self._month_()
                    self.name_last_node('month')
                    self._year_()
                    self.name_last_node('year')
            self._error('no available options')
        self.ast._define(
            ['dayofmonth', 'month', 'year'],
            []
        )

    @graken()
    def _datetime_(self):
        with self._choice():
            with self._option():
                with self._group():
                    self._time_()
                    self.name_last_node('time')
                    self._date_()
                    self.name_last_node('date')
            with self._option():
                with self._group():
                    self._time_()
                    self.name_last_node('time')
                    self._token('on')
                    self._date_()
                    self.name_last_node('date')
            with self._option():
                with self._group():
                    self._date_()
                    self.name_last_node('date')
                    self._token('at')
                    self._time_()
                    self.name_last_node('time')
            self._error('no available options')
        self.ast._define(
            ['date', 'time'],
            []
        )

    @graken()
    def _datetimewithyear_(self):
        with self._choice():
            with self._option():
                with self._group():
                    self._time_()
                    self.name_last_node('time')
                    self._datewithyear_()
                    self.name_last_node('date')
            with self._option():
                with self._group():
                    self._time_()
                    self.name_last_node('time')
                    self._token('on')
                    self._datewithyear_()
                    self.name_last_node('date')
            with self._option():
                with self._group():
                    self._datewithyear_()
                    self.name_last_node('date')
                    self._token('at')
                    self._time_()
                    self.name_last_node('time')
            with self._option():
                self._datewithyear_()
                self.name_last_node('date')
            self._error('no available options')
        self.ast._define(
            ['date', 'time'],
            []
        )

    @graken()
    def _timeofdayrange_(self):
        with self._choice():
            with self._option():
                with self._group():
                    self._token('between')
                    self._time_()
                    self._token('and')
                    self._time_()
            with self._option():
                with self._group():
                    self._token('from')
                    self._time_()
                    self._token('to')
                    self._time_()
            with self._option():
                with self._group():
                    self._time_()
                    self._token('to')
                    self._time_()
            self._error('no available options')

    @graken()
    def _interval_(self):
        with self._choice():
            with self._option():
                self._token('week')
            with self._option():
                self._token('month')
            with self._option():
                self._token('year')
            with self._option():
                self._token('day')
            with self._option():
                self._token('hour')
            with self._option():
                self._token('minute')
            with self._option():
                self._token('second')
            with self._option():
                self._token('ms')
            with self._option():
                self._token('millisecond')
            self._error('expecting one of: day hour millisecond minute month ms second week year')

    @graken()
    def _intervals_(self):
        with self._choice():
            with self._option():
                self._token('weeks')
            with self._option():
                self._token('months')
            with self._option():
                self._token('years')
            with self._option():
                self._token('days')
            with self._option():
                self._token('hours')
            with self._option():
                self._token('minutes')
            with self._option():
                self._token('seconds')
            with self._option():
                self._token('ms')
            with self._option():
                self._token('milliseconds')
            self._error('expecting one of: days hours milliseconds minutes months ms seconds weeks years')

    @graken()
    def _weekday_(self):
        with self._choice():
            with self._option():
                self._token('mon')
            with self._option():
                self._token('monday')
            with self._option():
                self._token('tue')
            with self._option():
                self._token('tuesday')
            with self._option():
                self._token('wed')
            with self._option():
                self._token('wednesday')
            with self._option():
                self._token('thu')
            with self._option():
                self._token('thursday')
            with self._option():
                self._token('fri')
            with self._option():
                self._token('friday')
            with self._option():
                self._token('sat')
            with self._option():
                self._token('saturday')
            with self._option():
                self._token('sun')
            with self._option():
                self._token('sunday')
            self._error('expecting one of: fri friday mon monday sat saturday sun sunday thu thursday tue tuesday wed wednesday')

    @graken()
    def _timeofdayconstraint_(self):
        with self._optional():
            self._token('at')
        self._times_()
        self.name_last_node('timeofdayconstraint')
        self.ast._define(
            ['timeofdayconstraint'],
            []
        )

    @graken()
    def _aftertimeofdayconstraint_(self):
        self._token('after')
        self._time_()
        self.name_last_node('aftertimeofdayconstraint')
        self.ast._define(
            ['aftertimeofdayconstraint'],
            []
        )

    @graken()
    def _betweentimesofdayconstraint_(self):
        with self._choice():
            with self._option():
                with self._group():
                    self._token('between')
                    self._time_()
                    self.add_last_node_to_name('@')
                    self._token('and')
                    self._time_()
                    self.add_last_node_to_name('@')
            with self._option():
                with self._group():
                    self._token('from')
                    self._time_()
                    self.add_last_node_to_name('@')
                    self._token('to')
                    self._time_()
                    self.add_last_node_to_name('@')
            self._error('no available options')

    @graken()
    def _nintervalconstraint_(self):
        with self._choice():
            with self._option():
                with self._group():
                    self._token('every')
                    self._integer_()
                    self._intervals_()
            with self._option():
                with self._group():
                    self._token('every')
                    self._ordinal_()
                    self._interval_()
            self._error('no available options')

    @graken()
    def _intervalconstraint_(self):
        with self._group():
            self._token('every')
            self._interval_()

    @graken()
    def _dateconstraint_(self):
        with self._choice():
            with self._option():
                with self._group():
                    with self._optional():
                        self._token('on')
                    self._dates_()
            with self._option():
                with self._group():
                    self._token('every year on')
                self._date_()
            self._error('no available options')

    @graken()
    def _datewithyearconstraint_(self):
        with self._group():
            with self._optional():
                self._token('on')
            self._datewithyear_()

    @graken()
    def _yeardayconstraint_(self):
        self._token('on the ')
        self._ordinal_()
        self._token('day of the year')

    @graken()
    def _monthdayconstraint_(self):
        self._token('on the')
        self._ordinal_()
        self.add_last_node_to_name('@')

        def block1():
            with self._optional():
                self._token(',')
            self._ordinal_()
            self.add_last_node_to_name('@')
        self._closure(block1)
        with self._optional():
            with self._optional():
                self._token(',')
            self._token('and')
            self._ordinal_()
            self.add_last_node_to_name('@')
        with self._optional():
            self._token('day of the month')

    @graken()
    def _weekdayconstraint_(self):
        with self._optional():
            self._token('every')
        self._weekday_()
        self.add_last_node_to_name('@')

        def block1():
            with self._optional():
                self._token(',')
            self._weekday_()
            self.add_last_node_to_name('@')
        self._closure(block1)
        with self._optional():
            with self._optional():
                self._token(',')
            self._token('and')
            self._weekday_()
            self.add_last_node_to_name('@')

    @graken()
    def _nthweekdayconstraint_(self):
        with self._group():
            with self._choice():
                with self._option():
                    self._token('the')
                with self._option():
                    self._token('on the')
                with self._option():
                    self._token('every')
                self._error('expecting one of: every on the the')
        self._ordinal_()
        self.add_last_node_to_name('@')
        self._weekday_()
        self.add_last_node_to_name('@')
        self._token('of the month')

    @graken()
    def _startingat_(self):
        with self._choice():
            with self._option():
                with self._group():
                    self._token('starting')
                    with self._optional():
                        with self._choice():
                            with self._option():
                                self._token('at')
                            with self._option():
                                self._token('on')
                            self._error('expecting one of: at on')
                    self._datetimewithyear_()
                    self.name_last_node('@')
            with self._option():
                self._token('starting on')
                self._weekday_()
                self.name_last_node('weekday')
            self._error('no available options')
        self.ast._define(
            ['weekday'],
            []
        )


class UnknownSemantics(object):
    def start(self, ast):
        return ast

    def atomic_constraint(self, ast):
        return ast

    def syntax_error(self, ast):
        return ast

    def constraint_list(self, ast):
        return ast

    def and_constraint(self, ast):
        return ast

    def except_constraint(self, ast):
        return ast

    def forconstraint(self, ast):
        return ast

    def timeinterval(self, ast):
        return ast

    def number(self, ast):
        return ast

    def integer(self, ast):
        return ast

    def ordinal(self, ast):
        return ast

    def time(self, ast):
        return ast

    def times(self, ast):
        return ast

    def hour(self, ast):
        return ast

    def minute(self, ast):
        return ast

    def second(self, ast):
        return ast

    def millisecond(self, ast):
        return ast

    def year(self, ast):
        return ast

    def month(self, ast):
        return ast

    def dayofmonth(self, ast):
        return ast

    def date(self, ast):
        return ast

    def dates(self, ast):
        return ast

    def datewithyear(self, ast):
        return ast

    def datetime(self, ast):
        return ast

    def datetimewithyear(self, ast):
        return ast

    def timeofdayrange(self, ast):
        return ast

    def interval(self, ast):
        return ast

    def intervals(self, ast):
        return ast

    def weekday(self, ast):
        return ast

    def timeofdayconstraint(self, ast):
        return ast

    def aftertimeofdayconstraint(self, ast):
        return ast

    def betweentimesofdayconstraint(self, ast):
        return ast

    def nintervalconstraint(self, ast):
        return ast

    def intervalconstraint(self, ast):
        return ast

    def dateconstraint(self, ast):
        return ast

    def datewithyearconstraint(self, ast):
        return ast

    def yeardayconstraint(self, ast):
        return ast

    def monthdayconstraint(self, ast):
        return ast

    def weekdayconstraint(self, ast):
        return ast

    def nthweekdayconstraint(self, ast):
        return ast

    def startingat(self, ast):
        return ast


def main(filename, startrule, **kwargs):
    with open(filename) as f:
        text = f.read()
    parser = UnknownParser(parseinfo=False)
    return parser.parse(text, startrule, filename=filename, **kwargs)

if __name__ == '__main__':
    import json
    ast = generic_main(main, UnknownParser, name='Unknown')
    print('AST:')
    print(ast)
    print()
    print('JSON:')
    print(json.dumps(ast, indent=2))
    print()

