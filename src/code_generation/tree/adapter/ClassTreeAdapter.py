from typing import List, Any

from src.code_generation.syntax.custom_type import NodeType
from src.code_generation.syntax.syntax_tree import Node
from src.code_generation.tree.adapter.TreePort import TreePort


class ClassTreeAdapter(TreePort):
    def get_node_type(self, node: Node) -> NodeType:
        return node.get_type()

    def get_children(self, node: Node) -> List[Node]:
        return node.children

    def get_property(
        self, node: Node, prop: Any, *, default=None, is_require=True
    ) -> Any:
        kwargs = getattr(node, "kwargs", {})
        _prop = kwargs.get(prop, default)
        if is_require and _prop is None:
            raise AttributeError(
                f"Attribute '{prop}' is not defined but required for class '{node.__class__.__name__}'"
            )
        return _prop
