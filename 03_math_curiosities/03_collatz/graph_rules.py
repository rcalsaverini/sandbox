from dataclasses import dataclass
from domain import Rule
from iterate_rules import iterate_rule
from matplotlib import pyplot as plt
from matplotlib.transforms import Bbox
from networkx import DiGraph # type: ignore
from seaborn import color_palette # type: ignore
from sympy import factorint, isprime
from typing import Callable, List, Tuple, Dict
from typing import List, Tuple
import networkx as nx # type: ignore


Color = str | Tuple[int, int, int] | None
Layout = Dict[int, Tuple[int, int]]
Layouter = Callable[[DiGraph], Layout]
Labeller = Callable[[int], str]
Colorizer = Callable[[int], Color]
Displayer = Callable[[DiGraph, Layout, plt.Axes], None]

def build_graph(update_rule: Rule, starting_points: List[int], max_iterations: int) -> DiGraph:
    graph = DiGraph()
    iterated_rule = iterate_rule(update_rule, max_iterations=max_iterations)
    orbits = [iterated_rule(starting_point) for starting_point in starting_points]
    graph.add_nodes_from(node for orbit in orbits for node in orbit)
    for orbit in orbits:
        graph.add_edges_from(zip(orbit, orbit[1:]))
    return graph


# common layouters

def dot_layout(graph: nx.Graph) -> Layout:
    return nx.nx_agraph.graphviz_layout(graph, prog="dot", args="-Grankdir=LR -Gsplines=ortho")

def kamada_kawai_layout(graph: nx.Graph) -> Layout:
    return nx.kamada_kawai_layout(graph, weight=None, scale=1, center=None, dim=2)

def spring_layout(graph: nx.Graph) -> Layout:
    return nx.spring_layout(graph, k=0.5, pos=None, fixed=None, iterations=50, threshold=0.0001, weight=None, scale=1, center=None, dim=2, seed=None)


# common colorizers

def color_by_divisor(node, max_colors=100):
    if node == 1:
        return "silver"
    pallete = color_palette("Set2", max_colors)
    max_divisor = max(factorint(node))
    return pallete[max_divisor] if max_divisor < max_colors else "silver"

def color_by_primality(node):
    if isprime(node):
        return "darkorange"
    else:
        return "steelblue"

# graph drawer
@dataclass
class GraphDisplayer:
    node_displayer: Callable[[DiGraph, Layout, plt.Axes], None]
    edge_displayer: Callable[[DiGraph, Layout, plt.Axes], None]
    label_displayer: Callable[[DiGraph, Layout, plt.Axes], None]
    post_display: Callable[[plt.Axes], None]   
    
    def display(self, graph: DiGraph, node_positions: Layout, ax: plt.Axes) -> None:
        self.node_displayer(graph, node_positions, ax)
        self.edge_displayer(graph, node_positions, ax)
        self.label_displayer(graph, node_positions, ax)
    
    @staticmethod    
    def _get_displayed_elements(ax: plt.Axes):
        queue = [e for e in ax.get_children()] # type: ignore
        output = []
        while len(queue) > 0:
            element = queue.pop()
            queue.extend(element.get_children())
            output.append(element)
        return output

    
def create_colorized_node_displayer(colorizer: Colorizer, node_size: int, node_shape: str="o") -> Displayer:
    def colorized_node_displayer(graph: DiGraph, node_positions: Layout, ax: plt.Axes) -> None:
        colors = [colorizer(node) for node in graph.nodes]
        nx.draw_networkx_nodes(graph, node_positions, node_size=node_size, node_shape="o", node_color=colors, ax=ax)
        
    return colorized_node_displayer

def create_edge_displayer(arrow_size: int, node_size: int, arrowstyle: str="-|>", connectionstyle: str="arc3,rad=0.05") -> Displayer:    
    def edge_displayer(graph: DiGraph, node_positions: Layout, ax: plt.Axes) -> None:
        nx.draw_networkx_edges(
            graph,
            node_positions,
            arrows=True,
            arrowsize=arrow_size,
            arrowstyle=arrowstyle,
            node_size=node_size * 1.1,
            connectionstyle=connectionstyle,
            ax=ax
        )
    return edge_displayer

def create_label_displayer(labeller: Labeller, font_size) -> Displayer:
    def label_displayer(graph: DiGraph, node_positions: Layout, ax: plt.Axes) -> None:
        labels = {node: labeller(node) for node in graph.nodes}
        nx.draw_networkx_labels(graph, node_positions, labels, font_size=font_size, ax=ax)

    return label_displayer

def truncate_big_numbers(node: int) -> str:
    label = str(node)
    if len(label) > 6 and node > 0:
        return label[0:1] + "..." + label[-2:-1]
    elif len(label) > 6 and node < 0:
        return label[0:2] + "..." + label[-2:-1]
    return label
    
def make_padding_fixer(x_padding: float, y_padding: float) -> Callable[[plt.Axes], None]:
    def padding_fixer(ax: plt.Axes) -> None:
        bboxes = Bbox.union([e.get_bbox() for e in self._get_displayed_elements(ax) if hasattr(e, "get_bbox")]) # type: ignore
        ax.set_xlim(bboxes.xmin - x_padding, bboxes.xmax + x_padding)
        ax.set_ylim(bboxes.ymin - y_padding, bboxes.ymax + y_padding)

    return padding_fixer

def make_canvasser(figsize: Tuple[int, int]) -> Callable[[], Tuple[plt.Figure, plt.Axes]]:
    def canvasser() -> Tuple[plt.Figure, plt.Axes]:
        fig, ax = plt.subplots(figsize=figsize)
        return fig, ax
    return canvasser

@dataclass
class GraphDrawer:
    layouter: Layouter
    canvasser: Callable[[], Tuple[plt.Figure, plt.Axes]]
    graph_displayer: GraphDisplayer
    
    
    @classmethod
    def create_default(
            cls, 
            figsize: Tuple[int, int],
            node_size: int,
            arrow_size: int,
            font_size: int,
            colorizer: Colorizer=color_by_primality,
            padding: float=0.05,
            labeller: Labeller=truncate_big_numbers
        ) -> "GraphDrawer":
        x_padding, y_padding = padding * figsize[0], padding * figsize[1]
    
        return cls(
            layouter=dot_layout,
            canvasser=make_canvasser(figsize),
            graph_displayer=GraphDisplayer(
                node_displayer=create_colorized_node_displayer(colorizer, node_size),
                edge_displayer=create_edge_displayer(arrow_size, node_size),
                label_displayer=create_label_displayer(labeller, font_size),
                post_display=make_padding_fixer(x_padding, y_padding)
            )
        )
    
     
    def draw(self: "GraphDrawer", graph: DiGraph) -> plt.Figure:
        fig, ax = self.canvasser()
        node_positions = self.layouter(graph)
        self.graph_displayer.display(graph, node_positions, ax)
        ax.set_axis_off() # type: ignore
        fig.tight_layout()
        
        return fig
