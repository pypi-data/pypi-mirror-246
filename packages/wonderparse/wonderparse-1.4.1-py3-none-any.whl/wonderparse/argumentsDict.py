import argparse as _ap
import inspect as _ins

from . import _autosaving_utils
from . import argumentDict as _argumentDict
from . import option_string as _option_string
from ._parameter_utils import Kind as _Kind


def organized(value:dict, /):
    value = dict(value)
    optional = dict()
    non_optional = dict()
    for dest, argumentDict in value.items():
        if _argumentDict.is_optional(argumentDict):
            optional[dest] = argumentDict
        else:
            non_optional[dest] = argumentDict
    ans = dict(**optional, **non_optional)
    return ans

def add_to_parser(
    value:dict, 
    /, 
    parser:_ap.ArgumentParser, 
    *, 
    organize:bool=True,
):
    if organize:
        value = organized(value)
    else:
        value = dict(value)
    for dest, argumentDict in value.items():
        _argumentDict.add_to_parser(
            argumentDict, 
            dest=dest,
            parser=parser, 
        )

def by_annotation(value:dict, /):
    if value is _ins.Parameter.empty:
        return dict()
    value = dict(value)
    ans = dict()
    for dest, y in value.items():
        ans[dest] = _argumentDict.by_annotation(y)
    return ans


@_autosaving_utils.By_func_deco
class by_func:
    @classmethod
    def without_autoSave(cls, value, /, *, prefix_char):
        ans = dict()
        signature = _ins.signature(value)
        for n, p in signature.parameters.items():
            part = by_parameter(p, prefix_char=prefix_char)
            ans = dict(**ans, **part)
        return ans
    @classmethod
    def with_autoSave(cls, value, /, *, autoSave, **kwargs):
        ansA = cls.without_autoSave(value, **kwargs)
        ansB = dict([autoSave])
        ans = dict(**ansA, **ansB)
        return ans


def by_parameter(value:dict, /, *, prefix_char=None):
    if value.name.startswith('_'):
        raise ValueError(value.name)
    annotation = value.annotation
    kind = _Kind.get(value)
    if kind == _Kind.VAR_KEYWORD:
        if annotation is _ins.Parameter.empty:
            return dict()
        else:
            return dict(annotation)
    argumentDictA = _argumentDict.by_annotation(annotation)
    argumentDictB = dict()
    if kind == _Kind.SIMPLY_POSITIONAL:
        if value.default is not _ins.Parameter.empty:
            argumentDictB['nargs'] = '?'
            argumentDictB['default'] = value.default
    elif kind == _Kind.VAR_POSITIONAL:
        argumentDictB['nargs'] = '*'
        argumentDictB['default'] = tuple()
    elif kind == _Kind.KEYWORD_ONLY:
        if 'option_strings' not in argumentDictA.keys():
            option_string = _option_string.by_dest_metavar_and_prefix_char(
                dest=value.name,
                metavar=argumentDictA.get('metavar'),
                prefix_char=prefix_char,
            )
            argumentDictA['option_strings'] = [option_string]
        if value.default is _ins.Parameter.empty:
            argumentDictB['required'] = True
        else:
            argumentDictB['required'] = False
            argumentDictB['default'] = value.default
    else:
        raise NotImplementedError
    argumentDict = dict(
        **argumentDictB, 
        **argumentDictA,
    )
    ans = {value.name:argumentDict}
    return ans
