import copy
from typing import Optional


class Options:
    def __init__(self, *, signature: Optional[bool] = None):
        # Log call signature
        self.signature = signature

        # These are more like TODO items
        # Log dimensions if they are tensors
        self.dimensions = True
        # Log every nth call
        self.skip = 0
        # Log every log_skip * multiplier, we exponentially increase the skip
        self.skip_multiplier = 1
        # Log primitive values such as ints, floats, strings etc
        self.primitive_values = True
        # Log lists/tuples of primitives with only few values
        self.list_limit = 5
        # Log only short strings
        self.strings_limit = 10
        # Pickle and save objects
        self.pickle = True
        # Add ids to wrappers so that we can identify them as code changes
        self.add_ids = True

        self._options = [
            'signature',
            'dimensions',
            'skip',
            'skip_multiplier',
            'primitive_values',
            'list_limit',
            'strings_limit',
            'pickle',
            'add_ids'
        ]

    @staticmethod
    def default():
        return Options(signature=True)

    def clone(self):
        return copy.deepcopy(self)

    def inherit(self, opt: 'Options'):
        for k in self._options:
            if self.__getattribute__(k) is None:
                self.__setattr__(k, opt.__getattribute__(k))
