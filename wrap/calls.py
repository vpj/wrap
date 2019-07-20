import json
import random
import string
from pathlib import Path
from typing import Dict, Any, List

from wrap.options import Options


def random_string(length=5):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


class Calls:
    def __init__(self, path: Path):
        self.path = path

    def add(self, *,
            key: str, options: Options,
            args: List[Any], kwargs: Dict[str, Any],
            start: float):
        call = Call(key=key, options=options,
                    args=args, kwargs=kwargs,
                    start=start)
        return call

    def save(self, call: 'Call', end: float):
        call.end = end
        path = str(self.path)
        with open(path, "a") as f:
            f.write(json.dumps(call.json()) + '\n')


class Call:
    def __init__(self, *,
                 key: str, options: Options,
                 args: List[Any], kwargs: Dict[str, Any],
                 start: float):
        self.key = key
        self.start = start
        self.end = -1
        if options.signature:
            self.arg_types = [self.get_type(a) for a in args]
            self.kwargs_types = {k: self.get_type(v) for k, v in kwargs.items()}
        else:
            self.arg_types = None
            self.kwargs_types = None

    @staticmethod
    def get_type(value: Any) -> str:
        t = type(value)
        return f"{t.__module__}.{t.__name__}"

    def json(self):
        data = dict(key=self.key,
                    start=self.start,
                    end=self.end)
        if self.arg_types is not None:
            data['arg_types'] = self.arg_types
            data['kwarg_types'] = self.kwargs_types

        return data
