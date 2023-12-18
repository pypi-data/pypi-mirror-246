import threading
import time
from functools import wraps
from typing import Callable, List, TypeVar, Tuple, Any, Dict

from py_dot.core.design.invokable_value import InvokableHistoricalValue
from py_dot.core.timer import set_timeout, TimerThread

T = TypeVar('T')
LOCK = threading.Lock()

COMPOSE_INITIALIZING = None
COMPOSE_CALL = False
RECOMPUTING = {}
USING = []


class Dynamic(InvokableHistoricalValue):
    _composed: List[Callable] = []
    _uses: List['DynamicUse'] = []
    _updates: Dict['Dynamic', Any] = {}
    _update_timer: TimerThread = None

    def __init__(self, defaults: T):
        with LOCK:
            super().__init__(defaults)

    @property
    def value(self):
        with LOCK:
            return super().value

    @property
    def previous_value(self):
        with LOCK:
            return super().previous_value

    @classmethod
    def _update(cls, dynamic: 'Dynamic', value):
        with LOCK:
            if dynamic in cls._updates:
                if dynamic._previous_value == value:
                    cls._updates.pop(dynamic)
                    return

            cls._updates[dynamic] = value

            def updator():
                for update_dynamic in cls._updates:
                    update_dynamic.set(cls._updates[update_dynamic])

                    for use_function in update_dynamic._uses:
                        if use_function in USING:
                            continue

                        USING.append(use_function)

                cls._updates.clear()

                for use_function in USING:
                    use_function()
                USING.clear()

            if cls._update_timer:
                cls._update_timer.clear()

            cls._update_timer = set_timeout(updator, 0.024)

    def get(self):
        with LOCK:
            return self.get()

    def set(self, value: T):
        with LOCK:
            # if COMPUTING.get():
            #     raise Exception('Cannot Set value in Computed function')

            if self._value == value:
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
        with LOCK:
            self._uses.append(use_function)
            return self

    def __call__(self, *args) -> T:
        with LOCK:
            initializing = COMPOSE_INITIALIZING
            if initializing:
                self._composed.append(initializing)

            return super().__call__(*args)

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
        with LOCK:
            for dynamic in dynamics:
                dynamic.used(self)

            self._use_function = use_function
            self._dynamics = dynamics

    def __call__(self):
        with LOCK:
            values = []
            for dynamic in self._dynamics:
                values.append(dynamic.get())

            self._use_function(*values)


class DynamicCompose:
    def __init__(self, function):
        with LOCK:
            self._function = function
            COMPOSE_INITIALIZING = function
            self.__call__()
            COMPOSE_INITIALIZING = None

    def __call__(self):
        with LOCK:
            COMPOSE_CALL = True
            self._function()
            COMPOSE_CALL = None
