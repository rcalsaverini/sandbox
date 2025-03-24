use rstest::*;
use std::{ collections::{ HashMap, HashSet }, hash::Hash };
mod graph;

fn main() {
    println!("Hello, world!");
}

type Node = i32;
// #[derive(Debug, Clone, Copy, Hash)]
// struct Edge<const DIRECTED: bool> {
//     from: Node,
//     to: Node,
// }

// impl<const DIRECTED: bool> PartialEq for Edge<DIRECTED> {
//     fn eq(&self, other: &Self) -> bool {
//         match DIRECTED {
//             true => self.from == other.from && self.to == other.to,
//             false =>
//                 (self.from == other.from && self.to == other.to) ||
//                     (self.from == other.to && self.to == other.from),
//         }
//     }
// }

// impl<const DIRECTED: bool> Eq for Edge<DIRECTED> {}

trait Graph<const DIRECTED: bool> {
    fn from_edges<const N: usize>(edges: [Edge<DIRECTED>; N]) -> Self;
    fn get_nodes(&self) -> HashSet<Node>;
    fn get_edges(&self) -> HashSet<Edge<DIRECTED>>;
}

trait DirectedGraph: Graph<true> {
    fn get_parents(&self, node: Node) -> HashSet<Node>;
    fn get_children(&self, node: Node) -> HashSet<Node>;
}

trait UndirectedGraph: Graph<false> {
    fn get_neighbors(&self, node: Node) -> HashSet<Node>;
}

type GraphAL<const DIRECTED: bool> = HashMap<Node, HashSet<Node>>;

impl<const DIRECTED: bool> Graph<DIRECTED> for GraphAL<DIRECTED> {
    fn from_edges<const N: usize>(edges: [Edge<DIRECTED>; N]) -> Self {
        let mut graph = HashMap::new();
        for edge in edges.iter() {
            graph.entry(edge.from).or_insert(HashSet::new()).insert(edge.to);
            if !DIRECTED {
                graph.entry(edge.to).or_insert(HashSet::new()).insert(edge.from);
            }
        }
        graph
    }

    fn get_nodes(&self) -> HashSet<Node> {
        self.keys().copied().collect()
    }

    fn get_edges(&self) -> HashSet<Edge<DIRECTED>> {
        self.iter()
            .flat_map(|(from, tos)| { tos.iter().map(move |to| Edge { from: *from, to: *to }) })
            .collect()
    }
}

impl DirectedGraph for GraphAL<true> {
    fn get_parents(&self, node: Node) -> HashSet<Node> {
        self.iter()
            .filter(|(_, tos)| tos.contains(&node))
            .map(|(from, _)| *from)
            .collect()
    }

    fn get_children(&self, node: Node) -> HashSet<Node> {
        self.get(&node).cloned().unwrap_or_default()
    }
}

impl UndirectedGraph for GraphAL<false> {
    fn get_neighbors(&self, node: Node) -> HashSet<Node> {
        self.get(&node).cloned().unwrap_or_default()
    }
}
