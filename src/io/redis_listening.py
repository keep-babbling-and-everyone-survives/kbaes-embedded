import redis
import time
import traceback
import json

def RedisCheck():
    try:
        r = redis.StrictRedis(host='192.168.33.10', port=6379)

        p = r.pubsub()
        p.subscribe('private-newgame.4')
        PAUSE = True

        while PAUSE:
            message = p.get_message()
            if message:
                command = message['data']
                if type(command) == str:
                    print (json.loads(command)['data'])

                if command == b'START':
                    PAUSE = False

            time.sleep(1)

        print("Permission to start...")

    except Exception as e:
        print("!!!!!!!!!! EXCEPTION !!!!!!!!!")
        print(str(e))
        print(traceback.format_exc())

RedisCheck()