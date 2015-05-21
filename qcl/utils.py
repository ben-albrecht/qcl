""" Assorted utility functions and classes """
from os import path, listdir


def is_type(typecheck, data):
    """
    Generic type checker
    typically used to check that a string can be cast to int or float
    """
    try:
        typecheck(data)
    except ValueError:
        return False
    else:
        return True


'''
def walk(topdir, ignore=None):
    """os.walk with an option to ignore directories"""
    for dirpath, dirnames, filenames in os.walk(topdir):
        dirnames[:] = [
            dirname for dirname in dirnames
            if os.path.join(dirpath, dirname) not in ignore]
        yield dirpath, dirnames, filenames
'''


def walk(top, topdown=True, onerror=None, followlinks=False, ignore=[]):
    """Modified implementation of os.walk with ignore option"""
    islink, join, isdir = path.islink, path.join, path.isdir

    # We may not have read permission for top, in which case we can't
    # get a list of the files the directory contains.  os.walk
    # always suppressed the exception then, rather than blow up for a
    # minor reason when (say) a thousand readable directories are still
    # left to visit.  That logic is copied here.
    try:
        names = listdir(top)
    except OSError as err:
        if onerror is not None:
            onerror(err)
        return

    dirs, nondirs = [], []
    for name in names:
        if name not in ignore:
            if isdir(join(top, name)):
                dirs.append(name)
            else:
                nondirs.append(name)

    if topdown:
        yield top, dirs, nondirs
    for name in dirs:
        new_path = join(top, name)
        if followlinks or not islink(new_path):
            yield from walk(new_path, topdown, onerror, followlinks)
    if not topdown:
        yield top, dirs, nondirs

