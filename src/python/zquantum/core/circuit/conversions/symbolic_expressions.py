"""Utilities for converting symbolic expressions between different dialects."""
from functools import singledispatch
from numbers import Number
from typing import NamedTuple, Any, Iterable, Union, Dict, Callable

import sympy


class Symbol(NamedTuple):
    """Abstract symbol."""

    name: str


class FunctionCall(NamedTuple):
    """Represents abstract function call.     """

    name: str
    args: Iterable["Expression"]


Expression = Union[Symbol, FunctionCall, Number]


@singledispatch
def expression_tree_from_sympy(expression):
    raise NotImplementedError(
        f"Expression {expression} of type {type(expression)} is currentlyl not supported"
    )
