import argparse as _ap
import inspect as _ins

from . import argumentsDict as _argumentsDict


def _get_prefix_char(parser):
    prefix_chars = parser.prefix_chars
    try:
        return prefix_chars[0]
    except IndexError:
        return None

def by_object(value, /, **kwargs):
    func = by_holder if hasattr(value, "_dest") else by_func
    return func(value, **kwargs)

def by_holder(value, /, **kwargs):
    ans = _ap.ArgumentParser(
        description=value.__doc__,
        **kwargs,
    )
    subparsers = ans.add_subparsers(dest=value._dest, required=True)
    for n, m in _ins.getmembers(value):
        if n.startswith("_"):
            continue
        cmd = n
        prefix_char = _get_prefix_char(ans)
        if prefix_char is not None:
            cmd = cmd.replace('_', prefix_char)
        inner_kwargs = dict(kwargs)
        inner_kwargs.pop('parents', None)
        inner_kwargs['prog'] = cmd
        parent = by_object(
            m,
            **inner_kwargs,
        )
        inner_kwargs['description'] = parent.description
        inner_kwargs['add_help'] = False
        inner_kwargs.pop('autoSave', None)
        subparser = subparsers.add_parser(
            cmd,
            parents=[parent],
            **inner_kwargs,
        )
    return ans

def by_func(
    value, 
    /, 
    *, 
    autoSave=None,
    **kwargs,
):
    ans = _ap.ArgumentParser(
        description=value.__doc__,
        **kwargs,
    )
    prefix_char = _get_prefix_char(ans)
    argumentsDict = _argumentsDict.by_func(
        value, 
        prefix_char=prefix_char,
        autoSave=autoSave,
    )
    _argumentsDict.add_to_parser(
        argumentsDict,
        parser=ans,
    )
    return ans

def by_parameter(value, /, **kwargs):
    ans = _ap.ArgumentParser(
        **kwargs,
    )
    prefix_char = _get_prefix_char(ans)
    argumentsDict = _argumentsDict.by_parameter(
        value, 
        prefix_char=prefix_char,
    )
    _argumentsDict.add_to_parser(
        argumentsDict,
        parser=ans,
    )
    return ans

def by_argumentsDict(value, /, **kwargs):
    ans = _ap.ArgumentParser(**kwargs)
    _argumentsDict.add_to_parser(
        value, 
        parser=ans,
    )
    return ans
