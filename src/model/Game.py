from utils.singleton import Singleton
from model.Ruleset import Ruleset

class Game:
    __metaclass__ = Singleton

    def __init__(self):
        self.id = 0
        self.status = ""
        self.currentRuleset = Ruleset
        self.options = {}

    def setId(self, id):
        self.id = id

    def setNewGame(self, id):
        self.id = id
        self.status = "pending"
        self.options = {}
        self.currentRuleset = {}

    def setCurrentRuleset(self, ruleset):
        self.currentRuleset = ruleset

    def setOptions(self, options):
        self.options = options