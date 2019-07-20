import inspect
import json
import random
import string

from pathlib import Path
from typing import Callable, Optional, Dict, Any

from wrap.options import Options


def random_string(length=5):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


class Definitions:
    free: Dict[Any, 'Definition']
    keyed: Dict[Any, 'Definition']

    def __init__(self, path: Path):
        self.path = path
        self.keyed, self.free = self._load_definitions(str(path))

    @staticmethod
    def _load_definitions(path: str):
        keyed = {}
        free = {}

        try:
            with open(path, 'r') as f:
                content = f.read()
                definitions = json.loads(content)

            for k, v in definitions['keyed'].items():
                keyed[k] = Definition(**v)

            for k, v in definitions['free'].items():
                free[k] = Definition(**v)
        except FileNotFoundError:
            pass

        return keyed, free

    def add(self, func: Callable, options: Options) -> str:
        if options.key is not None:
            definition = Definition.create(options.key, func)
            self.keyed[definition.key] = definition
            self.save()
            return definition.key

        assert options.add_key is False

        definition = Definition.create(None, func)
        if definition.name in self.free and self.free[definition.name] == definition:
            definition.key = definition.name
        else:
            for k, v in self.free.items():
                if v == definition:
                    definition.key = k

        if definition.key is None:
            if definition.name not in self.free:
                definition.key = definition.name
            else:
                definition.key = definition.name + ":" + random_string(5)

        self.free[definition.key] = definition
        self.save()

        return definition.key

    def save(self):
        path = str(self.path)
        definitions = dict(keyed={}, free={})
        for k, v in self.keyed.items():
            definitions['keyed'][k] = v.json()
        for k, v in self.free.items():
            definitions['free'][k] = v.json()

        with open(path, "w") as f:
            f.write(json.dumps(definitions, indent=2))


class Definition:
    @staticmethod
    def create(key: Optional[str], func: Callable):
        file = inspect.getfile(func)
        line = inspect.getsourcelines(func)[1]
        name = func.__name__
        signature = str(inspect.signature(func))

        return Definition(key=key,
                          file=file, line=line,
                          name=name, signature=signature)

    def __init__(self, *, key: Optional[str], file: str, line: int, name: str, signature: str):
        self.key = key
        self.file = file
        self.line = line
        self.name = name
        self.signature = signature

    def __eq__(self, other: 'Definition'):
        if other.file != self.file:
            return False
        if other.line != self.line:
            return False
        if other.name != self.name:
            return False
        if other.signature != self.signature:
            return False

        return True

    def json(self):
        return dict(key=self.key,
                    file=self.file,
                    line=self.line,
                    name=self.name,
                    signature=self.signature)
