import json
import random
import string
from pathlib import Path
from typing import Dict, Any, List

import numpy as np
import torch

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

def get_arg_info(value, options):
        info = {}
        if options.signature:
            t = type(value)
            info['type'] = f"{t.__module__}.{t.__name__}"

        if options.dimensions:
            if isinstance(value, np.ndarray):
                info['shape'] = list(value.shape)
            if isinstance(value, torch.Tensor):
                info['shape'] = list(value.shape)

        return info

class Call:
    def __init__(self, *,
                 key: str, options: Options,
                 args: List[Any], kwargs: Dict[str, Any],
                 start: float):
        self.key = key
        self.start = start
        self.end = -1
        self.args = [get_arg_info(a, options) for a in args]
        self.kwargs = {k: get_arg_info(v, options) for k, v in kwargs.items()}

    def json(self):
        data = dict(key=self.key,
                    start=self.start,
                    end=self.end,
                    args=self.args,
                    kwargs=self.kwargs)

        return data
