import threading

from py_dot.core.design.invokable_value import InvokableValue

LOCK = threading.Lock()


class ThreadSafe(InvokableValue):
    def set(self, value):
        with LOCK:
            return super().set(value)

    def get(self):
        with LOCK:
            return super().get()

    def __call__(self, *args):
        with LOCK:
            return super().__call__(*args)


class ThreadSafeList(list):
    def append(self, *args, **kwargs):
        with LOCK:
            return super().append(*args, **kwargs)

    def extend(self, *args, **kwargs):
        with LOCK:
            return super().extend(*args, **kwargs)

    def pop(self, *args, **kwargs):
        with LOCK:
            return super().pop(*args, **kwargs)

    def index(self, *args, **kwargs):
        with LOCK:
            return super().index(*args, **kwargs)

    def count(self, *args, **kwargs):
        with LOCK:
            return super().count(*args, **kwargs)

    def insert(self, *args, **kwargs):
        with LOCK:
            return super().insert(*args, **kwargs)

    def remove(self, *args, **kwargs):
        with LOCK:
            return super().remove(*args, **kwargs)

    def sort(self, *args, **kwargs):
        with LOCK:
            return super().sort(*args, **kwargs)

    def __len__(self):
        with LOCK:
            return super().__len__()

    def __iter__(self):
        with LOCK:
            return super().__iter__()

    def __getitem__(self, *args, **kwargs):
        with LOCK:
            return super().__getitem__(*args, **kwargs)

    def __add__(self, *args, **kwargs):
        with LOCK:
            return super().__add__(*args, **kwargs)

    def __iadd__(self, *args, **kwargs):
        with LOCK:
            return super().__iadd__(*args, **kwargs)

    def __mul__(self, *args, **kwargs):
        with LOCK:
            return super().__mul__(*args, **kwargs)

    def __rmul__(self, *args, **kwargs):
        with LOCK:
            return super().__rmul__(*args, **kwargs)

    def __contains__(self, *args, **kwargs):
        with LOCK:
            return super().__contains__(*args, **kwargs)

    def __reversed__(self):
        with LOCK:
            return super().__reversed__()

    def __gt__(self, *args, **kwargs):
        with LOCK:
            return super().__gt__(*args, **kwargs)

    def __ge__(self, *args, **kwargs):
        with LOCK:
            return super().__ge__(*args, **kwargs)

    def __le__(self, *args, **kwargs):
        with LOCK:
            return super().__le__(*args, **kwargs)

    def __eq__(self, *args, **kwargs):
        with LOCK:
            return super().__eq__(*args, **kwargs)

    def __getitem__(self, *args, **kwargs):
        with LOCK:
            return super().__getitem__(*args, **kwargs)


class ThreadSafeDict(dict):
    def clear(self):
        with LOCK:
            return super().clear()

    def copy(self):
        with LOCK:
            return super().copy()

    @staticmethod  # known case
    def fromkeys(*args, **kwargs):
        with LOCK:
            return super().fromkeys(*args, **kwargs)

    def get(self, *args, **kwargs):
        with LOCK:
            return super().get(*args, **kwargs)

    def items(self):
        with LOCK:
            return super().items()

    def keys(self):
        with LOCK:
            return super().keys()

    def pop(self, k, d=None):
        with LOCK:
            return super().pop(k, d)

    def popitem(self):
        with LOCK:
            return super().popitem()

    def setdefault(self, *args, **kwargs):
        with LOCK:
            return super().setdefault(*args, **kwargs)

    def update(self, E=None, **F):
        with LOCK:
            return super().update(E, **F)

    def values(self):
        with LOCK:
            return super().values()

    def __class_getitem__(self, *args, **kwargs):
        with LOCK:
            return super().__class_getitem__(*args, **kwargs)

    def __contains__(self, *args, **kwargs):
        with LOCK:
            return super().__contains__(*args, **kwargs)

    def __delitem__(self, *args, **kwargs):
        with LOCK:
            return super().__delitem__(*args, **kwargs)

    def __eq__(self, *args, **kwargs):
        with LOCK:
            return super().__eq__(*args, **kwargs)

    def __getattribute__(self, *args, **kwargs):
        with LOCK:
            return super().__getattribute__(*args, **kwargs)

    def __getitem__(self, y):
        with LOCK:
            return super().__getitem__(y)

    def __ge__(self, *args, **kwargs):
        with LOCK:
            return super().__ge__(*args, **kwargs)

    def __gt__(self, *args, **kwargs):
        with LOCK:
            return super().__gt__(*args, **kwargs)

    def __init__(self, seq=None, **kwargs):
        with LOCK:
            super().__init__(seq=seq, **kwargs)

    def __ior__(self, *args, **kwargs):
        with LOCK:
            return super().__ior__(*args, **kwargs)

    def __iter__(self):
        with LOCK:
            return super().__iter__()

    def __len__(self):
        with LOCK:
            return super().__len__()

    def __le__(self, *args, **kwargs):
        with LOCK:
            return super().__le__(*args, **kwargs)

    def __lt__(self, *args, **kwargs):
        with LOCK:
            return super().__lt__(*args, **kwargs)

    @staticmethod
    def __new__(*args, **kwargs):
        with LOCK:
            return super().__new__(*args, **kwargs)

    def __ne__(self, *args, **kwargs):
        with LOCK:
            return super().__ne__(*args, **kwargs)

    def __or__(self, *args, **kwargs):
        with LOCK:
            return super().__or__(*args, **kwargs)

    def __repr__(self, *args, **kwargs):
        with LOCK:
            return super().__repr__(*args, **kwargs)

    def __reversed__(self):
        with LOCK:
            return super().__reversed__()

    def __ror__(self, *args, **kwargs):
        with LOCK:
            return super().__ror__(*args, **kwargs)

    def __setitem__(self, *args, **kwargs):
        with LOCK:
            return super().__setitem__(*args, **kwargs)

    def __sizeof__(self):
        with LOCK:
            return super().__sizeof__()
