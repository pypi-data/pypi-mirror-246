import typing


class Error:
    """
    Use this class as a decorator like this:
    >>> @Error
    >>> class error: ...
    
    Also ignore the documentation that looks like:
    "Common base class for all exceptions"
    """
    def __new__(wrapper, error_class: object):
        class ErrorClass(error_class, Exception):
            """
            Feel free to use this error class anytime.
            
            And if you want to change the docstring / documentation
            of your class then just add a docstring to you class.
            """
            def __init__(self, /, message: typing.Any = None) -> None:
                super().__init__(message)


        return ErrorClass