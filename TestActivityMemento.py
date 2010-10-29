"Class to test the ActivityMemento class."


import unittest
import ActivityMemento


class TestActivityMemento(unittest.TestCase):
    def setUp(self):
        self.__stringRep = "2001-01-01 08:00 Exercise quietly."
    def testCreation(self):
        memento = ActivityMemento.ActivityMemento(self.__stringRep)
        assert memento.getState() == self.__stringRep
    
