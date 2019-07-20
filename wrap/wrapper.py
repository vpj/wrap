import types
from typing import Callable, Optional

from wrap.options import Options

default_options = Options.default()


class Wrapping:
    def __init__(self, options: Options):
        options.inherit(default_options)
        self.options = options

    def __call__(self, func):
        return Wrapper(func, self.options)


class Wrapper:
    def __init__(self, func, options: Options):
        self.options = options
        self.func = func

    def __call__(self, *args, **kwargs):
        print(self.options, ':')
        self.func(*args, **kwargs)


def wrap(func: Optional[Callable]=None, *,
         signature: Optional[bool] = None):
    if func is not None:
        if isinstance(func, types.FunctionType):
            return Wrapper(func, default_options)
    else:
        return Wrapping(Options(signature=signature))
