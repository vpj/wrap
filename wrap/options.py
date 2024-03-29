import copy
from typing import Optional


class Options:
    def __init__(self, *,
                 key: Optional[str] = None,
                 signature: Optional[bool] = None,
                 dimensions: Optional[bool] = None,
                 skip: Optional[float] = None,
                 skip_multiplier: Optional[float] = None):
        self.key = key

        # Log call signature
        self.signature = signature
        # Log dimensions if they are tensors
        self.dimensions = dimensions
        # Log every nth call
        self.skip = skip
        # Log every log_skip * multiplier, we exponentially increase the skip
        self.skip_multiplier = skip_multiplier

        # These are more like TODO items
        # Add ids to wrappers so that we can identify them as code changes
        self.add_key = False
        # Log primitive values such as ints, floats, strings etc
        self.primitive_values = True
        # Log lists/tuples/dicts of primitives with only few values
        self.list_limit = 5
        # Log only short strings
        self.strings_limit = 10
        # Pickle and save objects
        self.pickle = True

        self._options = [
            'signature',
            'dimensions',
            'skip',
            'skip_multiplier',
            'primitive_values',
            'list_limit',
            'strings_limit',
            'pickle',
            'add_key'
        ]

    @staticmethod
    def default():
        return Options(key=None,
                       signature=True,
                       dimensions=True,
                       skip=0,
                       skip_multiplier=1)

    def clone(self):
        return copy.deepcopy(self)

    def inherit(self, opt: 'Options'):
        for k in self._options:
            if self.__getattribute__(k) is None:
                self.__setattr__(k, opt.__getattribute__(k))

    def __repr__(self):
        return f"signature={self.signature}"
