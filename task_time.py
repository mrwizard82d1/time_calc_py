2010-04-26 0800 cf-cqs
2010-04-26 1030 scm-trans
2010-04-26 1200 prsnl
2010-04-26 1310 scm-trans
2010-04-26 1600 cf-cqs
2010-04-26 1705 go hom
#! /cygdrive/c/cygwin/bin/env python
#
# Python script to calcuate the duration of a task.
#
# Filter function: reads from standard input and writes to standard output. 
# Each task has the form YYYY-MM-DD hh:mm <Details>
#


import datetime
import re
import string
import sys


def calcDifference(date, time, previousDate, previousTime):
    """Calculate the difference between two datetimes."""
    hour, minute = splitTime( time )
    year, month, day = splitDate( date )

    if int(hour) < 24:
        finis = datetime.datetime(hour=int(hour),
                                  minute=int(minute), year=int(year),
                                  month=int(month), day=int(day))
    else:
        finis = datetime.datetime(hour=0,
                                  minute=int(minute), year=int(year),
                                  month=int(month), day=int(day) + 1)
        
    
    hour, minute = splitTime( previousTime )
    year, month, day = splitDate( previousDate )
    start = datetime.datetime(hour=int(hour), minute=int(minute),
                              year=int(year), month=int(month),
                              day=int(day))
    
    assert finis >= start, \
           'Start time %s greater than finish %s' % (str(start), str(finis))
    assert (finis - start).days == 0, \
           'Finish time %s greater than 24 hours behind start %s' % \
           (str(start), str(finis))
        
    return finis - start


def splitDate(date):
    """Split a date in either yyyy-mm-dd or yyyymmdd format."""
    try:
        year, month, day = re.split( '-', date )
    except ValueError:
        year = date[:4]
        month = date[4:6]
        day = date[6:]
    return year, month, day
    
def splitTime(time):
    """Split a time in either hh:mm or hhmm format."""
    try:
        hour, minute = re.split( ':', time )
    except ValueError:
        minute = time[-2:]
        hour = time[:-2]
    return hour, minute
        

if __name__ == '__main__':
    previousDate = None
    nextLine = sys.stdin.readline()
    while (nextLine != "" and nextLine != '\n'):
        [ date, time, details ] = re.split('\s+', nextLine, 2)
        if (previousDate != None):
            duration = calcDifference(date, time, previousDate, previousTime)
            print(previousDate, previousTime, str(duration)[:4], 
                  previousDetails)
        previousDate = date
        previousTime = time
        previousDetails = details.strip()
        nextLine = sys.stdin.readline()
    
