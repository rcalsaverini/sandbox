from pytest import fixture

from python.graphs.src.undirected import (
    get_neighbors,
    get_vertices,
    is_connected,
    has_loop,
    has_loop_recursive,
    topo_sort,
    GraphEL,
    GraphAL,
    el2al,
    al2el,
)


@fixture
def empty_el() -> GraphEL:
    return []


@fixture
def empty_al() -> GraphAL:
    return {}


@fixture
def noloop_el() -> GraphEL:
    return [(0, 1), (0, 2), (2, 3)]


@fixture
def noloop_al() -> GraphAL:
    return {0: {1, 2}, 1: {0}, 2: {0, 3}, 3: {2}}


@fixture
def simple_el() -> GraphEL:
    return [(0, 1), (0, 2), (2, 1), (2, 3)]


@fixture
def simple_al() -> GraphAL:
    return {0: {1, 2}, 1: {0, 2}, 2: {0, 1, 3}, 3: {2}}


@fixture
def non_connected_el() -> GraphEL:
    return [(0, 1), (1, 2), (2, 3), (4, 5), (4, 6)]


@fixture
def non_connected_al() -> GraphAL:
    return {0: {1}, 1: {0, 2}, 2: {1, 3}, 3: {2}, 4: {5, 6}, 5: {4}, 6: {4}}


@fixture
def fully_connected_el() -> GraphEL:
    return [
        (0, 1),
        (0, 2),
        (0, 3),
        (0, 4),
        (1, 2),
        (1, 3),
        (1, 4),
        (2, 3),
        (2, 4),
        (3, 4),
    ]


@fixture
def fully_connected_al() -> GraphAL:
    return {
        0: {1, 2, 3, 4},
        1: {0, 2, 3, 4},
        2: {0, 1, 3, 4},
        3: {0, 1, 2, 4},
        4: {0, 1, 2, 3},
    }


@fixture
def all_graphs_el(empty_el, noloop_el, simple_el, fully_connected_el, non_connected_el):
    return [empty_el, noloop_el, simple_el, fully_connected_el, non_connected_el]


@fixture
def all_graphs_al(empty_al, noloop_al, simple_al, fully_connected_al, non_connected_al):
    return [empty_al, noloop_al, simple_al, fully_connected_al, non_connected_al]


def test_el2al(all_graphs_el, all_graphs_al):
    for graph_el, graph_al in zip(all_graphs_el, all_graphs_al):
        assert set(el2al(graph_el)) == set(graph_al), f"{graph_el} failed"


def test_al2el(all_graphs_el, all_graphs_al):
    for graph_el, graph_al in zip(all_graphs_el, all_graphs_al):
        edges = {edge for edge in graph_el}
        for edge in al2el(graph_al):
            assert (edge in edges) or (edge[1], edge[0]) in edges, (
                f"{edge} not in {edges}"
            )


def test_get_vertices(
    empty_el, noloop_el, simple_el, fully_connected_el, non_connected_el
):
    assert get_vertices(empty_el) == set()
    assert get_vertices(simple_el) == {0, 1, 2, 3}
    assert get_vertices(noloop_el) == {0, 1, 2, 3}
    assert get_vertices(fully_connected_el) == {0, 1, 2, 3, 4}
    assert get_vertices(non_connected_el) == {0, 1, 2, 3, 4, 5, 6}


def test_get_neighbors(
    empty_el, noloop_el, simple_el, fully_connected_el, non_connected_el
):
    assert get_neighbors(empty_el, 0) == set()
    assert get_neighbors(noloop_el, 0) == {1, 2}
    assert get_neighbors(noloop_el, 1) == {0}
    assert get_neighbors(noloop_el, 2) == {0, 3}
    assert get_neighbors(noloop_el, 3) == {2}
    assert get_neighbors(simple_el, 0) == {1, 2}
    assert get_neighbors(simple_el, 1) == {0, 2}
    assert get_neighbors(simple_el, 2) == {0, 1, 3}
    assert get_neighbors(simple_el, 3) == {2}
    assert get_neighbors(fully_connected_el, 0) == {1, 2, 3, 4}
    assert get_neighbors(fully_connected_el, 1) == {0, 2, 3, 4}
    assert get_neighbors(fully_connected_el, 2) == {0, 1, 3, 4}
    assert get_neighbors(fully_connected_el, 3) == {0, 1, 2, 4}
    assert get_neighbors(fully_connected_el, 4) == {0, 1, 2, 3}
    assert get_neighbors(non_connected_el, 0) == {1}
    assert get_neighbors(non_connected_el, 1) == {0, 2}
    assert get_neighbors(non_connected_el, 2) == {1, 3}
    assert get_neighbors(non_connected_el, 3) == {2}
    assert get_neighbors(non_connected_el, 4) == {5, 6}
    assert get_neighbors(non_connected_el, 5) == {4}
    assert get_neighbors(non_connected_el, 6) == {4}


def test_is_connected(
    empty_el, noloop_el, simple_el, fully_connected_el, non_connected_el
):
    assert not is_connected(empty_el)
    assert is_connected(noloop_el)
    assert is_connected(simple_el)
    assert is_connected(fully_connected_el)
    assert not is_connected(non_connected_el)


def test_has_loop(empty_el, noloop_el, simple_el, fully_connected_el, non_connected_el):
    assert not has_loop(empty_el)
    assert not has_loop(noloop_el)
    assert has_loop(simple_el)
    assert has_loop(fully_connected_el)
    assert not has_loop(non_connected_el)


def test_has_loop_recursive(
    empty_el, noloop_el, simple_el, fully_connected_el, non_connected_el
):
    assert not has_loop_recursive(empty_el)
    assert not has_loop_recursive(noloop_el)
    assert has_loop_recursive(simple_el)
    assert has_loop_recursive(fully_connected_el)
    assert not has_loop_recursive(non_connected_el)


def test_topo_sort(
    empty_el, noloop_el, simple_el, fully_connected_el, non_connected_el
):
    assert topo_sort(empty_el) == []
    assert topo_sort(noloop_el) == [1, 3, 2, 0]
    assert topo_sort(simple_el) == [3, 2, 1, 0]
    assert topo_sort(fully_connected_el) == [4, 3, 2, 1, 0]
    assert topo_sort(non_connected_el) == [3, 2, 1, 0, 5, 6, 4]
