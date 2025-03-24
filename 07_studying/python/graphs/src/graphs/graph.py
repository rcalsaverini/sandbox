from collections import defaultdict
from typing import TypeVar, Protocol, Generic, Iterable

A = TypeVar("A")
B = TypeVar("B")


class Visitor(Protocol, Generic[A, B]):
    def __call__(self, node: int, context: B | None, graph: "Graph") -> A:
        pass


class Graph(Protocol):
    @classmethod
    def from_edges(cls, edges: list[(int, int)]) -> "Graph":
        pass

    def get_nodes(self) -> set[int]:
        pass

    def get_neighbors(self, node: int) -> set[int]:
        pass

    def dfs_preorder(self: "Graph", start: int, visitor: Visitor[A, B]) -> Iterable[A]:
        visited = set()
        stack = [(start, None)]
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                yield visitor(node, self)
                for neighbor in self.get_neighbors(node):
                    stack.append(neighbor)

    def dfs_postorder(self: "Graph", start: int, visitor: Visitor[A]) -> Iterable[A]:
        visited = set()
        stack = [start]
        while stack:
            node, neighbors = stack.pop()
            if node not in visited:
                visited.add(node)
                yield visitor(node, neighbors)
                for neighbor in self.get_neighbors(start):
                    stack.append((neighbor, self.get_neighbors(neighbor)))
