import inspect as _ins
import typing as _typing

import funcinputs as _fi

from . import _autosaving_utils
from . import argumentDict as _argumentDict
from . import argumentsDict as _argumentsDict
from ._parameter_utils import Kind as _Kind


def by_object(value, /, **kwargs) -> _fi.FuncInput:
    func = by_holder if hasattr(value, "_dest") else by_func
    return func(value, **kwargs)

def by_holder(value, /, *, namespace, **kwargs) -> _fi.FuncInput:
    cmd = by_dest(
        value._dest,
        namespace=namespace,
    )
    ansA = _fi.FuncInput(args=[cmd])
    subobj = getattr(value, cmd)
    ansB = by_object(subobj, namespace=namespace, **kwargs)
    return ansA + ansB

@_autosaving_utils.By_func_deco
class by_func:
    @classmethod
    def without_autoSave(cls, value, /, *, namespace) -> _fi.FuncInput:
        ans = _fi.FuncInput()
        signature = _ins.signature(value)
        for n, p in signature.parameters.items():
            ans += by_parameter(p, namespace=namespace)
        return ans
    @classmethod
    def with_autoSave(cls, value, /, *, namespace, autoSave) -> _fi.FuncInput:
        ansA = cls.without_autoSave(
            value,
            namespace=namespace,
        )
        autoSaveHandler = by_dest(
            autoSave.dest,
            namespace=namespace,
        )
        if _argumentDict.is_optional(autoSave.argumentDict):
            ansB = _fi.FuncInput(kwargs={autoSave.dest:autoSaveHandler})
        else:
            ansB = _fi.FuncInput(args=[autoSaveHandler])
        return ansA + ansB
            
def by_parameter(value, /, *, namespace) -> _fi.FuncInput:
    kind = _Kind.get(value)
    if kind == _Kind.VAR_KEYWORD:
        argumentsDict = _argumentsDict.by_annotation(value.annotation)
        keys = argumentsDict.keys()
        keys = list(keys)
        kwargs = {k:by_dest(k, namespace=namespace) for k in keys}
        ans = _fi.FuncInput(kwargs=kwargs)
        return ans
    v = by_dest(value.name, namespace=namespace)
    if kind == _Kind.SIMPLY_POSITIONAL:
        return _fi.FuncInput(args=[v])
    if kind == _Kind.VAR_POSITIONAL:
        return _fi.FuncInput(args=v)
    if kind == _Kind.KEYWORD_ONLY:
        return _fi.FuncInput(kwargs={value.name:v})
    raise NotImplementedError

def by_dest(value, /, *, namespace) -> _typing.Any:
    ans = getattr(namespace, value)
    delattr(namespace, value)
    return ans
