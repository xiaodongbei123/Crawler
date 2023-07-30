import json


class Command:
    def __init__(self):
        pass
    def json_parser(self, file):
        with open(file, "r", encoding="utf-8") as fp:
            return json.load(fp)

Singleton_cmd = Command()
