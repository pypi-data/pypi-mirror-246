import inspect as _ins


class By_func_deco:
    def _autoSave_is_usable(self, autoSave, *, value):
        if autoSave is None:
            return False
        if _ins.signature(value).return_annotation is None:
            return False
        return True
    def __init__(self, original):
        self._original = original
    def __call__(self, value, /, *, autoSave=None, **kwargs):
        if self._autoSave_is_usable(
            autoSave=autoSave, 
            value=value,
        ):
            return self._original.with_autoSave(
                value,
                **kwargs,
                autoSave=autoSave,
            )
        else:
            return self._original.without_autoSave(
                value,
                **kwargs,
            )

