import threading


class ThreadSafe:
    _lock: threading.Lock

    def __init__(self, value):
        self._value = value
        self._lock = threading.Lock()

    def set(self, value):
        with self._lock:
            self._value = value

    def get(self):
        return self._value

    def __call__(self):
        return self._value


class ThreadSafeList:
    def __init__(self):
        self._list = []
        self._lock = threading.Lock()

    def append(self, item):
        with self._lock:
            self._list.append(item)

    def pop(self, index=-1):
        with self._lock:
            return self._list.pop(index)

    def __str__(self):
        with self._lock:
            return str(self._list)


class ThreadSafeDict:
    def __init__(self):
        self._dictionary = {}
        self._lock = threading.Lock()

    def __getitem__(self, key):
        with self._lock:
            return self._dictionary[key]

    def __setitem__(self, key, value):
        with self._lock:
            self._dictionary[key] = value

    def __delitem__(self, key):
        with self._lock:
            del self._dictionary[key]

    def __contains__(self, key):
        with self._lock:
            return key in self._dictionary
    def __str__(self):
        with self._lock:
            return str(self._dictionary)

    def keys(self):
        with self._lock:
            return list(self._dictionary.keys())

    def values(self):
        with self._lock:
            return list(self._dictionary.values())

    def items(self):
        with self._lock:
            return list(self._dictionary.items())