use rstest::Context;

use super::Node;
use super::edge::Edge;
use std::collections::HashSet;
use std::process::Output;

trait Graph<const DIRECTED: bool, E: Edge<DIRECTED>> {
    fn from_edges<const N: usize>(edges: [E; N]) -> Self;
    fn get_nodes(&self) -> HashSet<Node>;
    fn get_edges(&self) -> HashSet<E>;
}

trait DirectedGraph<E: Edge<true>>: Graph<true, E> {
    fn get_parents(&self, node: Node) -> HashSet<Node>;
    fn get_children(&self, node: Node) -> HashSet<Node>;
}

trait UndirectedGraph<E: Edge<false>>: Graph<false, E> {
    fn get_neighbors(&self, node: Node) -> HashSet<Node>;
}

enum SearchType {
    DFS
    BFS,
}

trait Search<const DIRECTED: bool, G: Graph<DIRECTED, E>, Context, Output, E: Edge<DIRECTED>> {
    fn visit(node: Node, graph: G, context: Context) -> Output;
    fn context_update(node: Node, parent: Node, graph: G, context: Context) -> Context;
}

// fn dfs(graph: G, start: Node, initial_context: Context) -> Vec<Output> {
//     let mut visited: HashSet<Node> = HashSet::new();
//     let mut stack: Vec<(Node, Context)> = Vec::new();
//     let mut output: Vec<Output> = Vec::new();
//     stack.push((start, initial_context));
//     while let Some((node, context)) = stack.pop() {
//         if visited.contains(&node) {
//             continue;
//         }
//         visited.insert(node);
//         output.push(Self::visit(node, graph, context));
//         if DIRECTED {
//         } else {
//             let neighbors = graph.get_neighbors(node);
//             for neighbor in neighbors {
//                 let new_context = Self::context_update(neighbor, node, graph, context);
//                 stack.push((neighbor, new_context));
//             }
//         }
//     }
//     output
// }
