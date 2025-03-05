from abc import ABCMeta
from typing import Optional, List

from src.code_generation.syntax.custom_type import Modifiers
from src.code_generation.syntax.syntax_tree import Node, Parameters, Body, Decorator
from src.code_generation.syntax.expression import Expression


class Definition(Node, metaclass=ABCMeta):
    pass


class FunctionDefinition(Definition):
    """
    Represents a function definition

    Possible kwargs:
        return_type: The return type
        modifier: The modifier (e.g., 'public', 'private')
    """
    def __init__(
            self,
            name: 'IdentifierExpression',
            body: Body,
            parameters: Optional[Parameters] = None,
            decorators: Optional[List[Decorator]] = None,
            *,
            return_type: Optional['IdentifierExpression'] = None,
            modifier: Optional[Modifiers] = None,
    ):
        self.name = name
        self.body = body
        self.decorators = decorators or []
        self.parameters = parameters or []
        self.return_type = return_type
        self.modifier = modifier


    @property
    def children(self):
        if self.parameters:
            return [self.body, self.parameters]
        return [self.body]


class AttributeDefinition(Definition):
    """
    Represents a class attribute
    Possible kwargs:
        type: The type
        initializer: The initial value
        modifier: The modifier (e.g., 'public', 'private')
    """
    def __init__(
            self,
            name: 'IdentifierExpression',
            *,
            type: Optional['IdentifierExpression'] = None,
            initializer: Optional[Expression] = None,
            modifier: Optional[Modifiers] = None,
    ):
        self.name = name
        self.type = type
        self.initializer = initializer
        self.modifier = modifier

    @property
    def children(self):
        return []


class ClassDefinition(Definition):
    """
    Represents a class definition

    Possible kwargs:
        extends: The class that this class extends
        implements: The interfaces this class implements
        modifiers: The modifiers (e.g., 'public', 'private')
    """
    def __init__(
            self,
            name: 'IdentifierExpression',
            attributes: List[AttributeDefinition],
            methods: List[FunctionDefinition],
            *,
            extends: Optional['IdentifierExpression'] = None,
            implements: Optional[List['IdentifierExpression']] = None,
            modifiers: Optional[Modifiers] = None,
    ):
        self.name = name
        self.methods = methods
        self.attributes = attributes
        self.extends = extends
        self.implements = implements
        self.modifiers = modifiers

    @property
    def children(self):
        return self.attributes + self.methods
