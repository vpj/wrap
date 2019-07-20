from wrap.wrapper import wrap


@wrap
def my_func(param):
    print(param)


@wrap()
def my_func_options(param):
    print(param)


def test():
    my_func(3)
    my_func('test')
    my_func_options('op_param')


if __name__ == '__main__':
    test()
