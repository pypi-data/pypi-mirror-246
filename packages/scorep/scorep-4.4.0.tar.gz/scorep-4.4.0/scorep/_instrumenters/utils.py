from scorep._bindings import abspath
from scorep.instrumenter import has_c_instrumenter


def get_module_name(frame):
    """Get the name of the module the given frame resides in"""
    modulename = frame.f_globals.get("__name__", None)
    if modulename is None:
        # this is a NUMPY special situation, see NEP-18, and Score-P Issue
        # issues #63
        if frame.f_code.co_filename == "<__array_function__ internals>":
            modulename = "numpy.__array_function__"
        else:
            modulename = "unkown"
    typeobject = frame.f_locals.get("self", None)
    if typeobject is not None:
        if has_c_instrumenter():
            return ".".join([modulename, type(typeobject).__name__])
        else:
            return ".".join([modulename, typeobject.__class__.__name__])
    return modulename


def get_file_name(frame):
    """Get the full path to the file the given frame resides in"""
    file_name = frame.f_code.co_filename
    if file_name is not None:
        full_file_name = abspath(file_name)
    else:
        full_file_name = "None"
    return full_file_name
