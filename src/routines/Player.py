# -*- coding: utf-8 -*-

from tornado.gen import coroutine
from tornado.options import options
from Queue import Queue
import time
import sys
import tornado.ioloop

import json
from threading import Thread

from utils.singleton import Singleton
from utils.httpClient import http_post_async

from model.Game import Game
from model.Ruleset import Ruleset

#from modules.ButtonModule import playModule as playModule
#from modules.TimerModule import TimerModule
from modules.MockModule import ButtonModule
from modules.TimeMock import TimerModule

class Player:
    __metaclass__ = Singleton
    game = Game()
    timer = TimerModule
    modulePlayer = ButtonModule
    q = Queue()

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
                print "Received new game request for game %d, but it's already started." % (cls.game.id)
            elif (cls.game.status == "aborted" and message.getGameStatus() == "aborted") or (cls.game.status == "finished" and message.getGameStatus() == "finished"):
                print "Received new game request for game %d, but it's already finished" % (cls.game.id)
            else:
                print "Inconsistence in game status. Reseting games"
                cls.game.setNewGame(message.getGameId())
        else:
            print "Received new game request for game %d..." % (message.getGameId())
            cls.game.setNewGame(message.getGameId())
            cls.game.setOptions(message.getGameOptions())
            cls.startGame(message.getGameId())

    @classmethod
    def abortGame(cls, message):
        if (message.getGameId() == cls.game.id):
            cls.game.interrupt()
            print "Requested game interruption. Resetting the board."
            if (cls.game.status == "running"):
                cls.modulePlayer.stop()
                cls.end_game(True)

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
            tornado.ioloop.IOLoop.current().add_future(confirmation, Player.onGameConfirmReponse)

    @staticmethod
    def eventLoop(player, iol):
        result = player.q.get()
        if result["event"] == "RS_ANSWERED":
            iol.add_callback(player.sendAnswer,result["answer"])
        elif result["event"] == "TIMER_DONE":
            sys.stdout.write("\ntimer for game %d ended.\n" % (player.game.id))
            sys.stdout.flush()
            player.game.interrupt()
            player.modulePlayer.stop()
            iol.add_callback(player.end_game, True)
        time.sleep(0.1)

    @classmethod
    def initBoard(cls, ruleset):
        print "Webservices accepted confirmation, starting the game..."
        cls.game.status = "running"
        cls.timer = TimerModule(cls.game.id, cls.game.options["errors"], cls.game.options["time"], cls.q)
        cls.timer.daemon = True
        cls.timer.start()
        cls.execRuleSet(ruleset)

    @classmethod
    def execRuleSet(cls, ruleset):
        if not cls.game.interrupted:
            cls.game.currentRuleSet = Ruleset(ruleset)
            cls.timer.gameRunning = True
            answerprint = "Reponse attendue : "
            for rs in cls.game.currentRuleSet.modules:
                answerprint = "%s%d" % (answerprint, rs.solution)
            rsCombination = bin(cls.game.currentRuleSet.combination)
            print "Waiting for player input (ruleset %s)..." % (rsCombination[rsCombination.rfind('b')+1:])
            print answerprint
            t = Thread(target = Player.eventLoop, args= (cls, tornado.ioloop.IOLoop.current(),))
            t.setDaemon(True)
            t.start()
            cls.modulePlayer = ButtonModule(cls.game.currentRuleSet, cls.q)
        else:
            print "Interrupted.\nListening..."

    @classmethod
    def sendAnswer(cls, answer):
        answerprint  = "Reponse donnee : "
        for r in answer:
            answerprint = "%s%d" % (answerprint, r["solution"])
        print answerprint
        print "Answer received from board, parsing and sending to API..."
        req_url = "%s://%s/api/game/%d/answer/%d" % (options.api_protocol, options.api_address, cls.game.id, cls.game.currentRuleSet.id)
        req_headers_dict = {'Accept': "application/json",'Content-Type': "application/json"}
        req_body_dict = {'modules': answer}
        answerSending = http_post_async(req_url, req_headers_dict, req_body_dict)
        tornado.ioloop.IOLoop.current().add_future(answerSending, cls.onAnswerSent)

    @classmethod
    def onGameConfirmReponse(cls, response):
        result = response.result()
        result = json.loads(result)
        Player.initBoard(result["next_ruleset"])

    @classmethod
    def onModuleSolved(cls, response):
        Player.sendAnswer(response.result())

    @classmethod
    def onAnswerSent(cls, response):
        result = response.result()
        result = json.loads(result)
        if result["has_next"]:
            cls.execRuleSet(result["next_ruleset"])
            if result["solved"] == 0:
                cls.timer.increment_error_count()
        else:
            cls.end_game(result["failed"])

    @classmethod
    def end_game(cls, failed):
        message = "Perdu" if failed else "Gagne"
        cls.timer.display_game_over(message)
        print "Game finished."
        print "Listening..."

