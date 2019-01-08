import json

class ApiMessage():
    def __init__(self, msg):
        self.type = msg[0]
        self.channel = msg[1]
        self.message = json.loads(msg[2])        

    def getGameId(self):
        try:
            self.message["data"]["game"]["id"]
        except:
            return 0
        else:
            return int(self.message["data"]["game"]["id"])

    def getGameOptions(self):
        try:
            self.message["data"]["game"]["options"]
        except:
            return "0"
        else:
            return self.message["data"]["game"]["options"]

    def getEvent(self):
        try:
            out = self.message["event"]
        except:
            return ""
        else:
            return out[out.rfind('\\')+1:]
