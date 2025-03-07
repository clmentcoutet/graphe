from abc import ABCMeta
from typing import Optional

from src.code_generation.syntax.syntax_tree import Node, Body
from src.code_generation.syntax.expression import Expression


class Statement(Node, metaclass=ABCMeta):
    pass


class ExpressionStatement(Statement):
    """
    Represents an expression statement in the code.

    Java attributes:
        - expression (Expression): The expression to be evaluated.
    """


class IfStatement(Statement):
    """
    Represents an if statement in the code.

    Java attributes:
        - condition (Expression): The condition to be evaluated.
        - then (Body): The body of the if statement when the condition is true.
        - _else (Optional[Body]): The body of the if statement when the condition is false.
    """


class ReturnStatement(Statement):
    """"
    Represents a return statement in the code.

    Java attributes:
        - expression (Expression): The expression to be returned.
    """
