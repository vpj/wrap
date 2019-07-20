import types
from pathlib import Path
from typing import Callable, Optional, Union

from wrap.definitions import Definition
from wrap.options import Options

default_options = Options.default()


class Configs:
    def __init__(self, log_dir: Path):
        self.log_dir: Path = log_dir
        if not self.log_dir.exists():
            self.log_dir.mkdir(parents=True)
        self.definitions_path = str(self.log_dir / 'definitions.json')


configs: Optional[Configs] = None


def init_wrap(log_dir: Union[str, None, Path]):
    global configs

    if log_dir is not None:
        if type(log_dir) == Path:
            log_dir = log_dir
        else:
            log_dir = Path(log_dir)

    configs = Configs(log_dir)


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
        self.log_definition()

    def log_definition(self):
        definition = Definition(self.func)
        with open(configs.definitions_path, "a") as f:
            f.write(definition.json_str() + '\n')

    def __call__(self, *args, **kwargs):
        print(self.options, ':')
        self.func(*args, **kwargs)


def wrap(func: Optional[Callable] = None, *,
         signature: Optional[bool] = None):
    if func is not None:
        if isinstance(func, types.FunctionType):
            return Wrapper(func, default_options)
    else:
        return Wrapping(Options(signature=signature))
