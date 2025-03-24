mod edge;
mod graph;

type Node = i32;

// type Node = i32;
// type Edge = (Node, Node);

// trait Graph {
//     fn from_edges<const N: usize>(edges: [Edge; N]) -> Self;
//     fn get_nodes(&self) -> Vec<i32>;
//     fn get_edges(&self) -> Vec<(i32, i32)>;
//     fn get_neighbors(&self, node: i32) -> Vec<i32>;
// }

// trait Visitor<G: Graph, Context, Output> {
//     fn visit(node: i32, graph: G, context: Context) -> Output;
//     fn context_update(node: i32, parent: i32, graph: G, context: Context) -> Context;
// }

// fn dfs<G: Graph, V: Visitor<G, C, O>, C, O>(
//     graph: G,
//     start: i32,
//     context: C,
//     visitor: V
// ) -> Vec<O> {
//     let nodes = graph.get_nodes();
//     let mut visited = vec![false; nodes.len()];
//     let mut stack: Vec<(i32, C)> = Vec::new();
//     let mut output: Vec<O> = Vec::new();
//     stack.push((start, context));
//     while let Some((node, context)) = stack.pop() {
//         if visited[node as usize] {
//             continue;
//         }
//         visited[node as usize] = true;
//         output.push(visitor.visit(node, graph, context));
//         let neighbors = graph.get_neighbors(node);
//         for neighbor in neighbors {
//             stack.push((neighbor, V::context_update(neighbor, node, graph, context)));
//         }
//     }
// }
