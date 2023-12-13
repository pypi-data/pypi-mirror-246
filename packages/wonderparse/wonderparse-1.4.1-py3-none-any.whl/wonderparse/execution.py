import inspect as _ins
import typing as _typing

from . import _autosaving_utils
from . import argumentDict as _argumentDict


def by_object(value, /, **kwargs):
    func = by_holder if hasattr(value, "_dest") else by_func
    return func(
        value, 
        **kwargs,
    )

def by_holder(value, /, *, funcInput, **kwargs):
    funcInput = funcInput.copy()
    cmd = funcInput.pop(0)
    value = getattr(value, cmd)
    return by_object(
        value, 
        funcInput=funcInput,
        **kwargs,
    )

@_autosaving_utils.By_func_deco
class by_func:
    @classmethod
    def with_autoSave(cls, value, /, *, funcInput, autoSave):
        if _argumentDict.is_optional(autoSave.argumentDict):
            autoSaveHandler = funcInput.pop(autoSave.dest)
        else:
            autoSaveHandler = funcInput.pop(-1)
        returnvalue = cls.without_autoSave(
            value,
            funcInput=funcInput,
        )
        return autoSaveHandler.write(returnvalue)
    @classmethod
    def without_autoSave(cls, value, /, *, funcInput):
        ans = funcInput.exec(value)
        sig = _ins.signature(value)
        returntype = sig.return_annotation
        if returntype in [_ins.Parameter.empty, _typing.Any]:
            return ans
        if returntype is not None:
            return returntype(ans)
        if ans is None:
            return None
        raise ValueError(f"""\
The function {value.__name__} returned {ans}, \
but it's return annotation is None.""")
