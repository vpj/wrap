import json
from pathlib import Path
from typing import Dict, Any, List, Union, Tuple

import numpy as np
import torch

from wrap.options import Options


class Calls:
    def __init__(self, path: Path):
        self.path = path

    def add(self, *,
            key: str, options: Options,
            args: Union[List[Any], Tuple], kwargs: Dict[str, Any],
            start: float):
        call = Call(key=key, options=options,
                    args=args, kwargs=kwargs,
                    start=start)
        return call

    def save(self, options: Options, call: 'Call', end: float, ret: Any):
        call.end = end
        call.ret = get_arg_info(ret, options)
        path = str(self.path)
        with open(path, "a") as f:
            f.write(json.dumps(call.json()) + '\n')


PRIMITIVE_TYPES = {int, float}


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

    if options.primitive_values:
        if type(value) in PRIMITIVE_TYPES:
            info['value'] = value
        if type(value) is str:
            if len(value) <= options.strings_limit:
                info['value'] = value
            else:
                info['value'] = value[:options.strings_limit]
                info['len'] = len(value)

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
        self.ret = None

    def json(self):
        data = dict(key=self.key,
                    start=self.start,
                    end=self.end,
                    args=self.args,
                    kwargs=self.kwargs,
                    ret=self.ret)

        return data
