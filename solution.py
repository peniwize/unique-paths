# Start of "solution.py".

from collections import deque
import inspect
import time
from typing import List
from typing import Optional
from typing import Set

"""
    There is a robot on an m x n grid. The robot is initially located at the 
    top-left corner (i.e., grid[0][0]). The robot tries to move to the 
    bottom-right corner (i.e., grid[m - 1][n - 1]). The robot can only move 
    either down or right at any point in time.

    NOTE: 'm' is the height (y); 'n' is the width (x).

    Given the two integers m and n, return the number of possible unique paths 
    that the robot can take to reach the bottom-right corner.

    The test cases are generated so that the answer will be less than or equal 
    to 2 * 109.

    Constraints:

        * 1 <= m, n <= 100
"""

"""
    Brute force solution.

    Example 1 (m=3, n=7):

      n 0   1   2   3   4   5   6
    m +---+---+---+---+---+---+---+
    0 | A | B | C | D | E | F | G |
      +---+---+---+---+---+---+---+
    1 | H | I | J | K | L | M | N |
      +---+---+---+---+---+---+---+
    2 | O | P | Q | R | S | T | U |
      +---+---+---+---+---+---+---+
    
    Count the number of unique paths from "A" (0, 0) to "Z" (6, 2).
    One of two directions can be chosen at each spot: right or down.
    The number of PATHS is the number of conbinations this produces.
    Since each spot has two choices, this can be modeled as a binary 
    decision tree:

              A
        B           H
     C     I     I     O
    D J   J P   J P   P ∅
    ...   ...   ...   ...

    Eventually the bottom right corner (U) will be reached through recursion.
    There is always one path from this cell to itself.  Backing up one 
    recursive step, we get to either 'N' or 'T'.  There is one path from these
    cells to 'U'.  However backing up one more recursive step to 'M' yields 
    TWO paths: M->N->U and M->T->U.  Backing up through the recursion and 
    solving the path count for each cell yields:

      n 0      1      2      3      4      5      6
    m +------+------+------+------+------+------+------+
    0 | A 28 | B 21 | C 15 | D 10 | E  6 | F  3 | G  1 |
      +------+------+------+------+------+------+------+
    1 | H  7 | I  6 | J  5 | K  4 | L  3 | M  2 | N  1 |
      +------+------+------+------+------+------+------+
    2 | O  1 | P  1 | Q  1 | R  1 | S  1 | T  1 | U  1 |
      +------+------+------+------+------+------+------+

    M = T + N
    L = M + S
    K = L + R
    ...
    F = M + G
    E = F + L
    D = K + E
    ...
    A = H + B

    The formula is: grid[y][x] = grid[y][x+1] + grid[y+1][x]
    
    Example 2: (m=3, n=2):

      n 0   1
    m +---+---+
    0 | A | B |
      +---+---+
    1 | C | D |
      +---+---+
    2 | E | F |
      +---+---+

    Corresponding "perfect" binary decision tree:
    
    0:                       A
    1:           C                       B
    2:     E           D           D           ∅
    3:  ∅     F     F     ∅     F     ∅     ∅     ∅
    4: ∅ ∅   ∅ ∅   ∅ ∅   ∅ ∅   ∅ ∅   ∅ ∅   ∅ ∅   ∅ ∅

    Depth of "perfect" binary tree: 2**(m+n)-1 => 2**5-1 = 31
    
    The reason it is '2**(m+n)' [2 to the power of m PLUS n] rather than 
    '2**(m*n)' is because a binary choice is not NOT made at every cell in 
    the WHOLE GRID, but rather at every cell in the PATHS through the grid 
    (to the destination).  The depth of the decision tree is related to 
    m PLUS n because you move either right or down at each step and your 
    choice is limited to only down when the right-most column is reached 
    and your choice is limited to only right when the bottom-most row is
    reached.

    The tree illustrates dead ends (non-existent nodes) with '∅'.  These 
    nodes are reached when the recursion is called with cooridnates that are 
    out of bounds.  The recursion stops when node 'F' is reached, but the 
    dead ends that can be reached from node 'F' are still modeled in the 
    "perfect" binary tree because they still theoretically exist and may be 
    reached, e.g. if the test for whether or not the target coordinate has 
    been reached comes AFTER the recusive calls.

    Since each node in the decision tree is visited:

    Time = O(2**[m+n]-1) => O(2**[m+n])
           Less because several recursive calls stop when '∅' is reached,
           which prevents the lowest level of the decision tree from being 
           reached thus pruning those sub-branches.

    Space = O(m+n)  [maximum call stack depth]
"""
class Solution1_BruteForce:
    def uniquePaths(self, m: int, n: int) -> int:
        def __helper(m, n, x = 0, y = 0):
            if x == n or y == m: return 0
            if x == n - 1 and y == m - 1: return 1
            return __helper(m, n, x + 1, y) \
                   + __helper(m, n, x, y + 1)
        return __helper(m, n)

"""
    This solution caches the result for every coordinate in the 2D grid, 
    which prevents all sub-problems from being solved more than once.
    This results in each cell in the grid being visited once.  While some 
    cells are technically visited more than once (to retrieve the memoized
    value) the work done during each visit is constant.

    Time = O(m*n)

    Space = O(m+n + m*n) => O(m*n)
            m+n: call stack
            m*n: memoized values
"""
class Solution2_DP_TopDown:
    def uniquePaths(self, m: int, n: int) -> int:
        def __helper(m, n, cache = {(n - 1, m - 1): 1}, x = 0, y = 0):
            if x == n or y == m: return 0
            if (x, y) in cache: return cache[(x, y)]
            result = __helper(m, n, cache, x + 1, y) \
                     + __helper(m, n, cache, x, y + 1)
            cache[(x, y)] = result
            return result
        return __helper(m, n)

"""
    This solution takes advantage of several characteristics from example 1:

        Example 1 (m=3, n=7):

      n 0   1   2   3   4   5   6
    m +---+---+---+---+---+---+---+
    0 | A | B | C | D | E | F | G |
      +---+---+---+---+---+---+---+
    1 | H | I | J | K | L | M | N |
      +---+---+---+---+---+---+---+
    2 | O | P | Q | R | S | T | U |
      +---+---+---+---+---+---+---+

    Eventually the bottom right corner (U) will be reached through recursion.
    There is always one path from this cell to itself.  Backing up one 
    recursive step, we get to either 'N' or 'T'.  There is one path from these
    cells to 'U'.  However backing up one more recursive step to 'M' yields 
    TWO paths: M->N->U and M->T->U.  Backing up through the recursion and 
    solving the path count for each cell yields:

      n 0      1      2      3      4      5      6
    m +------+------+------+------+------+------+------+
    0 | A 28 | B 21 | C 15 | D 10 | E  6 | F  3 | G  1 |
      +------+------+------+------+------+------+------+
    1 | H  7 | I  6 | J  5 | K  4 | L  3 | M  2 | N  1 |
      +------+------+------+------+------+------+------+
    2 | O  1 | P  1 | Q  1 | R  1 | S  1 | T  1 | U  1 |
      +------+------+------+------+------+------+------+

    Notice that the bottom row and right colums are all 1's so there is no 
    need to calculate those values.  Furthermore, the value of colums [n-2, 0]
    are always col[i] += col[i+1], which means a single row array can be
    used to iteratively calculate all values from rows [m-2, 0].

    Time = O((m-1) * (n-1)) => O(m*n)

    Space = O(n)
"""
class Solution3_DP_BottomUp:
    def uniquePaths(self, m: int, n: int) -> int:
        cache = [1] * n
        for row in range(m - 1):
            for col in range(n - 2, -1, -1):
                cache[col] += cache[col + 1]
        return cache[0]

"""
    This is the same solution as 'Solution3_DP_BottomUp', except the 
    iteration is from [1, n] rather than from [n - 2, 0], which may 
    run faster.

    Time = O((m-1) * (n-1)) => O(m*n)

    Space = O(n)
"""
class Solution4_DP_BottomUp:
    def uniquePaths(self, m: int, n: int) -> int:
        cache = [1] * n
        for row in range(m - 1):
            for col in range(1, n):
                cache[col] += cache[col - 1]
        return cache[n - 1]

def test1(solution):
    m = 3
    n = 7
    expected = 28
    startTime = time.time()
    result = solution.uniquePaths(m, n)
    endTime = time.time()
    print("{}:{}({:.6f} sec) result = {}".format(inspect.currentframe().f_code.co_name, type(solution), endTime - startTime, result))
    assert(expected == result)

def test2(solution):
    m = 3
    n = 2
    expected = 3
    startTime = time.time()
    result = solution.uniquePaths(m, n)
    endTime = time.time()
    print("{}:{}({:.6f} sec) result = {}".format(inspect.currentframe().f_code.co_name, type(solution), endTime - startTime, result))
    assert(expected == result)

def test100(solution):
    m = 1
    n = 1
    expected = 1
    startTime = time.time()
    result = solution.uniquePaths(m, n)
    endTime = time.time()
    print("{}:{}({:.6f} sec) result = {}".format(inspect.currentframe().f_code.co_name, type(solution), endTime - startTime, result))
    assert(expected == result)

if "__main__" == __name__:
    test1(Solution1_BruteForce())
    test1(Solution2_DP_TopDown())
    test1(Solution3_DP_BottomUp())
    test1(Solution4_DP_BottomUp())

    test2(Solution1_BruteForce())
    test2(Solution2_DP_TopDown())
    test2(Solution3_DP_BottomUp())
    test2(Solution4_DP_BottomUp())

    test100(Solution1_BruteForce())
    test100(Solution2_DP_TopDown())
    test100(Solution3_DP_BottomUp())
    test100(Solution4_DP_BottomUp())

# End of "solution.py".
