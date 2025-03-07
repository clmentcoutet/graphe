from abc import ABCMeta
from typing import Any, List, Optional

from src.code_generation.syntax.base_type import BaseType
from src.code_generation.syntax.custom_type import BinaryOperator, UnaryOperator
from src.code_generation.syntax.syntax_tree import Node


class Expression(Node, metaclass=ABCMeta):
    pass


class Operation(Expression, metaclass=ABCMeta):
    pass


class IdentifierExpression(Expression):
    """
    Represents an identifier expression.

    Java attributes:
        name (str): The name of the identifier.
        super_class (Optional[IdentifierExpression]): The superclass reference, if applicable.
    """


class BaseTypeExpression(IdentifierExpression):
    """
    Represents a reference to a base type.

    Java attributes:
        name (BaseType): The name of the base type.
    """


class Literal(Expression):
    """
    Represents a literal value.

    Java attributes:
        value (Any): The value of the literal.
    """


class BinaryOperation(Operation):
    """
    Represents a binary operation.

    Java attributes:
        operator (BinaryOperator): The operator of the binary operation.
        left (Expression): The left operand of the binary operation.
        right (Expression): The right operand of the binary operation.
    """


class UnaryOperation(Operation):
    """
    Represents a unary operation.

    Java attributes:
        operator (UnaryOperator): The operator of the unary operation.
        operand (Expression): The operand of the unary operation.
    """


class CallExpression(Expression):
    """
    Represents a method call expression.

    Java attributes:
        callee (IdentifierExpression): The identifier expression of the callee.
        arguments (Optional[List[Expression]]): The list of arguments for the method call.
    """
