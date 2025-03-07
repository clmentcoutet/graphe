from collections import deque


def find_paths(graph, start, end, cycles):
    paths = []
    queue = deque([(start, [start], set())])  # (current node, path, used cycles)

    cycle_sets = [set(cycle) for cycle in cycles]  # Convert cycles to sets for quick lookup

    while queue:
        node, path, used_cycles = queue.popleft()

        if node == end:
            paths.append(path)
            continue

        for neighbor in graph.get(node, []):
            if neighbor in path:
                continue  # Avoid simple cycles (self-loops)

            new_used_cycles = set()
            for cycle_index, cycle in enumerate(cycle_sets):
                if neighbor in cycle and any(n in cycle for n in path):
                    new_used_cycles.add(cycle_index)

            if not (used_cycles & new_used_cycles):  # Ensure we don't revisit cycles
                queue.append((neighbor, path + [neighbor], used_cycles | new_used_cycles))

    return paths

if __name__ == '__main__':
    # Example graph
    graph = {
        '0': ['1', '7'],
        '1': ['2'],
        '2': ['3'],
        '3': ['4', '5'],
        '4': [],
        '5': ['6', '7'],
        '6': ['2'],
        '7': ['1', '6']
    }
    start = '0'
    end = '4'
    cycles = [['2', '3', '5', '6'], ['2', '3', '5', '7', '1'], ['2', '3', '5', '7', '6']]

    # Find paths
    paths = find_paths(graph, start, end, cycles)

    # Display results
    for path in paths:
        print(" -> ".join(path))
