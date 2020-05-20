from typing import Iterable, Sequence


class TakeLast(object):

    def __call__(self, values: Iterable):
        if isinstance(values, Sequence):
            return values[-1]
        try:
            item = None
            for item in values:
                pass
            return item
        except TypeError:
            return None


class DropLast(object):

    def __call__(self, values: Sequence):
        return values[:-1]


class Replace(object):
    def __init__(self, old, new):
        self.old = old
        self.new = new

    def __call__(self, value: str):
        return value.replace(self.old, self.new)


def remove_unicode_whitespaces(value: str):
    return Replace('\xa0', '')(value)
