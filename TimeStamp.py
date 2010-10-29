import re


class TimeStamp:
    "Models a time stamp."
    def __init__(self, isoStamp):
        (date, timeOfDay) = re.split('\s+', isoStamp)
        (self.__year, self.__month, self.__day) = re.split('-', date)
        (self.__hour, self.__minute) = re.split(':', timeOfDay)
    def __sub__(self, other):
        year = self.__year
        month = self.__month
        day = self.__day
        hour = self.__hour
        minute = self.__minute

        minute = minute - other.__minute
        if (minute < 0):
            minute = minute + 60
            hour = hour - 1

        hour = hour - other.__hour
        if (hour < 0):
            hour = hour + 24
            day = day - 1

        day = day - other.__day
        if (day < 0):
            day = day + getDaysInMonth(month)
            month = month - 1

    def getDaysInMonth(self):
        if int(self.__month) in [ 1, 3, 5, 7, 8, 10, 12 ]:
            return 31
        elif int(self.__month) in [ 4, 6, 9, 11 ]:
            return 30
        else:
            daysInMonth = 28
            if ((int(self.__year) % 400 == 0) or (int(self.__year) % 4 == 0 and int(self.__year) % 100 != 0)):
                daysInMonth = daysInMonth + 1
            return daysInMonth
        
