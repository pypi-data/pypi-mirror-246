import threading
import time
from functools import wraps
from typing import Callable, List, TypeVar

from py_dot.core.thread.thread_safe import ThreadSafe, ThreadSafeDict

INITIALIZING = ThreadSafe(None)
COMPUTING = ThreadSafe(False)
RECOMPUTING = ThreadSafeDict()

T = TypeVar('T')


class Dynamic:
    _composed: List[Callable] = []
    _previous_value: ThreadSafe
    _current_value: ThreadSafe

    def __init__(self, defaults: T):
        self._previous_value = ThreadSafe(None)
        self._current_value = ThreadSafe(defaults)

    def previous_value(self):
        return self._previous_value()

    def current_value(self):
        return self._current_value.get()

    def get(self) -> T:
        return self.current_value()

    def set(self, value: T):

        # if COMPUTING.get():
        #     raise Exception('Cannot Set value in Computed function')

        if self._current_value.get() == value:
            return

        self._previous_value.set(self._current_value.get())
        self._current_value.set(value)

        threads = []
        events = []

        for computed_function in self._composed:
            if computed_function in RECOMPUTING:
                continue

            @wraps(computed_function)
            def target(event_: threading.Event):
                while not event_.is_set():
                    time.sleep(0.24)

                if computed_function in RECOMPUTING:
                    RECOMPUTING.__delitem__(computed_function)

                computed_function()

            event = threading.Event()
            thread = threading.Thread(
                target=target,
                args=(event,),
                name='signal_computed'
            )
            thread.start()

            RECOMPUTING[computed_function] = thread
            threads.append(thread)
            events.append(event)

        for event in events:
            event.set()

        for thread in threads:
            thread.join()

    def __call__(self) -> T:
        initializing = INITIALIZING()
        if initializing:
            self._composed.append(initializing)

        return self.get()

    @staticmethod
    def compose(target: Callable):
        computed_ = SignalCompose(target)
        return computed_


class SignalCompose:
    def __init__(self, function):
        self._function = function

        INITIALIZING.set(function)
        self.__call__()
        INITIALIZING.set(None)

    def __call__(self):
        COMPUTING.set(True)
        self._function()
        COMPUTING.set(None)
