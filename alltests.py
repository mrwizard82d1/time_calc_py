#! env python


import os
import re
import unittest


def suite():
    filenames = os.listdir('.')
    testFilenames = [filename for filename in filenames if re.match('.*Test', filename)]
    print testFilenames
    allTests = unittest.TestSuite()
    for module in (__import__, testFilenames):
        allTests.addTest(unittest.findTestCases(module))
        
    return allTests
        

if __name__ == '__main__':
    unittest.main(defaultTest='suite')