import tornado.gen

from model.ApiMessage import ApiMessage as ApiMessage

class ApiMessageHandler:
    def __init__(self, client, channel):
        self.client = client
        self.channel = channel
    
    @tornado.gen.coroutine
    def startListening(self):
        client = self.client
        yield client.connect()
        started = yield client.pubsub_subscribe(self.channel)
        if started:
            print "Subscribed to \"%s\"\nListening..." % (self.channel)
        
        # Looping over received messages
        while True:
            # Let's "block" until a message is available
            msg = yield client.pubsub_pop_message()
            self.handleMessage(msg)

    def handleMessage(self, msg):
        msg = ApiMessage(msg)
        print "Message Type : %s" % (msg.type)
        print "Message Channel : %s" % (msg.channel)
        print "Game id : %d" % (msg.getGameId())
        print "Event : %s" % (msg.getEvent())