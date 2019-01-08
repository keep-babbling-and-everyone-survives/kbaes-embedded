import tornado.ioloop
import tornado.gen
import tornadis

from tornado.options import options, define
from routines.ApiMessageHandler import ApiMessageHandler as ApiMessageHandler

define('redis_address')
define('redis_port', type=int)
define('channel_name')
define('board_id', type=int)

options.parse_config_file('./kbaes.conf')

client = tornadis.PubSubClient(host=options.redis_address, port=options.redis_port, autoconnect=False)

listener = ApiMessageHandler(client, "%s%d" % (options.channel_name, options.board_id))

if __name__ == '__main__':
    tornado.ioloop.IOLoop.instance().run_sync(listener.startListening)