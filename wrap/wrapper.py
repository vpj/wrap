import types

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


def wrap(*args, **kwargs):
    print(args)
    print(kwargs)
    assert len(args) > 0

    if isinstance(args[0], types.FunctionType):
        return Wrapper(args[0], default_options)
    else:
        return Wrapping(args[0])


@wrap
def my_func(param):
    print(param)


@wrap(Options())
def my_func_options(param):
    print(param)


def test():
    my_func(3)
    my_func('test')
    my_func_options('op_param')


if __name__ == '__main__':
    test()
