import inspect as _ins
from enum import Enum


class Kind(Enum):
    VAR_POSITIONAL = 2
    KEYWORD_ONLY = 3
    VAR_KEYWORD = 4  
    SIMPLY_POSITIONAL = 5
    @classmethod
    def get(cls, value, /):
        if type(value) is _ins.Parameter:
            value = value.kind
        value = int(value)
        value = {0:5, 1:5}.get(value, value)
        value = cls(value)
        return value
