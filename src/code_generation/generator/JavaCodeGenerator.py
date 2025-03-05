from src.code_generation.generator.CodeGenerator import CodeGenerator
from src.code_generation.syntax.base_type import JavaBaseType, BaseType
from src.code_generation.syntax.definition import ClassDefinition, AttributeDefinition, FunctionDefinition
from src.code_generation.syntax.expression import BaseTypeExpression, BinaryOperation, UnaryOperation, CallExpression, \
    Literal, IdentifierExpression
from src.code_generation.syntax.statement import ReturnStatement, IfStatement, ExpressionStatement
from src.code_generation.syntax.syntax_tree import Module, Parameters, Parameter, Body, Decorator
from src.code_generation.tree.adapter.TreePort import TreePort


class JavaCodeGenerator(CodeGenerator):
    INDENT = "    "

    def __init__(self, tree_adapter: TreePort, root: Module):
        super().__init__(tree_adapter, root)
        self.base_type = BaseType(JavaBaseType)

    def visit_base_type_expression(self, node: BaseTypeExpression, indent: int):
        return node.get_name(self.base_type)

    def visit_class_def(self, node: ClassDefinition, indent: int):
        modifiers = self.tree_adapter.get_property(node, 'modifiers') or ['public']
        name = self.visit(self.tree_adapter.get_property(node, 'name'), indent)
        extends = self.tree_adapter.get_property(node, 'extends')
        body = [self.visit(child, indent + 1) for child in self.tree_adapter.get_children(node)]
        indent_str = self.INDENT * indent
        modifier_str = " ".join(modifiers)
        res = f"{indent_str}{modifier_str} class {name}"
        if extends:
            extends_str = self.visit(extends, indent)
            res += f" extends {extends_str}"
        res += " {\n"
        res += "\n".join(body)
        res += f"\n{indent_str}}}"
        return res

    def visit_attribute_def(self, node: AttributeDefinition, indent: int):
        modifiers = self.tree_adapter.get_property(node, 'modifiers') or ['private']
        type_node = self.tree_adapter.get_property(node, 'type')
        name = self.visit(self.tree_adapter.get_property(node, 'name'), indent)
        initializer = self.tree_adapter.get_property(node, 'initializer')
        indent_str = self.INDENT * indent
        type_str = self.visit(type_node, indent) if type_node else "Object"
        res = f"{indent_str}{ ' '.join(modifiers) } {type_str} {name}"
        if initializer:
            init_code = self.visit(initializer, indent)
            res += f" = {init_code}"
        res += ";"
        return res

    def visit_function_def(self, node: FunctionDefinition, indent: int):
        modifiers = self.tree_adapter.get_property(node, 'modifiers') or ['public']
        return_type_node = self.tree_adapter.get_property(node, 'return_type')
        return_type = self.visit(return_type_node, indent) if return_type_node else "void"
        name = self.visit(self.tree_adapter.get_property(node, 'name'), indent)
        decorators = self.tree_adapter.get_property(node, 'decorators')
        children = self.tree_adapter.get_children(node)
        body = self.visit(children[0], indent + 1)
        params = self.visit(children[1], indent) if len(children) > 1 else ""
        decorators_code = []
        for decorator in decorators:
            decorators_code.append(self.visit(decorator, indent))
        annotation_str = "\n".join(decorators_code) + "\n" if decorators_code else ""
        modifier_str = " ".join(modifiers)
        indent_str = self.INDENT * indent
        return f"{annotation_str}{indent_str}{modifier_str} {return_type} {name}({params}) {{\n{body}\n{indent_str}}}"

    def visit_parameter(self, node: Parameter, indent: int):
        type_node = self.tree_adapter.get_property(node, '_type')
        name = self.visit(self.tree_adapter.get_property(node, 'name'), indent)
        type_str = self.visit(type_node, indent) if type_node else self.base_type.DEFAULT
        return f"{type_str} {name}"

    def visit_return_statement(self, node: ReturnStatement, indent: int):
        children = self.tree_adapter.get_children(node)
        code = self.visit(children[0], indent)
        indent_str = self.INDENT * indent
        return f"{indent_str}return {code};"

    def visit_if_statement(self, node: IfStatement, indent: int):
        indent_str = self.INDENT * indent
        children = self.tree_adapter.get_children(node)
        condition = self.visit(children[0], indent)
        then_branch = self.visit(children[1], indent + 1)
        code = f"{indent_str}if ({condition}) {{\n{then_branch}\n{indent_str}}}"
        if len(children) > 2:
            else_branch = self.visit(children[2], indent + 1)
            code += f" else {{\n{else_branch}\n{indent_str}}}"
        return code

    def visit_expression_statement(self, node: ExpressionStatement, indent: int):
        expr = self.visit(self.tree_adapter.get_children(node)[0], indent)
        indent_str = self.INDENT * indent
        return f"{indent_str}{expr};"

    def visit_call_expression(self, node: CallExpression, indent: int):
        call = self.visit(self.tree_adapter.get_property(node, 'callee'), indent)
        arguments = [self.visit(child, indent) for child in self.tree_adapter.get_children(node)]
        return f"{call}({', '.join(arguments)})"

    def visit_decorator(self, node: Decorator, indent: int):
        name = self.visit(self.tree_adapter.get_property(node, 'expression'), indent)
        parameters = self.tree_adapter.get_children(node)
        if parameters:
            params = self.visit(parameters[0], indent)
            return f"@{name}({params})"
        return f"@{name}"

    def visit_identifier_expression(self, node: IdentifierExpression, indent: int):
        res = self.tree_adapter.get_property(node, 'name')
        super_class = self.tree_adapter.get_property(node, 'super_class')
        if super_class:
            return f"{self.visit(super_class, indent)}.{res}"
        return res