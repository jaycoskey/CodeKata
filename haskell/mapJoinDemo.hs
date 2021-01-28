import Data.List
import Data.Map (Map)
import qualified Data.Map as Map
import Text.Printf

getTeamAvail :: Map String [Int] -> Map String [String] -> Map String [Int]
getTeamAvail memberAvailabilities teamMembers = Map.fromList availList
  where
    mem2avail :: String -> [Int]
    mem2avail b = memberAvailabilities Map.! b

    unifyN :: [[Int]] -> Int -> Bool
    unifyN xss n = any (== 1) [xs !! n | xs <- xss]

    unify :: [[Int]] -> [Int]
    unify xss = [if (unifyN xss n) then 1 else 0 | n <- [0 .. 6]]

    availList :: [(String, [Int])]
    availList = [(k, unify $ map mem2avail v) | (k, v) <- Map.toList teamMembers]


main :: IO()
main =
    let amy = "Amy"
        bob = "Bob"
        cat = "Cat"
        dan = "Dan"

        memAvailList :: [(String, [Int])]
        memAvailList = [ (amy, [1,0,0,0,0,0,1]), (bob, [1,1,1,0,0,0,0]), (cat, [0,0,0,0,1,1,1]), (dan, [1,1,0,0,0,1,1]) ]

        memberAvailabilities :: Map String [Int]
        memberAvailabilities = Map.fromList memAvailList

        dev = "Dev"
        ops = "Ops"

        teamMembers :: Map String [String]
        teamMembers = Map.fromList [(dev, [amy, bob]), (ops, [cat, dan])]

        teamAvails :: Map String [Int]
        teamAvails = getTeamAvail memberAvailabilities teamMembers

        teamAvailList :: [(String, [Int])]
        teamAvailList = Map.toList teamAvails

        printItem :: (String, [Int]) -> IO()
        printItem (k, v) = putStrLn $ show k ++ " :" ++ show v
    in mapM_ printItem teamAvailList

