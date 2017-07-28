_version_tuple = (1, 0, 0)
__version__ = '.'.join(str(e) for e in _version_tuple)


def version():
    """Return back the current version
    """

    return _version_tuple
