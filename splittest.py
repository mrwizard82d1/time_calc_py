#! env python


"""Unit tests the function to split some time between multiple 'projects.'"""


from datetime import time
from datetime import timedelta
import unittest

import split


class SplitIntervalTest(unittest.TestCase):
    """Split a single time interval."""
    def testIntervalTwoWay(self):
        """Test a two-way split of a time interval."""
        actualTwoWay = split.split(2, time(hour=1, minute=40))
        self.assertEquals((timedelta(hours=1), timedelta(minutes=40)), actualTwoWay, 
                          'Two-way split of single interval: %s, %s' % actualTwoWay)
        
    def testIntervalThreeWay(self):
        """Test a three-way split."""
        actualThreeWay = split.split(3, time(hour=1, minute=40))
        self.assertEquals((timedelta(minutes=40), timedelta(minutes=30), timedelta(minutes=30)), actualThreeWay, 
                          'Three-way split of single interval: %s, %s, %s' % actualThreeWay)
        
        
class SplitRangeTest(unittest.TestCase):
    """Split a single time interval."""
    def testRangeTwoWay(self):
        """Test a two-way split of a time range."""
        actualTwoWay = split.split(2, start=time(hour=9), finis=time(hour=10, minute=40))
        self.assertEquals((timedelta(hours=1), timedelta(minutes=40)), actualTwoWay, 
                          'Two-way split of range: %s, %s' % actualTwoWay)
        
    def testRangeThreeWay(self):
        """Test a three-way split of a time range."""
        actualThreeWay = split.split(3, start=time(hour=9), finis=time(hour=10, minute=40))
        self.assertEquals((timedelta(minutes=40), timedelta(minutes=30), timedelta(minutes=30)), actualThreeWay, 
                          'Three-way split of range: %s, %s, %s' % actualThreeWay)
        
        
class InvalidSplitParameters(unittest.TestCase):
    """Tests an invalid split count."""
    def testInvalidCountValue(self):
        """Tests an invalid split count."""
        self.assertRaises(ValueError, split.split, -1, time(hour=1, minute=40))
        self.assertRaises(ValueError, split.split, 'aspersion', time(hour=14), time(hour=15))
        
    def testInvalidTimeRange(self):
        """Tests an invalid time range."""
        self.assertRaises(ValueError, split.split, 2, start=time(hour=12, minute=1), finis=time(hour=12, minute=0))
        
        
if __name__ == '__main__':
    unittest.main()
