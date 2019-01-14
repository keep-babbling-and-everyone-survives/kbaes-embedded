import json

class ApiMessage():
    def __init__(self, msg):
        self.type = msg[0]
        self.channel = msg[1]
        self.message = json.loads(msg[2])

    def getGameId(self):
        try:
            out = self.message["data"]["game"]["id"]
        except:
            return 0
        else:
            return int(out)

    def getGameOptions(self):
        try:
            out = self.message["data"]["game"]["options"]
        except:
            return "0"
        else:
            return out

    def getEvent(self):
        try:
            out = self.message["event"]
        except:
            return ""
        else:
            return out[out.rfind('\\')+1:]

    def getRequiredModules(self):
        try:
            out = self.message["data"]["game"]["modules"]
        except:
            return ""
        else:
            return out

    def getGameStatus(self):
        try:
            out = self.message["data"]["game"]["status"]
        except:
            return ""
        else:
            return out
