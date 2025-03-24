"""
Data structures and algorithms for Undirected Graphs
"""

from collections import defaultdict


GraphEL = list[tuple[int, int]]
GraphAL = dict[int, set[int]]


def el2al(graph: GraphEL) -> GraphAL:
    al = defaultdict(lambda: set())
    for left, right in graph:
        al[left] = al[left] | {right}
        al[right] = al[right] | {left}
    return al


def al2el(graph: GraphAL) -> GraphEL:
    output = []
    for vertex, neighbors in graph.items():
        for neighbor in neighbors:
            output.append((vertex, neighbor))
            output.append((neighbor, vertex))
    return list(set(output))


def get_vertices(graph: GraphEL) -> set[int]:
    return {vertex for edge in graph for vertex in edge}


def get_neighbors(graph: GraphEL, vertex: int) -> set[int]:
    return {edge[1] for edge in graph if edge[0] == vertex} | {
        edge[0] for edge in graph if edge[1] == vertex
    }


def depth_first_search(graph: GraphEL, start: int) -> list[int]:
    visited = set()
    stack = [start]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            for neighbor in get_neighbors(graph, vertex):
                stack.append(neighbor)
    return visited


def is_connected(graph: GraphEL) -> bool:
    starting_vertex = graph[0][0] if graph else None
    if starting_vertex is None:
        return False
    visits = depth_first_search(graph, 0)
    return all([node in visits for node in get_vertices(graph)])


def has_loop_recursive(graph: GraphEL) -> bool:
    visited = set()

    def dfs_has_loop(node, parent):
        visited.add(node)
        for neighbor in get_neighbors(graph, node):
            if neighbor not in visited:
                _has_loop = dfs_has_loop(neighbor, node)
                if _has_loop:
                    return True
            elif neighbor != parent:
                return True
        return False

    if not graph:
        return False
    return dfs_has_loop(graph[0][0], None)


def has_loop(graph: GraphEL) -> bool:
    if not graph:
        return False
    visited = set()
    stack = [(graph[0][0], None)]
    while stack:
        node, parent = stack.pop()
        visited.add(node)
        for neighbor in get_neighbors(graph, node):
            if neighbor not in visited:
                stack.append((neighbor, node))
            elif neighbor != parent:
                return True
    return False


def topo_sort(graph: GraphEL) -> list[int]:
    def dfs_topo_sort(node, visited, stack):
        stack = []
        visited.add(node)
        for neighbor in get_neighbors(graph, node):
            if neighbor not in visited:
                stack.extend(dfs_topo_sort(neighbor, visited, stack))
        stack.append(node)
        return stack

    nodes = get_vertices(graph)
    order = []
    visited = set()
    while len(visited) < len(nodes):
        for node in nodes:
            if node not in visited:
                order.extend(dfs_topo_sort(node, visited, []))

    if not graph:
        return []
    return order
