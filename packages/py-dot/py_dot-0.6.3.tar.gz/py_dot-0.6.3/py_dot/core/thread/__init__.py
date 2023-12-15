import time
from functools import wraps
from threading import Thread, Event
from typing import Callable


class EventThread(Thread):
    event = Event()

    def set(self):
        self.event.set()

    def is_set(self):
        return self.event.is_set()

    def set_join(self):
        self.event.set()
        self.join()

class RepeatThread(EventThread):
    def __init__(
            self,
            group=None,
            target=None,
            *args,
            **kwargs
    ):
        repeat_rate = kwargs.get('repeat_rate', 0.24)

        if target:
            def repeat_target(*thread_args, **thread_kwargs):
                while not self.event.is_set():
                    target(*thread_args, **thread_kwargs)
                    time.sleep(repeat_rate)

        super().__init__(*args, **kwargs)


def thread_start(
        target: Callable,
        thread_class=EventThread,
        *args,
        **kwargs
):
    thread = thread_class(target=target, *args, **kwargs)
    thread.start()
    return thread


def thread_run(
        thread_class=EventThread,
        *args,
        **kwargs
):
    def thread_run_wrap(target: Callable) -> Thread:
        thread = thread_class(target=target, *args, **kwargs)
        thread.start()

        return thread

    return thread_run_wrap


def thread_make(
        thread_class=EventThread,
        *common_args, **common_kwargs
):
    """ Sugar of () -> threading.Thread()

    >>> @thread_make()
    >>> def test():
    >>>     print('tested !')
    >>>
    >>> thread = test()
    >>> thread.start()
    >>> thread.join()
    """

    def thread_make_decorator(target: Callable):
        @wraps(target)
        def thread_make_wrap(*args, **kwargs):
            thread = thread_class(target=target, *common_args, *args, **common_kwargs, **kwargs)
            thread.start()

            return thread

        return thread_make_wrap

    return thread_make_decorator
