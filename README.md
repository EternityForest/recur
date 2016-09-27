#recur: fast reliable recurring events for python

Recur is a python library providing support for specifying recurring events with a plain english like syntax.
for example:
    every 3 days at 3pm
is internally translated to a set of "constraint objects" where the first constraint is one that matches "every 3 days" and the second is one that matches 3pm on any given day. Events occur at times when all constraints match.

constraints can also represent ranges of times, and in this case an event occurs at the beginning of each matching period.

recur is optimized so that constraints like "every 2 seconds on mondays" will never sift through every single second just to find the one on monday. Instead, recur first skips to midnight on the next monday(recur knows which constraints to match first based on the average time between matches), then asks the "2 seconds" constraint what the next match is after midnight.

The api is very simple.

recur.getConstraint("every day")
recur.after(datetime.datetime.now(), inclusive=False)
