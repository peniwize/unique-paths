/*!
    \file "main.cpp"

    Author: Matt Ervin <matt@impsoftware.org>
    Formatting: 4 spaces/tab (spaces only; no tabs), 120 columns.
    Doc-tool: Doxygen (http://www.doxygen.com/)

    https://leetcode.com/problems/unique-paths/
*/

//!\sa https://github.com/doctest/doctest/blob/master/doc/markdown/main.md
#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN

#include "utils.hpp"

/*
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
*/

/*!
    This is the same solution as 'Solution3_DP_BottomUp', except the 
    iteration is from [1, n] rather than from [n - 2, 0], which may 
    run faster.

    Time = O((m-1) * (n-1)) => O(m*n)

    Space = O(n)
    
    See also: 'solution.py'
    See also: https://leetcode.com/problems/unique-paths/solutions/4718603/python-brute-force-dp-full-explanation-t-o-m-n-s-o-n/
*/
class Solution {
public:
    int uniquePaths(int m, int n) {
        int cache[n];
        std::fill_n(cache, n, 1);
        for (int row = m - 1; row; --row) {
            for (int col = 1; n > col; ++col) {
                cache[col] += cache[col - 1];
            }
        }
        return cache[n - 1];
    }
};

// {----------------(120 columns)---------------> Module Code Delimiter <---------------(120 columns)----------------}

namespace doctest {
    const char* testName() noexcept { return doctest::detail::g_cs->currentTest->m_name; }
} // namespace doctest {

TEST_CASE("Case 1")
{
    cerr << doctest::testName() << '\n';
    int const m = 3;
    int const n = 7;
    int const expected = 28;
    auto solution = Solution{};
    { // New scope.
        auto const start = std::chrono::steady_clock::now();
        auto const result = solution.uniquePaths(m, n);
        CHECK(expected == result);
        cerr << "Elapsed time: " << elapsed_time_t{start} << '\n';
    }
    cerr << "\n";
}

TEST_CASE("Case 2")
{
    cerr << doctest::testName() << '\n';
    int const m = 3;
    int const n = 2;
    int const expected = 3;
    auto solution = Solution{};
    { // New scope.
        auto const start = std::chrono::steady_clock::now();
        auto const result = solution.uniquePaths(m, n);
        CHECK(expected == result);
        cerr << "Elapsed time: " << elapsed_time_t{start} << '\n';
    }
    cerr << "\n";
}

/*
    End of "main.cpp"
*/
