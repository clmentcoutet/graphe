def classify_edges(graph, start):
    """
    Perform a DFS from the start node to classify each edge in the graph.
    An edge (u, v) is marked as a 'back' edge (cycle edge) if v is already
    in the recursion stack when it is encountered.

    Returns a dictionary mapping (u, v) to one of:
      - 'tree' for tree edges,
      - 'back' for back (cycle) edges,
      - 'forward/cross' for other edges.
    """
    discovered = {}
    finished = {}
    edge_types = {}
    time = 0
    recursion_stack = set()

    def dfs(u):
        nonlocal time
        time += 1
        discovered[u] = time
        recursion_stack.add(u)
        for v in graph.get(u, []):
            if v not in discovered:
                edge_types[(u, v)] = 'tree'
                dfs(v)
            elif v in recursion_stack:
                edge_types[(u, v)] = 'back'
            else:
                edge_types[(u, v)] = 'forward/cross'
        recursion_stack.remove(u)
        time += 1
        finished[u] = time

    dfs(start)
    return edge_types


def build_state_graph(graph, start):
    """
    Convert the original (possibly cyclic) graph into an acyclic state graph.

    Each node 'v' in the original graph appears in two states:
       (v, False): reached without having traversed any cycle edge,
       (v, True): reached after having traversed a cycle edge.

    For every original edge (u, v):
       - If (u, v) is a back edge (cycle edge), add a transition only from
         (u, False) to (v, True).
       - Otherwise, add transitions from (u, False) to (v, False) and from
         (u, True) to (v, True).
    """
    edge_types = classify_edges(graph, start)

    # Collect all nodes in the graph.
    nodes = set(graph.keys())
    for u in graph:
        for v in graph[u]:
            nodes.add(v)

    # Initialize the state graph with both states for every node.
    state_graph = {}
    for node in nodes:
        state_graph[(node, False)] = []
        state_graph[(node, True)] = []

    for u in graph:
        for v in graph[u]:
            if edge_types.get((u, v), 'tree') == 'back':
                # Cycle edge: allowed only when the cycle is not yet used.
                state_graph[(u, False)].append((v, True))
            else:
                # Normal edge: available in both states.
                state_graph[(u, False)].append((v, False))
                state_graph[(u, True)].append((v, True))
    return state_graph


def filter_reachable_states(state_graph, start_state):
    """
    Filter the state graph to include only states reachable from the start_state.
    """
    reachable = set()
    stack = [start_state]
    while stack:
        current = stack.pop()
        if current not in reachable:
            reachable.add(current)
            for neighbor in state_graph.get(current, []):
                if neighbor not in reachable:
                    stack.append(neighbor)
    return {state: [nbr for nbr in neighbors if nbr in reachable]
            for state, neighbors in state_graph.items() if state in reachable}


def get_sinks(state_graph):
    """
    Return all states in the state graph that have no outgoing transitions.
    """
    return {state for state, neighbors in state_graph.items() if not neighbors}


def list_all_paths_dag(state_graph, start_state, sinks):
    """
    Return all paths (as lists of state nodes) in the DAG from start_state to any sink.
    """
    all_paths = []

    def dfs(current, path):
        if current in sinks:
            all_paths.append(path.copy())
        for neighbor in state_graph.get(current, []):
            dfs(neighbor, path + [neighbor])

    dfs(start_state, [start_state])
    return all_paths


def convert_state_path_to_original(state_path):
    """
    Given a state path (a list of tuples (node, used)), return the corresponding
    path in the original graph by dropping the state information.
    """
    return [node for (node, used) in state_path]


def get_all_paths_from_cycled_graph(graph, start):
    full_state_graph = build_state_graph(graph, start)
    filtered_state_graph = filter_reachable_states(full_state_graph, (start, False))

    # Identify sink states in the filtered state graph.
    sinks = get_sinks(filtered_state_graph)

    state_paths = list_all_paths_dag(filtered_state_graph, (start, False), sinks)
    original_paths = [convert_state_path_to_original(path) for path in state_paths]

    return original_paths

# --- Example usage ---
if __name__ == "__main__":
    # Define the original cyclic graph.
    # Graph:
    #   A -> B -> C -> D
    #         ^       │
    #         └-------┘   (cycle edge C -> B)
    graph = {
        'A': ['B'],
        'B': ['C', 'A'],
        'C': ['D', 'B']  # C -> B is a back (cycle) edge.
    }
    start = 'A'
    graph = {
        'A': ['B'],
        'B': ['A', 'C'],
        'C': ['D', 'A'],
        'D': ['C', 'B', 'E', 'A']
    }

    original_paths = get_all_paths_from_cycled_graph(graph, start)

    print("\nCorresponding paths in the original graph:")
    for path in original_paths:
        print(path)
