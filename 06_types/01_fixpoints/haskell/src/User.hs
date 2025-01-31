module User where
import CoFree ( CoFree(CoFree), Fix)
import Lib (ShowableFunctor(..))


data UserF a = UserF
    { name :: String
    , age :: Int
    , friends :: [a]
    } deriving (Show, Functor)

instance ShowableFunctor UserF where
    showF :: (Show a) => UserF a -> String
    showF = show

type User = Fix UserF
type UserId = CoFree UserF Int

store :: User -> UserId
store (CoFree _ u) = CoFree 0 (fmap store u)

user :: String -> Int -> [User] -> User
user name age friends = CoFree () (UserF name age friends) 

john :: User
john = user "John" 30 []

father :: User
father = user "Father" 60 [john]

main :: IO ()
main = do
    print john
    print father
