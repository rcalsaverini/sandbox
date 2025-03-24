"""
Data structures and algorithms for Directed Graphs
"""

GraphEL = list[tuple[int, int]]
GraphAL = dict[int, set[int]]


def el2al(graph: GraphEL) -> GraphAL:
    al = {}
    for edge in graph:
        al[edge[0]] = al.get(edge[0], set()) | {edge[1]}
    return al


def al2el(graph: GraphAL) -> GraphEL:
    return [
        (vertex, neighbor)
        for vertex, neighbors in graph.items()
        for neighbor in neighbors
    ]


def get_neighbors(graph: GraphEL, vertex: int) -> set[int]:
    return {edge[1] for edge in graph if edge[0] == vertex}
