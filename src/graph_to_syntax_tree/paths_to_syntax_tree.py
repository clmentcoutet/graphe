from typing import List, Dict

from src.graph_to_syntax_tree.generate_syntax_tree_skeleton import generate_syntax_tree_skeleton_from_test_name
from src.graph_to_syntax_tree.merge_syntax_tree import merge_syntax_tree
from src.graph_to_syntax_tree.path_to_syntax import get_test_name_path_using_node_label


def paths_to_syntax_tree(paths: List[List[Dict]]):
    sub_syntax_tree = []
    for path in paths:
        test_name = get_test_name_path_using_node_label(path)
        sub_syntax_tree.append(generate_syntax_tree_skeleton_from_test_name(test_name))

    class_name = "class_test"
    return merge_syntax_tree(class_name, sub_syntax_tree)