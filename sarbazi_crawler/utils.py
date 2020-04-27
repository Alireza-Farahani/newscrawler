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


def remove_unicode_whitespaces(value: str):
    return value.replace('\xa0', '')
# class TakeLast(object):
#
#     def __call__(self, values: Iterable):
#         for value in values:
#             if value is not None and value != '':
#                 return value

# def is_iterable(obj) -> bool:
#     try:
#         iter(obj)
#     except TypeError:
#         return False
#     else:
#         return True
