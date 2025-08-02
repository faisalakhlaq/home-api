import random
import string
from typing import Any, Callable, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


def random_string_generator(
    size: int = 8, chars: str = string.ascii_lowercase + string.digits
) -> str:
    return "".join(random.choice(chars) for _ in range(size))


def set_docstring(doc: str, **format_kwargs: Any) -> Callable[[F], F]:
    """
    Decorator factory that assigns a docstring to a function or method.

    This is particularly useful when you want to:
    1. Share the same docstring between OpenAPI specs and method docstrings
    2. Dynamically set docstrings
    3. Keep docstring definitions DRY by reusing them

    Args:
        doc: The docstring to be assigned to the decorated function

    Returns:
        A decorator that will assign the docstring to its target function

    Example:
        >>> DOC = "This does something important"
        >>>
        >>> @set_docstring(DOC)
        >>> def my_function():
        >>>     pass
        >>>
        >>> print(my_function.__doc__)
        'This does something important'

    Extended functionality:
        Can format the docstring with keyword arguments:

        >>> DOC = "Process {entity}s"
        >>>
        >>> @set_docstring(DOC, entity="user")
        >>> def process_users():
        >>>     pass
        >>>
        >>> print(process_users.__doc__)
        'Process users'

    Notes:
        - Works with both functions and methods
        - The docstring is assigned at decoration time (when Python loads the
            module)
        - For class methods, consider placing this decorator after @classmethod
            or @staticmethod
    """
    if format_kwargs:
        doc = doc.format(**format_kwargs)

    def decorator(func: F) -> F:
        func.__doc__ = doc
        return func

    return decorator
