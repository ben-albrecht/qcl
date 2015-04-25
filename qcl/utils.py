""" Assorted utility functions and classes """

def is_type(typecheck, data):
    """ Generic type checker """
    try:
        typecheck(data)
    except ValueError:
        return False
    else:
        return True
