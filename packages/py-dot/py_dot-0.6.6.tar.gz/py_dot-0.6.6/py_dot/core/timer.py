from threading import Thread, Event
from time import sleep
from typing import Callable, Union


class TimerThread(Thread):
    event: Event
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.event = Event()

    def clear(self):
        self.event.set()


def set_timeout(
        callback: Callable, delay: Union[int, float],
        daemon=False,
        start=True
) -> TimerThread:
    """ Set Timer to Run after delay

    Print after 3s:
    >>> def foo(timer_: Event):
    ...     print('foo')
    ... timer = set_timeout(foo, 3)


    Disable Timer:
    >>> timer.clear()
    """

    def set_timeout_thread():
        sleep(delay)

        if not thread.event.is_set():
            callback()

    thread = TimerThread(target=set_timeout_thread, daemon=daemon)

    if start:
        thread.start()

    return thread


def set_interval(
        callback: Callable,
        delay: int,
        start=True,
        daemon=False
):
    """ Set Timer to Run per delay

    Print per 3s:
    >>> def foo():
    ...     print('foo')
    ... timer = set_interval(foo, 3)


    Disable Timer:
    >>> timer.clear()
    """

    def set_interval_thread():
        # index = 0
        while not thread.event.is_set():
            sleep(delay)
            callback()
            # index += 1

    thread = TimerThread(target=set_interval_thread, daemon=daemon)

    if start:
        print('start thread')
        thread.start()

    return thread


def timeout(
        delay: Union[int, float],
        daemon=False,
        start=True
):
    """ set_timeout sugar decorator

    Print after 3s
    >>> @timeout(3)
    ... def foo(timer: Event):
    ...     print('foo')

    Disable Timer:
    >>> foo.set()
    """

    def set_timeout_decorator(callback: Callable):
        return set_timeout(callback, delay, daemon=daemon, start=start)

    return set_timeout_decorator


def interval(
        delay: int,
        daemon=False,
        start=True
):
    """ set_interval sugar decorator

    Print per 3s
    >>> @interval(3)
    ... def foo(timer: Event, index: int):
    ...     print('foo')

    Disable Timer:
    >>> foo.clear()
    """

    def set_interval_decorator(callback: Callable):
        return set_interval(callback, delay, daemon=daemon, start=start)

    return set_interval_decorator
