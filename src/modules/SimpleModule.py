import tornado.gen

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
    answer = yield tornado.gen.maybe_future(answer)
    raise tornado.gen.Return(answer)
