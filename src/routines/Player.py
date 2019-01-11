from tornado.gen import coroutine
from utils.singleton import Singleton

class Player:
    __metaclass__ = Singleton

    @staticmethod
    def newGame(message):
        print "Game id : %d" % (message.getGameId())
        print "Options: %s" % (message.getGameOptions())
        print "Modules: %s" % (message.getRequiredModules())
        print "Newgame"
        # create or poll new Game vie singleton
        # check if game is not running or finished
        # populate new game with id and options
        # check board relevance and module presence
        # query /api/game/{id}/confirm

