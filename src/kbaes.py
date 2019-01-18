import tornado.ioloop
import tornado.gen
import tornadis
import sys

from tornado.options import options, define
from routines.ApiMessageHandler import ApiMessageHandler as ApiMessageHandler
from reset_board import reset_board

define('api_protocol')
define('api_address')
define('redis_address')
define('redis_port', type=int)
define('channel_name')
define('board_id', type=int)

options.parse_config_file('./kbaes.conf')

client = tornadis.PubSubClient(host=options.redis_address, port=options.redis_port, autoconnect=False)

listener = ApiMessageHandler(client, "%s%d" % (options.channel_name, options.board_id))

if __name__ == '__main__':
    reset_board()
    try:
        tornado.ioloop.IOLoop.current().run_sync(listener.startListening)
    except (KeyboardInterrupt, SystemExit):
        print '\n! Received keyboard interrupt, quitting threads.\n'
        sys.exit()
