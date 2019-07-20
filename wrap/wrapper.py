import math
import time
import types
from pathlib import Path
from typing import Callable, Optional, Union

from wrap.calls import Calls
from wrap.definitions import Definition, Definitions
from wrap.options import Options

default_options = Options.default()


class State:
    def __init__(self, log_dir: Path):
        self.log_dir: Path = log_dir
        if not self.log_dir.exists():
            self.log_dir.mkdir(parents=True)
        self.definitions = Definitions(self.log_dir / 'definitions.json')
        self.calls = Calls(self.log_dir / 'calls.jsonl')


state: Optional[State] = None


def init_wrap(log_dir: Union[str, None, Path]):
    global state

    assert state is None

    if log_dir is not None:
        if type(log_dir) == Path:
            log_dir = log_dir
        else:
            log_dir = Path(log_dir)

    state = State(log_dir)


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
        self.key = state.definitions.add(self.func, self.options)
        self._log_next = 0
        self._counter = 0
        self._skip = self.options.skip

    def __call__(self, *args, **kwargs):
        if not self.should_log():
            return self.func(*args, **kwargs)

        start = time.time()
        call = state.calls.add(key=self.key, options=self.options,
                               args=args, kwargs=kwargs,
                               start=start)
        print(self.options, self.key, ':')
        ret = self.func(*args, **kwargs)
        end = time.time()
        state.calls.save(self.options, call, end, ret)
        return ret

    def should_log(self):
        self._counter += 1

        if self._log_next > self._counter:
            return False

        self._log_next = math.floor(self._counter + 1 + self._skip)
        self._skip = self._skip * self.options.skip_multiplier

        return True


def wrap(func: Optional[Callable] = None, *,
         signature: Optional[bool] = None,
         dimensions: Optional[bool] = None,
         skip: Optional[float] = None,
         skip_multiplier: Optional[float] = None):
    if func is not None:
        if isinstance(func, types.FunctionType):
            return Wrapper(func, default_options)
    else:
        return Wrapping(Options(signature=signature,
                                dimensions=dimensions,
                                skip=skip,
                                skip_multiplier=skip_multiplier))
