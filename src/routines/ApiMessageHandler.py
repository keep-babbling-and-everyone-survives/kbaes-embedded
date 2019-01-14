from tornado.gen import coroutine
import tornado.ioloop

from model.ApiMessage import ApiMessage as ApiMessage
from routines.Player import Player

class ApiMessageHandler:
    def __init__(self, client, channel):
        self.client = client
        self.channel = channel

    @coroutine
    def startListening(self):
        client = self.client
        connection = yield client.connect()
        if connection:
            started = yield client.pubsub_subscribe(self.channel)
            if started:
                print "Subscribed to \"%s\"\nListening..." % (self.channel)

            # Looping over received messages
            while True:
                # Let's "block" until a message is available
                msg = yield client.pubsub_pop_message()
                self.handleMessage(msg)
        else:
            print "Connection error."
            tornado.ioloop.IOLoop.instance().stop()

    def handleMessage(self, msg):
        message = ApiMessage(msg)
        print "Message Type : %s" % (message.type)
        print "Message Channel : %s" % (message.channel)
        print "Event : %s" % (message.getEvent())
        return self.triggerEvent(message)

    def triggerEvent(self, message):
        dispatcher = {
            "RequestNewGame": Player.newGame
        }
        event = message.getEvent()
        dispatch = dispatcher.get(event, lambda: self.unknownEvent)
        dispatch(message)
        
        return ""
    
    def unknownEvent(self):
        print "This event is not handled."