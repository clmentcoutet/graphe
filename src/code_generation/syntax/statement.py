from abc import ABCMeta
from typing import Optional

from src.code_generation.syntax.syntax_tree import Node, Body
from src.code_generation.syntax.expression import Expression


class Statement(Node, metaclass=ABCMeta):
    pass


class ExpressionStatement(Statement):
    def __init__(self, expression: Expression):
        self.expression = expression

    @property
    def children(self):
        return []


class IfStatement(Statement):
    def __init__(self, condition: Expression, then_branch: Body, else_branch: Optional[Body] = None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    @property
    def children(self):
        children = [self.condition, self.then_branch]
        if self.else_branch is not None:
            children.append(self.else_branch)
        return children


class ReturnStatement(Statement):
    def __init__(self, expression: Expression):
        self.expression = expression

    @property
    def children(self):
        return [self.expression]
