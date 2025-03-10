from abc import ABC, abstractmethod
from typing import List, Optional, Any

from src.code_generation.syntax.custom_type import NodeType


class Node(ABC):
    TYPE_MAPPING = {
        "Module": NodeType.MODULE,
        "FunctionDefinition": NodeType.FUNCTION_DEF,
        "Parameters": NodeType.PARAMETERS,
        "Parameter": NodeType.PARAMETER,
        "Body": NodeType.BODY,
        "Statement": NodeType.STATEMENT,
        "ExpressionStatement": NodeType.EXPRESSION_STATEMENT,
        "IfStatement": NodeType.IF_STATEMENT,
        "ReturnStatement": NodeType.RETURN_STATEMENT,
        "Expression": NodeType.EXPRESSION,
        "IdentifierExpression": NodeType.IDENTIFIER_EXPRESSION,
        "BaseTypeExpression": NodeType.BASE_TYPE_EXPRESSION,
        "Literal": NodeType.LITERAL,
        "BinaryOperation": NodeType.BINARY_OPERATION,
        "UnaryOperation": NodeType.UNARY_OPERATION,
        "CallExpression": NodeType.CALL_EXPRESSION,
        "Decorator": NodeType.DECORATOR,
        "ClassDefinition": NodeType.CLASS_DEF,
        "AttributeDefinition": NodeType.ATTRIBUTE_DEF,
    }

    def __init__(
        self,
        **kwargs,
    ):
        self.kwargs = kwargs

    def get_type(self):
        return self.TYPE_MAPPING[self.__class__.__name__]


class Module(Node):
    """
    Represents a module in the abstract tree

    Java attributes:
        - classes (Optional[List[ClassDefinition]]): The classes defined in the module.
    """

    def __init__(
        self,
        **kwargs,
    ):
        self.kwargs = kwargs


class Parameter(Node):
    """
    Represents a function parameter.

    Java attributes:
        - name (IdentifierExpression): The name of the parameter.
        - type (IdentifierExpression): The type of the parameter.
    """


class Parameters(Node):
    def __init__(self, parameters: List[Parameter]):
        self.parameters = parameters

    @property
    def children(self):
        return self.parameters


class Body(Node):
    """
    Represents the body of a function or method.

    Java attributes:
        - statements (List[Statement]): The statements in the body.
    """


class Decorator(Node):
    """
    Represents a decorator in the abstract tree

    Java attributes:
        - name (IdentifierExpression): The name of the decorator
        - arguments (Optional[Expression]): The arguments of the decorator
    """
