import json

class Ruleset:
    def __init__(self, ruleset):
        self.combination = ruleset["combination"]
        self.id = ruleset["id"]
        self.modules = []
        for m in ruleset["modules"]:
            self.modules.append(Module(m["name"], m["range_min"], m["range_max"], m["solution"]))

class Module:
    def __init__(self, name, rangemin, rangemax, solution):
        self.name = name
        self.range = {'min': rangemin, 'max': rangemax}
        self.solution = solution