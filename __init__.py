try:
    import binaryninja
    from .qresource import QResource
except ImportError:
    # unittests are executed without access to binaryninja api
    pass


