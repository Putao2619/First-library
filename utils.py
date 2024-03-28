import copy
class Jdict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    def __deepcopy__(self, memo=None):
        return Jdict(copy.deepcopy(dict(self), memo=memo))