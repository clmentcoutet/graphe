from typing import Dict, List


def _normalize_label(label: str) -> str:
    return label.strip().lower().replace(" ", "_")


def get_test_name_path_using_node_label(path: List[Dict]) -> str:
    result = "test_"
    for i, node in enumerate(path):
        label = _normalize_label(node.get('label', "") if node.get('label', "") else "")
        _type = node.get('type', "") if node.get('type', "") else "external_call"
        if i == 0:
            result += f"{label}__"
        elif i == len(path) - 1:
            result += f"_{label}"
        elif _type == "external_call":
            result += f"{label}_"
    return result