module Lib (ShowableFunctor(..)) where

class ShowableFunctor f where
    showF :: (Show a) => f a -> String