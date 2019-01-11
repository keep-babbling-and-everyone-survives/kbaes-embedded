from utils.singleton import Singleton

class Game:
    __metaclass__ = Singleton

    def __init__(self)
        self.id = 0
        self.status = ""
        self.currentRuleset = ""

    def setId(self, id)
        self.id = id