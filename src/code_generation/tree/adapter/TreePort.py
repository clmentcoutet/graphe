from abc import ABC, abstractmethod
from typing import List, Any

from src.code_generation.syntax.custom_type import NodeType
from src.code_generation.syntax.syntax_tree import Node


class TreePort(ABC):
    @abstractmethod
    def get_node_type(self, node: Node) -> NodeType:
        pass

    @abstractmethod
    def get_children(self, node: Node) -> List[Node]:
        pass

    @abstractmethod
    def get_property(self, node: Node, prop: Any, *, default=None, is_require=True) -> Any:
        pass
