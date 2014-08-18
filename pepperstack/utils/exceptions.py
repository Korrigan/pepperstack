"""
Module containing useful exceptions for pepperstack

"""

class PepperstackException(Exception):
    """
    Base class for all pepperstack exception to make
    catch-all easier

    """
    pass


class DoesNotExistsException(PepperstackException):
    """
    An exception class raised when a model is not found

    """
    pass


class DuplicateException(PepperstackException):
    """
    An exception class raised when trying to create duplicate
    entries in database

    """
    pass

class CommandException(PepperstackException):
    """
    An exception class used to handle command errors

    """
    pass
