from pathlib import Path
from typing import Any

import numpy as np
import torch

from wrap.wrapper import wrap, init_wrap

init_wrap(Path(__file__).parent.parent / 'logs')


@wrap
def my_func(param='ee', *, param2='ff'):
    print(param)


@wrap(signature=False)
def my_func_options(param):
    print(param)


@wrap
def my_func(param: Any = 'ee', *, param2: Any = 'ff'):
    print(param)


@wrap(skip=5)
def my_skip(idx: int):
    print(idx)


@wrap(skip=1, skip_multiplier=2)
def my_skip_multi(idx: int):
    print(idx)


def test():
    my_func(3)
    my_func(param='test')
    my_func_options('op_param')
    my_func(np.zeros((25, 3)))
    my_func(torch.tensor(np.ones((2, 3, 4))))
    my_func(param2=torch.tensor(np.ones((2, 3, 4))))

    for i in range(20):
        my_skip(i)

    for i in range(100):
        my_skip_multi(i)


if __name__ == '__main__':
    test()
