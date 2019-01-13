from tornado.gen import coroutine
from tornado.options import options
import tornado.ioloop

import json

from utils.singleton import Singleton
from utils.httpClient import http_post_async

from model.Game import Game

class Player:
    __metaclass__ = Singleton
    game = Game()

    @classmethod
    def newGame(cls, message):
        print "Game id : %d" % (message.getGameId())
        print "Options: %s" % (json.dumps(message.getGameOptions()))
        print "Modules: %s" % (json.dumps(message.getRequiredModules()))
        if cls.game.id == message.getGameId():
            if cls.game.status == "pending" and message.getGameStatus() == "pending":
                print "Game %d pending" % (cls.game.id)
                cls.startGame(message.getGameId())
            elif cls.game.status == "running" and message.getGameStatus() == "running":
                print "Game %d already started" % (cls.game.id)
            elif (cls.game.status == "aborted" and message.getGameStatus() == "aborted") or (cls.game.status == "finished" and message.getGameStatus() == "finished"):
                print "Game %d finished" % (cls.game.id)
            else:
                print "Inconsistence in game status. Reseting games"
                cls.game.setNewGame(message.getGameId())
        else:
            cls.game.setNewGame(message.getGameId())
            cls.game.setOptions(message.getGamesOptions())
            cls.startGame(message.getGameId())

    @classmethod
    def startGame(cls, gameId):
        print "New game created..."
        boardCanPlay = True # board validation with requested modules
        if boardCanPlay:
            print "Board validated, sending confirmation to the webservices and requesting first ruleset"
            req_url = "%s://%s/api/game/%d/confirm" % (options.api_protocol, options.api_address, cls.game.id)
            req_headers_dict = {'Accept': "application/json",'Content-Type': "application/json"}
            req_body_dict = {'status':'OK'}
            confirmation = http_post_async(req_url, req_headers_dict, req_body_dict)
            # Execute the http request on main IOLoop
            tornado.ioloop.IOLoop.instance().add_future(confirmation, onGameConfirmReponse)

    @classmethod
    def initBoard(cls, ruleset, gameid):
        print "Webservices accepted confirmation, starting the game..."
        cls.game.status = "running"
        # Le code de valentin ici

def onGameConfirmReponse(response):
    result = response.result()
    result = json.loads(result)
    Player.initBoard(result["next_ruleset"], result["game_id"])
