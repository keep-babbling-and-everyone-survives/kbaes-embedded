from utils.singleton import Singleton
from model.Ruleset import Ruleset

class Game:
    __metaclass__ = Singleton

    def __init__(self):
        self.id = 0
        self.status = ""
        self.currentRuleset = Ruleset
        self.options = {}
        self.interrupted = False

    def setId(self, id):
        self.id = id

    def setNewGame(self, id):
        self.id = id
        self.status = "pending"
        self.options = {}
        self.currentRuleset = {}
        self.interrupted = False

    def setCurrentRuleset(self, ruleset):
        self.currentRuleset = ruleset

    def setOptions(self, options):
        self.options = options

    def interrupt(self):
        self.interrupted = True