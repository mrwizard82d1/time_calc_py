#! /cygdrive/c/cygwin/bin/env python
#
# Python script to calcuate the duration of a task.
#
# Filter function: reads from standard input and writes to standard output. 
# Each task has the form YYYY-MM-DD hh:mm <Details>
#


import re
import string
import sys


summary = {}
nextLine = sys.stdin.readline()
while (nextLine != '' and nextLine != '\n'):
    [ date, time, duration, category ] = re.split('\s+', nextLine, 3)
    category = category.strip()
    [ hours, minutes ] = re.split(':', duration)
    elapsedDuration = int(hours) + float(minutes) / 60
    if category in summary:
        summary[category] = summary[category] + elapsedDuration
    else:
        summary[category] = elapsedDuration
    nextLine = sys.stdin.readline()

theCategories = list(summary.keys())
theCategories.sort()
for category in theCategories:
    print("%s:\t%.02f" % (category, summary[category]))
    
    
