from abc import ABC, abstractmethod

from src.code_generation.syntax.custom_type import NodeType
from src.code_generation.syntax.definition import ClassDefinition, AttributeDefinition, FunctionDefinition
from src.code_generation.syntax.expression import BaseTypeExpression, IdentifierExpression, Literal, BinaryOperation, \
    UnaryOperation, CallExpression
from src.code_generation.syntax.statement import ExpressionStatement, IfStatement, ReturnStatement
from src.code_generation.syntax.syntax_tree import Node, Decorator, Module, Parameters, Parameter, Body
from src.code_generation.tree.adapter.TreePort import TreePort


class CodeGenerator(ABC):
    INDENT = "    "

    def __init__(self, tree_adapter: TreePort, root: Module):
        self.tree_adapter = tree_adapter
        self.root = root
        self.base_type = None
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
            NodeType.BASE_TYPE_EXPRESSION: self.visit_base_type_expression,
            NodeType.LITERAL: self.visit_literal,
            NodeType.BINARY_OPERATION: self.visit_binary_operation,
            NodeType.UNARY_OPERATION: self.visit_unary_operation,
            NodeType.CALL_EXPRESSION: self.visit_call_expression,
            NodeType.DECORATOR: self.visit_decorator,
            NodeType.CLASS_DEF: self.visit_class_def,
            NodeType.ATTRIBUTE_DEF: self.visit_attribute_def,
        }

    def visit(self, node: Node, indent):
        node_type = self.tree_adapter.get_node_type(node)
        if node_type in self.visit_map:
            return self.visit_map[node_type](node, indent)
        else:
            raise NotImplementedError(f"Node type '{node_type.value}' not supported")

    def generate(self):
        return self.visit(self.root, 0)

    def visit_module(self, node: Module, indent: int):
        code = [self.visit(child, indent) for child in self.tree_adapter.get_children(node)]
        return "\n\n".join(code)

    @abstractmethod
    def visit_base_type_expression(self, node: BaseTypeExpression, indent: int):
        node.get_name(self.base_type)

    @abstractmethod
    def visit_decorator(self, node: Decorator, indent: int):
        raise NotImplementedError

    @abstractmethod
    def visit_class_def(self, node: ClassDefinition, indent: int):
        raise NotImplementedError

    @abstractmethod
    def visit_attribute_def(self, node: AttributeDefinition, indent: int):
        raise NotImplementedError

    @abstractmethod
    def visit_function_def(self, node: FunctionDefinition, indent: int):
        raise NotImplementedError

    def visit_parameters(self, node: Parameters, indent: int):
        params = [self.visit(child, indent) for child in self.tree_adapter.get_children(node)]
        return ", ".join(params)

    def visit_parameter(self, node: Parameter, indent: int):
        return self.visit(self.tree_adapter.get_property(node, 'name'), indent)

    def visit_body(self, node: Body, indent: int):
        code = [self.visit(child, indent) for child in self.tree_adapter.get_children(node)]
        return f"{self.INDENT * indent}\n".join(code)

    @abstractmethod
    def visit_expression_statement(self, node: ExpressionStatement, indent: int):
        raise NotImplementedError

    @abstractmethod
    def visit_if_statement(self, node: IfStatement, indent: int):
        raise NotImplementedError

    @abstractmethod
    def visit_return_statement(self, node: ReturnStatement, indent: int):
        raise NotImplementedError

    @abstractmethod
    def visit_identifier_expression(self, node: IdentifierExpression, indent: int):
        raise NotImplementedError

    def visit_literal(self, node: Literal, indent: int):
        return self.tree_adapter.get_property(node, 'value')

    def visit_binary_operation(self, node: BinaryOperation, indent: int):
        children = self.tree_adapter.get_children(node)
        left = self.visit(children[0], indent)
        right = self.visit(children[1], indent)
        op = self.tree_adapter.get_property(node, 'operator').value
        return f"{left} {op} {right}"

    def visit_unary_operation(self, node: UnaryOperation, indent: int):
        children = self.tree_adapter.get_children(node)
        op = self.tree_adapter.get_property(node, 'operator').value
        operand = self.visit(children[0], indent)
        return f"{op}{operand}"

    @abstractmethod
    def visit_call_expression(self, node: CallExpression, indent: int):
        raise NotImplementedError