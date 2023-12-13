import argparse as _ap
import inspect as _ins
import typing as _typing

_LEGAL_ACTIONS = [
    'store', 
    'store_const', 
    'append', 
    'append_const', 
    'help', 
    'version',
]

def is_optional(
    value:dict, 
    /,
) -> bool:
    value = dict(value)
    option_strings = value.get('option_strings', [])
    option_strings = list(option_strings)
    return bool(len(option_strings))

def by_annotation(
    value:_typing.Any, 
    /,
) -> dict:
    if value is _ins.Parameter.empty:
        return {}
    if callable(value):
        return {'type': value}
    if type(value) is str:
        return {'help': value}  
    return dict(value)

def add_to_parser(
    value:dict, 
    /, 
    parser:_ap.ArgumentParser, 
    *, 
    dest:str,
) -> None:
    value = dict(value)
    value['action'] = value.get('action', 'store')
    if value['action'] not in _LEGAL_ACTIONS:
        raise ValueError
    option_strings = value.pop('option_strings', [])
    parser.add_argument(
        *option_strings, 
        dest=dest, 
        **value,
    )
