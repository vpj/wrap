import inspect
import json


class Definition:
    def __init__(self, func):
        self.file = inspect.getfile(func)
        self.line = inspect.getsourcelines(func)[1]
        self.name = func.__name__
        self.signature = str(inspect.signature(func))

    def json(self):
        return dict(file=self.file,
                    line=self.line,
                    name=self.name,
                    signature=self.signature)

    def json_str(self):
        return json.dumps(self.json())
