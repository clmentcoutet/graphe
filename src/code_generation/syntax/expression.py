from abc import ABCMeta
from typing import Any, List, Optional

from src.code_generation.syntax.base_type import BaseType
from src.code_generation.syntax.custom_type import BinaryOperator, UnaryOperator
from src.code_generation.syntax.syntax_tree import Node


class Expression(Node, metaclass=ABCMeta):
    pass


class IdentifierExpression(Expression):
    def __init__(
            self,
            name: str,
            *,
            super_class: Optional['IdentifierDefinition'] = None):
        self.name = name
        self.super_class = super_class


    @property
    def children(self):
        return []


class BaseTypeExpression(IdentifierExpression):
    def __init__(
            self,
            name: str,
        ):
        super().__init__(name=name)

    def get_name(self, base_type: BaseType):
        return getattr(base_type, self.name)


class Literal(Expression):
    def __init__(self, value: Any):
        self.value = value

    @property
    def children(self):
        return []


class BinaryOperation(Expression):
    def __init__(self, left: Expression, operator: BinaryOperator, right: Expression):
        self.left = left
        self.operator = operator
        self.right = right

    @property
    def children(self):
        return [self.left, self.right]


class UnaryOperation(Expression):
    def __init__(self, operator: UnaryOperator, operand: Expression):
        self.operator = operator
        self.operand = operand

    @property
    def children(self):
        return [self.operand]


class CallExpression(Expression):
    def __init__(self, callee: IdentifierExpression, arguments: List[Expression]):
        self.callee = callee
        self.arguments = arguments  # List of expressions as arguments

    @property
    def children(self):
        return self.arguments
