from pathlib import Path

from wrap.wrapper import wrap, init_wrap

init_wrap(Path(__file__).parent.parent / 'logs')


@wrap
def my_func(param='ee', *, param2='ff'):
    print(param)


@wrap(signature=False)
def my_func_options(param):
    print(param)


def test():
    my_func(3)
    my_func('test')
    my_func_options('op_param')


if __name__ == '__main__':
    test()
