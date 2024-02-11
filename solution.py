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

    Given the two integers m and n, return the number of possible unique paths 
    that the robot can take to reach the bottom-right corner.

    The test cases are generated so that the answer will be less than or equal 
    to 2 * 109.

    Constraints:

        * 1 <= m, n <= 100
"""

class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        #
        # TODO: >>> Under Construction <<<
        #
        return -1

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

if "__main__" == __name__:
    test1(Solution())
    test2(Solution())

# End of "solution.py".
