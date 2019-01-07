# Let's import tornado and tornadis
import tornado.ioloop
import tornado.gen
import tornadis

@tornado.gen.coroutine
def listenRedis():
    yield client.connect()
    started = yield client.pubsub_subscribe('private-raspberry.0')
    if started:
        print "Subscribed to \"private-raspberry.0\"\nListening..."
    
    # Looping over received messages
    while True:
        # Let's "block" until a message is available
        msg = yield client.pubsub_pop_message()
        print(msg)
        # >>> ['pmessage', 'foo*', 'foo', 'bar']
        # (for a "publish foo bar" command from another connection)

        if isinstance(msg, tornadis.TornadisException):
            # closed connection by the server
            break
        elif len(msg) >= 4 and msg[3] == "STOP":
            # it's a STOP message, let's unsubscribe and quit the loop
            yield client.pubsub_unsubscribe("private-raspberry.0")
            break

    # Let's disconnect
    client.disconnect()


# Build a tornadis.Client object with some options as kwargs
# host: redis host to connect
# port: redis port to connect
# autoconnect=True: put the Client object in auto(re)connect mode
client = tornadis.PubSubClient(host="192.168.33.10", port=6379, autoconnect=False)

# Start a tornado IOLoop, execute the coroutine and end the program
if __name__ == '__main__':
    tornado.ioloop.IOLoop.instance().run_sync(listenRedis)