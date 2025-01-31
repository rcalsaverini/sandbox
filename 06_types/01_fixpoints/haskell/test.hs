

newtype Fix f = Fix { unFix :: f (Fix f) }

data CoFree f a = CoFree {tag :: a, content :: f (CoFree f a)}

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

data UserF a = UserF
    { name :: String
    , age :: Int
    , friends :: [a]
    } deriving (Show, Functor)

type User = Fix UserF
type UserId = CoFree UserF Int

instance Show User where
    show :: User -> String
    show (Fix (UserF name age friends)) = "User {name: " ++ name ++ ", age: " ++ show age ++ ", friends: " ++ show friends ++ "}"

instance Show UserId where
    show :: UserId -> String
    show (CoFree tag content) = "UserId {userId: " ++ show tag ++ ", user: " ++ show content ++ "}"

-- newtype User = User (UserF User) deriving(Show)
-- data UserId = UserId {userId:: Int, user :: UserF UserId} deriving(Show)

store :: User -> UserId
store (Fix u) = CoFree 0 (fmap store u)

user :: String -> Int -> [User] -> User
user name age friends = Fix (UserF name age friends)

john :: User
john = user "John" 30 []

father :: User
father = user "Father" 60 [john]

main :: IO ()
main = do
    print john
    print father
