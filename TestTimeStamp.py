import unittest
import TimeStamp


class TestTimeStamp(unittest.TestCase):
    "Class used to test the TimeStamp class."
    def setUp(self):
        self.__jan012001_1000 = TimeStamp.TimeStamp("2001-01-01 10:00")
        self.__feb281990 = TimeStamp.TimeStamp("1990-02-28 0:00")
        self.__jan312000 = TimeStamp.TimeStamp("2000-01-31 0:00")
        self.__feb292000 = TimeStamp.TimeStamp("2000-02-29 0:00")
        self.__nov302000 = TimeStamp.TimeStamp("2000-11-30 0:00")
        self.__feb292004 = TimeStamp.TimeStamp("2004-02-29 0:00")
    def testDaysInMonth(self):
        assert 31 == self.__jan312000.getDaysInMonth(), "Error: " + self.__jan312000.getDaysInMonth() + " in January 2000"
        assert 30 == self.__nov302000.getDaysInMonth(), "Error: " + self.__nov302000.getDaysInMonth() + " in November 2000"
        assert 28 == self.__feb281990.getDaysInMonth(), "Error: " + self.__feb281990.getDaysInMonth() + " in February 1990"
        assert 29 == self.__feb292000.getDaysInMonth(), "Error: " + self.__feb292000.getDaysInMonth() + " in February 2000"
        assert 29 == self.__feb292004.getDaysInMonth(), "Error: " + self.__feb292004.getDaysInMonth() + " in February 2004"

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestTimeStamp("testDaysInMonth"))
    return suite
