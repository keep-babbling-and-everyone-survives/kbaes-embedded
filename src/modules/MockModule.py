import tornado.gen
import json

@tornado.gen.coroutine
def playModule(ruleset):
    answer = 0
    for module in ruleset.modules:
        i = raw_input("Le module est un '%s', quelle reponse donnez-vous ? " % (module.name))
        if i == "1":
            answer = answer << 1
            answer = answer | 1
        else :
            answer = answer << 1
    answer = yield tornado.gen.maybe_future(convertToJson(answer, ruleset))
    raise tornado.gen.Return(answer)

def convertToJson(answer, ruleset):
    modules = []
    moduleslen = len(ruleset.modules)
    for n in range(moduleslen):
        bit = 2**(moduleslen-(n+1))
        modules.append({"name": ruleset.modules[n].name, "solution": answer & bit > 0})
    return modules

