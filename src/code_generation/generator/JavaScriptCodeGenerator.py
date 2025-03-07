from src.code_generation.generator.CodeGenerator import CodeGenerator
from src.code_generation.syntax.base_type import (
    BaseType,
    JavaScriptBaseType,
)  # Add JavaScriptBaseType similar to Python
from src.code_generation.syntax.definition import (
    FunctionDefinition,
    ClassDefinition,
    AttributeDefinition,
)
from src.code_generation.syntax.expression import (
    BaseTypeExpression,
    Literal,
    IdentifierExpression,
    BinaryOperation,
    UnaryOperation,
    CallExpression,
)
from src.code_generation.syntax.statement import (
    ExpressionStatement,
    ReturnStatement,
    IfStatement,
)
from src.code_generation.syntax.syntax_tree import (
    Node,
    Parameter,
    Module,
    Parameters,
    Decorator,
)
from src.code_generation.tree.adapter.TreePort import TreePort


class JavaScriptCodeGenerator(CodeGenerator):
    INDENT = "    "

    def __init__(self, tree_adapter: TreePort, root: Module):
        super().__init__(tree_adapter, root)
        self.base_type = BaseType(JavaScriptBaseType)  # Use JavaScriptBaseType

    def visit_base_type_expression(self, node: BaseTypeExpression, indent: int):
        return node.get_name(self.base_type)  # Return the name of the base type

    def visit_parameter(self, node: Parameter, indent: int):
        return super().visit_parameter(node, indent)

    def visit_identifier_expression(self, node: IdentifierExpression, indent: int):
        res = self.tree_adapter.get_property(node, "name")
        super_class = self.tree_adapter.get_property(node, "super_class")
        if super_class:
            return f"{self.visit(super_class, indent)}.{res}"
        return res

    def visit_literal(self, node: Literal, indent: int):
        return super().visit_literal(node, indent)

    def visit_body(self, node, indent):
        code = []
        for child in self.tree_adapter.get_children(node):
            code.append(self.visit(child, indent))
        indent_str = self.INDENT * indent
        return f"{indent_str}\n".join(code)

    def visit_expression_statement(self, node: ExpressionStatement, indent: int):
        raise NotImplementedError("visit_expression_statement not implemented")

    def visit_return_statement(self, node: ReturnStatement, indent: int):
        children = self.tree_adapter.get_children(node)
        code = self.visit(children[0], indent)  # Expression
        indent_str = self.INDENT * indent
        return f"{indent_str}return {code}"

    def visit_module(self, node: Module, indent: int):
        code = []
        for child in self.tree_adapter.get_children(node):
            code.append(self.visit(child, indent))
        return "\n\n".join(code)

    def visit_function_def(self, node: FunctionDefinition, indent: int):
        name = self.visit(self.tree_adapter.get_property(node, "name"), indent)
        decorators = self.tree_adapter.get_property(node, "decorators")
        children = self.tree_adapter.get_children(node)
        body = self.visit(children[0], indent + 1)  # Body
        params = self.visit(children[1], indent) if len(children) > 1 else ""
        decorators_code = []
        for decorator in decorators:
            decorators_code.append(self.visit(decorator, indent))
        res = f"{' '.join(decorators_code)}\n{self.INDENT * indent}function {name}({params})"
        return_type = self.tree_adapter.get_property(node, "return_type")
        if return_type:
            res += f" : {self.visit(return_type, indent)}"
        return f"{res} {{\n{body}\n{self.INDENT * indent}}}"

    def visit_parameters(self, node: Parameters, indent: int):
        params = [
            self.visit(child, indent) for child in self.tree_adapter.get_children(node)
        ]
        return ", ".join(params)

    def visit_binary_operation(self, node: BinaryOperation, indent: int):
        children = self.tree_adapter.get_children(node)
        left = self.visit(children[0], indent)
        right = self.visit(children[1], indent)
        op = self.tree_adapter.get_property(node, "operator").value
        return f"{left} {op} {right}"

    def visit_unary_operation(self, node: UnaryOperation, indent: int):
        children = self.tree_adapter.get_children(node)
        op = self.tree_adapter.get_property(node, "operator").value
        operand = self.visit(children[0], indent)
        return f"{op}{operand}"

    def visit_call_expression(self, node: CallExpression, indent: int):
        call = self.visit(self.tree_adapter.get_property(node, "callee"), indent)
        arguments = [
            self.visit(child, indent) for child in self.tree_adapter.get_children(node)
        ]
        return f"{call}({', '.join(arguments)})"

    def visit_if_statement(self, node: IfStatement, indent: int):
        indent_str = self.INDENT * indent
        children = self.tree_adapter.get_children(node)
        condition = self.visit(children[0], indent)
        then_branch = self.visit(children[1], indent + 1)
        code = f"{indent_str}if ({condition}) {{\n{then_branch}\n{indent_str}}}"
        if len(children) > 2:  # Else branch exists
            else_branch = self.visit(children[2], indent + 1)
            code += f"\n{indent_str}else {{\n{else_branch}\n{indent_str}}}"
        return code

    def visit_decorator(self, node: Decorator, indent: int):
        name = self.visit(self.tree_adapter.get_property(node, "expression"), indent)
        parameters = self.tree_adapter.get_children(node)
        res = f"{self.INDENT * indent}@{name}"
        if parameters:
            params = self.visit(parameters[0], indent)  # Parameters
            res += f"({', '.join(params)})"
        return res

    def visit_class_def(self, node: ClassDefinition, indent: int):
        name = self.visit(self.tree_adapter.get_property(node, "name"), indent)
        body = []
        for child in self.tree_adapter.get_children(node):
            body.append(self.visit(child, indent + 1))
        extended = self.tree_adapter.get_property(node, "extends")
        res = f"class {name}"
        if extended:
            extends = self.visit(extended, indent)  # Parameters
            res += f" extends {extends} {{"
        else:
            res += " {"
        res += "\n" + f"{self.INDENT * indent}\n".join(body)
        return res

    def visit_attribute_def(self, node: AttributeDefinition, indent: int):
        name = self.visit(self.tree_adapter.get_property(node, "name"), indent)
        _type = self.tree_adapter.get_property(node, "type")
        initializer = self.tree_adapter.get_property(node, "initializer")
        res = f"let {name}"
        if _type:
            res += f" : {self.visit(_type, indent)}"
        if initializer:
            res += f" = {self.visit(initializer, indent)}"
        return f"{self.INDENT * indent}{res}"
