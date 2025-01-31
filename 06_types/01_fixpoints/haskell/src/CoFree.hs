module CoFree (CoFree(..), Fix) where

import Lib ( ShowableFunctor(..) )

data CoFree f a = CoFree {tag :: a, content :: f (CoFree f a)}
type Fix f = CoFree f ()

instance (ShowableFunctor f, Show a) => Show (CoFree f a) where
    show :: ShowableFunctor f => CoFree f a -> String
    show (CoFree tag content) = "CoFree {tag: " ++ show tag ++ ", content: " ++ showF content ++ "}"

instance Functor f => Functor (CoFree f) where
    fmap :: Functor f => (a -> b) -> CoFree f a -> CoFree f b
    fmap f (CoFree x xs) = CoFree (f x) (fmap (fmap f) xs)

instance Applicative f => Applicative (CoFree f) where
    pure :: Applicative f => a -> CoFree f a
    pure x = CoFree x (pure (pure x))

    (<*>) :: Applicative f => CoFree f (a -> b) -> CoFree f a -> CoFree f b
    (CoFree f fs) <*> (CoFree x xs) = CoFree (f x) (fmap (<*>) fs <*> xs)

instance Monad f => Monad (CoFree f) where
    (>>=) :: Monad f => CoFree f a -> (a -> CoFree f b) -> CoFree f b
    (CoFree x xs) >>= f = 
        let CoFree y ys = f x
        in CoFree y (xs >>= fmap (>>= f) . content)

