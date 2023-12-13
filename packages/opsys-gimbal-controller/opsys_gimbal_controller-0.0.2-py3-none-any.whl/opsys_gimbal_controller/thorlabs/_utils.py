"Utilities"
from ctypes import (
    CDLL,
    CFUNCTYPE,
    c_ushort,
    c_ulong,
    c_short,
    c_char_p,
    c_int
)
from typing import (
    Any,
    List,
)

c_word = c_ushort
c_dword = c_ulong


def bind(lib: CDLL, func: str,
         argtypes: List[Any] = None, restype: Any = None) -> CFUNCTYPE:
    _func = getattr(lib, func, null_function)
    _func.argtypes = argtypes
    _func.restype = restype

    return _func


def null_function():
    pass


__all__ = [
    bind,
    null_function,
    c_word,
    c_dword,
]


class ThorlabsConfiguration:
    TOTAL_STEPS_PER_ROUND = 409600
    DEGREES_PER_ROUND = 5.4546
    SERIAL_NUMBER = c_char_p(bytes("40231214", "utf-8"))
    CHANNEL = c_short(1)
    STEP_ANGLE = 11.25
    MILLISECONDS = c_int(10)
    ACCELERATION = 826  # 1deg/s^2
    MAX_VELOCITY = 4031547  # 1deg/s
    ACCURACY = 0.0001
