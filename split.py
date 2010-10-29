#! env python

from datetime import datetime
from datetime import timedelta
from datetime import time
import getopt
import sys

def elapsedToHHMM(elapsed):
    (hh, mm) = (elapsed / 60, elapsed % 60)
    return (hh, mm)

def hhmmToElapsed(hh, mm):
    return hh * 60 + mm
    
def split(count, finis, start=time()):
    if finis < start:
        raise ValueError, 'Finish %s less than start %s' % (finis, start)
    finisDateTime = datetime.today().replace(hour=finis.hour, minute=finis.minute, second=finis.second)
    startDateTime = datetime.today().replace(hour=start.hour, minute=start.minute, second=start.second)
    elapsedTime = finisDateTime - startDateTime
        
    if count == 2:
        mssElapsed = (elapsedTime * 6) // 10
        vpnElapsed = (elapsedTime * 4) // 10
        return mssElapsed, vpnElapsed
    elif count == 3:
        fwElapsed = (elapsedTime * 4) // 10
        vpnElapsed = (elapsedTime * 3) // 10
        idsElapsed = (elapsedTime * 3) // 10
        return fwElapsed, vpnElapsed, idsElapsed
    else:
        raise ValueError, 'Unrecognized count for split: %s' % count

if __name__ == '__main__':
    usage = """Usage %s [SPLIT] [TIME in hh:mm format]...
    \t-s, --split COUNT\tspecify two-way or three-way split
    """ % sys.argv[0]
    try:
        (options, args) = getopt.getopt(sys.argv[1:], 's:', ['split='])
    except getopt.GetoptError:
        print >> sys.stderr, usage
        sys.exit(1)
    
    for option, value in options:
        if option in ['-s', '--split']:
            splitcount = value
    try:
        int(splitcount)
    except NameError:
        print >> sys.stderr, usage
        sys.exit(1)
    
    midnight = datetime.now().replace(hour=0, minute=0, second=0)
    try:
        hh, mm = args[0].split(':')
        finis = datetime.now().replace(hour=int(hh), minute=int(mm))
        start = midnight
    except IndexError:
        print >> sys.stderr, usage
        sys.exit(1)
    
    if len(args) == 2:
        start = finis
        hh, mm = args[1].split(':')
        finis = datetime.now().replace(hour=int(hh), minute=int(mm))
    elif len(args) > 2:
        print >> sys.stderr, usage
        sys.exit(1)
    
    if splitcount == '2':
        mssElapsed, vpnElapsed = split(2, start=start, finis=finis)
        print 'mss:\t%s' % str((midnight + mssElapsed).timetz())[:5]
        print 'vpn:\t%s' % str((midnight + vpnElapsed).timetz())[:5]
    elif splitcount == '3':
        mssElapsed, vpnElapsed, idsElapsed = split(3, start=start, finis=finis)
        print 'mss:\t%s' % str((midnight + mssElapsed).timetz())[:5]
        print 'vpn:\t%s' % str((midnight + vpnElapsed).timetz())[:5]
        print 'ids:\t%s' % str((midnight + idsElapsed).timetz())[:5]
    else:
        print >> sys.stderr, usage
        sys.exit(1)
    


