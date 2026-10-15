import Challenge
open NonuniformCostUnanimousVote
example : expectedCost ([((1:Rat)/2),((1:Rat)/2),((1:Rat)/2)], [1,1,1], 0) [0,1,2] = (5:Rat)/2 := by native_decide
example : expectedCost ([], [], 0) [] = 0 := by native_decide
