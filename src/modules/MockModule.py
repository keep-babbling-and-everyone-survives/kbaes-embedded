import tornado.gen
from threading import Thread
import json

class ButtonModule(Thread):
    def __init__(self, ruleset, queue):
        Thread.__init__(self)
        self.q = queue
        self.ruleset = ruleset
        self.should_continue = True
        self.daemon = True
        self.start()

    def run(self):
        answer = 0
        module = iter(self.ruleset.modules)
        while self.should_continue:
            try:
                name = module.next().name
                i = raw_input("Le module est un '%s', quelle reponse donnez-vous ? " % (name))
                if i == "1":
                    answer = answer << 1
                    answer = answer | 1
                else :
                    answer = answer << 1
            except StopIteration:
                self.stop()
                response = {"event": "RS_ANSWERED", "answer": self.convertToJson(answer, self.ruleset)}
                self.q.put(response)

    def stop(self):
        self.should_continue = False

    def convertToJson(self, answer, ruleset):
        modules = []
        moduleslen = len(ruleset.modules)
        for n in range(moduleslen):
            bit = 2**(moduleslen-(n+1))
            modules.append({"name": ruleset.modules[n].name, "solution": int(answer & bit > 0)})
        return modules

