#! env python

import sys

import calcduration

def elapsedToHHMM(elapsed):
    (hh, mm) = (elapsed / 60, elapsed % 60)
    return (hh, mm)

def hhmmToElapsed(hh, mm):
    return hh * 60 + mm

if len(sys.argv) < 2:
    print 'Usage: %s <elapsed time in hh:mm>'
    sys.exit(1)

# must have at least one argument.
hh, mm = sys.argv[1].split(':')

if len(sys.argv) == 3:
    startTime = sys.argv[1]
    finisTime = sys.argv[2]
    startDate = '2003-08-15'            # assume time on same date
    finisDate = '2003-08-15'
    hh, mm = calcduration.calcDifference(finisDate, finisTime, startDate, startTime).split(':')

elapsed = hhmmToElapsed(int(hh), int(mm))
mssElapsed = elapsed * 0.60
vpnElapsed = elapsed * 0.40
(mssHH, mssMM) = elapsedToHHMM(mssElapsed)
(vpnHH, vpnMM) = elapsedToHHMM(vpnElapsed)

print 'mss: %02d:%02d' % (mssHH, mssMM)
print 'vpn: %02d:%02d' % (vpnHH, vpnMM)

