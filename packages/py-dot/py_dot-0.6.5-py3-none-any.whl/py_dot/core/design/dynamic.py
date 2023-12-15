import threading
import time
from functools import wraps
from typing import Callable, List, TypeVar, Tuple, Any, Dict

from py_dot.core.thread.thread_safe import ThreadSafe, ThreadSafeDict, ThreadSafeList
from py_dot.core.timer import set_timeout, TimerThread

COMPOSE_INITIALIZING = ThreadSafe(None)
COMPOSE_CALL = ThreadSafe(False)
RECOMPUTING = ThreadSafeDict()

T = TypeVar('T')

USING = ThreadSafeList()


class Dynamic:
    _composed: List[Callable] = []

    _uses: List['DynamicUse'] = []

    _previous_value: ThreadSafe
    _current_value: ThreadSafe

    _updates: Dict['Dynamic', Any] = {}
    _update_timer: TimerThread = None

    def __init__(self, defaults: T):
        self._previous_value = ThreadSafe(None)
        self._current_value = ThreadSafe(defaults)

    def __call__(self) -> T:
        initializing = COMPOSE_INITIALIZING()
        if initializing:
            self._composed.append(initializing)

        return self.get()

    @classmethod
    def _update(cls, dynamic: 'Dynamic', value):

        if dynamic in cls._updates:
            if dynamic._previous_value.get() == value:
                cls._updates.pop(dynamic)
                return

        cls._updates[dynamic] = value

        def updator():
            for update_dynamic in cls._updates:
                update_dynamic._previous_value.set(dynamic.current_value)
                update_dynamic._current_value.set(cls._updates[update_dynamic])

                for use_function in update_dynamic._uses:
                    if use_function in USING.get():
                        continue

                    USING.append(use_function)

            cls._updates.clear()

            for use_function in USING():
                use_function()
            USING.clear()

        if cls._update_timer:
            cls._update_timer.clear()

        cls._update_timer = set_timeout(updator, 0.024)

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

        self.__class__._update(self, value)

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

    def used(self, use_function):
        self._uses.append(use_function)
        return self

    @staticmethod
    def compose(target: Callable):
        computed_ = DynamicCompose(target)
        return computed_

    @staticmethod
    def use(*args: 'Dynamic'):
        def use_decorator(target: Callable):
            dynamic_use = DynamicUse(target, args)

            dynamic_use()

            return dynamic_use

        return use_decorator


class DynamicUse:
    _use_function: Callable

    def __init__(self, use_function: Callable, dynamics: Tuple[Dynamic]):
        for dynamic in dynamics:
            dynamic.used(self)

        self._use_function = use_function
        self._dynamics = dynamics

    def __call__(self):

        values = []
        for dynamic in self._dynamics:
            values.append(dynamic.get())

        self._use_function(*values)


class DynamicCompose:
    def __init__(self, function):
        self._function = function

        COMPOSE_INITIALIZING.set(function)
        self.__call__()
        COMPOSE_INITIALIZING.set(None)

    def __call__(self):
        COMPOSE_CALL.set(True)
        self._function()
        COMPOSE_CALL.set(None)
