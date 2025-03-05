from typing import List, Any

from src.code_generation.syntax.custom_type import NodeType
from src.code_generation.syntax.syntax_tree import Node
from src.code_generation.tree.TreePort import TreePort


class ClassTreeAdapter(TreePort):
    def get_node_type(self, node: Node) -> NodeType:
        print(node)
        return node.get_type()

    def get_children(self, node: Node) -> List[Node]:
        return node.children

    def get_property(self, node: Node, prop: Any):
        return getattr(node, prop, None)