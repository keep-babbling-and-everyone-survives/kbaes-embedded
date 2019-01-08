import tornado.ioloop
import tornado.gen
import tornadis

from routines.ApiMessageHandler import ApiMessageHandler as ApiMessageHandler

channel = "private-board.1"

client = tornadis.PubSubClient(host="192.168.33.10", port=6379, autoconnect=False)

listener = ApiMessageHandler(client, channel)

if __name__ == '__main__':
    tornado.ioloop.IOLoop.instance().run_sync(listener.startListening)