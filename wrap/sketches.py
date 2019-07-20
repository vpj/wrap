import types


class Wrap:
    def __init__(self):
        self.configs = 1

    def wrap_with_option(self, func, options):
        return Wrapper(func, options)

    def wrap(self, *args, **kwargs):
        print(self)
        print(args)
        print(kwargs)
        assert len(args) > 0

        if isinstance(args[0], types.FunctionType):
            return Wrapper(args[0], None)
        else:
            return Wrapping(args[0], self)


wrap_instance = Wrap()


class Wrapping:
    def __init__(self, options, wi: Wrap):
        self.options = options
        self.wi = wi

    def __call__(self, func):
        return self.wi.wrap_with_option(func, self.options)


class Wrapper:
    def __init__(self, func, options):
        self.options = options
        self.func = func

    def __call__(self, *args, **kwargs):
        print(self.options, ':')
        self.func(*args, **kwargs)


def wrap(*args, **kwargs):
    return wrap_instance.wrap(*args, **kwargs)


@wrap
def my_func(param):
    print(param)


@wrap_instance.wrap
def my_func2(param):
    print(param)


@wrap('options')
def my_func_options(param):
    print(param)


def test():
    my_func(3)
    my_func('test')
    my_func_options('op_param')


if __name__ == '__main__':
    test()
