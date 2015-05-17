""" Assorted utility functions and classes """

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


