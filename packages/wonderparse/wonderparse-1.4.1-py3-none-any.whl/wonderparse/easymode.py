from . import autosaving as _autosaving
from . import execution as _execution
from . import parser as _parser
from . import process_namespace as _process_namespace


def simple_run(*, 
    args, 
    program_object,
    endgame='print',
    edit_namespace=None,
    **kwargs,
):
    finalTouch = _finalTouch(endgame)
    autoSave = _autoSave(endgame)
    parser = _parser.by_object(
        program_object, 
        autoSave=autoSave,
        **kwargs,
    )
    ns = parser.parse_args(args)
    if edit_namespace is not None:
        edit_namespace(ns)
    funcInput = _process_namespace.by_object(
        program_object, 
        namespace=ns,
        autoSave=autoSave,
    )
    if len(vars(ns)):
        raise ValueError(f"Some arguments in the namespace were not processed: {ns}")
    try:
        result = _execution.by_object(
            program_object, 
            funcInput=funcInput,
            autoSave=autoSave,
        )
    except Exception as exc:
        msg = _exit_msg(
            prog=kwargs.get('prog'),
            exc=exc,
        )
        raise SystemExit(msg)
    return finalTouch(result)

def _exit_msg(
    *,
    prog,
    exc,
):
    if prog is None:
        msgA = f"{type(exc)}"
    else:
        msgA = f"Running {prog} failed because of {type(exc)}"
    msg = f"{msgA}: {exc}"
    return msg

def _autoSave(value, /):
    if type(value) is _autosaving.AutoSave:
        return value
    return None

def _finalTouch(value, /):
    if type(value) is _autosaving.AutoSave:
        return _return
    if type(value) is not str:
        return value
    if value == 'print':
        return print
    if value == 'iterprint':
        return iterprint
    if value == 'return':
        return _return
    raise ValueError(f"{value.__repr__()} is not a legal value for endgame.")
    
def iterprint(values):
    for value in values:
        print(value)

def _return(value):
    return value

