from typing import TypeVar

T = TypeVar('T')


class InvokableValue:
    _value: T

    def __init__(self, value: T):
        self._value = T

    def get(self) -> T:
        return self._value

    def set(self, value: T):
        self._value = value
        return value

    @property
    def value(self):
        return self._value

    def __call__(self, *args) -> T:
        if len(args) == 1:
            return self.set(*args)

        return self._value


class InvokableHistoricalValue(InvokableValue):
    _previous_value: T

    def __init__(self, value: T):
        super().__init__(value)

        self._previous_value = None

    @property
    def previous_value(self):
        return self._previous_value

    def set(self, value: T):
        self._previous_value = self._value

        return super().set(value)
