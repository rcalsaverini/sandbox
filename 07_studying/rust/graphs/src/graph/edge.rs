use std::cmp::{ max, min };
use super::Node;

pub trait Edge<const DIRECTED: bool> {}

#[derive(Debug, Clone, Copy, Hash, Eq, PartialEq)]
pub struct Pair(Node, Node);
impl Pair {
    pub fn new(x: Node, y: Node) -> Self {
        Self(max(x, y), min(x, y))
    }
}

impl Edge<false> for Pair {}
impl Edge<true> for (Node, Node) {}
