import inspect


def get_class_that_defined_method(meth):
    if inspect.ismethod(meth):
        for cls in inspect.getmro(meth.__self__.__class__):
            if cls.__dict__.get(meth.__name__) is meth:
                return cls
        meth = meth.__func__  # fallback to __qualname__ parsing
    if inspect.isfunction(meth):
        if not hasattr(meth, '__qualname__'):
            pass  # python too old
        else:
            try:
                cls = getattr(
                    inspect.getmodule(meth),
                    meth.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0]
                )  # yapf: disable
            except AttributeError:  # defined in an exec() on new python?
                cls = 'exec'
            if isinstance(cls, type):
                return cls
    return None
