import json

class ApiMessage():
    def __init__(self, msg):
        self.type = msg[0]
        self.channel = msg[1]
        self.message = json.loads(msg[2])

    def getGameId(self):
        return self.message["data"]["game"]["id"]
