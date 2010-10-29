class ActivityMemento:
    "A Memento for an activity."
    def __init__(self, aString):
        self.__state = aString
    def getState(self):
        return self.__state
