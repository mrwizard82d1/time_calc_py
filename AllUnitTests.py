"Module for executing all unit tests."


import unittest
import TestActivityMemento


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestActivityMemento.TestActivityMemento("testCreation"))
    return suite
