from abc import ABCMeta
from typing import Optional, List

from src.code_generation.syntax.custom_type import Modifier
from src.code_generation.syntax.syntax_tree import Node, Parameters, Body, Decorator
from src.code_generation.syntax.expression import Expression


class Definition(Node, metaclass=ABCMeta):
    pass


class FunctionDefinition(Definition):
    """
    Represents a function definition

    Java attributes:
        - name (IdentifierExpression): The function name
        - return_type (IdentifierExpression): The function return type
        - modifier (Modifier): The function modifier (e.g., 'public', 'private')
        - body (Optional[Body]): The function body
        - parameters (Optional[List[Parameter]]): The function parameters
        - decorators (Optional[List[Decorator]]): The function decorators
    """


class AttributeDefinition(Definition):
    """
    Represents a class attribute

    Java attributes:
        - name (IdentifierExpression): The attribute name
        - type (IdentifierExpression): The attribute type
        - modifier (Modifier): The attribute modifier (e.g., 'public', 'private')
        - initializer (Optional[Expression]): The attribute initializer
    """


class ClassDefinition(Definition):
    """
    Represents a class definition

    Java attributes:
        - name (IdentifierExpression): The class name
        - modifiers (Modifier): The class modifier (e.g., 'public', 'private')
        - attributes (Optional[AttributeDefinition]): attribute of the class
        - methods (Optional[List[FunctionDefinition]]): methods of the class
        - implements (Optional[List[IdentifierExpression]]): The class implements
        - extend (Optional[IdentifierExpression]): The class extends
    """

    def __init__(
        self,
        name: "IdentifierExpression",
        attributes: List[AttributeDefinition],
        methods: List[FunctionDefinition],
        *,
        extend: Optional["IdentifierExpression"] = None,
        implements: Optional[List["IdentifierExpression"]] = None,
        modifiers: Optional[Modifier] = None,
    ):
        self.name = name
        self.methods = methods
        self.attributes = attributes
        self.extend = extend
        self.implements = implements
        self.modifiers = modifiers

    @property
    def children(self):
        return self.attributes + self.methods
