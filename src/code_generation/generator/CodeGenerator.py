from abc import ABC, abstractmethod

from src.code_generation.syntax.custom_type import NodeType
from src.code_generation.syntax.syntax_tree import Node


class CodeGenerator(ABC):
    def __init__(self, tree_adapter, root):
        self.tree_adapter = tree_adapter
        self.root = root
        # Mapping from NodeType to visit methods
        self.visit_map = {
            NodeType.MODULE: self.visit_module,
            NodeType.FUNCTION_DEF: self.visit_function_def,
            NodeType.PARAMETERS: self.visit_parameters,
            NodeType.PARAMETER: self.visit_parameter,
            NodeType.BODY: self.visit_body,
            NodeType.EXPRESSION_STATEMENT: self.visit_expression_statement,
            NodeType.IF_STATEMENT: self.visit_if_statement,
            NodeType.RETURN_STATEMENT: self.visit_return_statement,
            NodeType.IDENTIFIER_EXPRESSION: self.visit_identifier_expression,
            NodeType.LITERAL: self.visit_literal,
            NodeType.BINARY_OPERATION: self.visit_binary_operation,
            NodeType.UNARY_OPERATION: self.visit_unary_operation,
            NodeType.CALL_EXPRESSION: self.visit_call_expression,
            NodeType.DECORATOR: self.visit_decorator,
        }

    def visit(self, node: Node, indent: int = 0):
        node_type = self.tree_adapter.get_node_type(node)
        if node_type in self.visit_map:
            return self.visit_map[node_type](node, indent)
        else:
            raise NotImplementedError(f"Node type '{node_type.value}' not supported")

    def generate(self):
        return self.visit(self.root)

    @abstractmethod
    def visit_decorator(self, node: Node, indent: int):
        raise NotImplementedError

    @abstractmethod
    def visit_module(self, node: Node, indent: int):
        raise NotImplementedError

    @abstractmethod
    def visit_function_def(self, node: Node, indent: int):
        raise NotImplementedError

    @abstractmethod
    def visit_parameters(self, node: Node, indent: int):
        raise NotImplementedError

    @abstractmethod
    def visit_parameter(self, node: Node, indent: int):
        return self.tree_adapter.get_property(node, 'name')

    @abstractmethod
    def visit_body(self, node: Node, indent: int):
        raise NotImplementedError

    @abstractmethod
    def visit_expression_statement(self, node: Node, indent: int):
        raise NotImplementedError

    @abstractmethod
    def visit_if_statement(self, node: Node, indent: int):
        raise NotImplementedError

    @abstractmethod
    def visit_return_statement(self, node: Node, indent: int):
        raise NotImplementedError

    @abstractmethod
    def visit_identifier_expression(self, node: Node, indent: int):
        return self.tree_adapter.get_property(node, 'name')

    @abstractmethod
    def visit_literal(self, node: Node, indent: int):
        return self.tree_adapter.get_property(node, 'value')

    @abstractmethod
    def visit_binary_operation(self, node: Node, indent: int):
        raise NotImplementedError

    @abstractmethod
    def visit_unary_operation(self, node: Node, indent: int):
        raise NotImplementedError

    @abstractmethod
    def visit_call_expression(self, node: Node, indent: int):
        raise NotImplementedError