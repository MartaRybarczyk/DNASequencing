import numpy as np
import copy

from initialSolution import choose_next_oligo, max_common_part, find_best_subpath
from solution import Solution
from sequenceFactory import generateSampleOligo

def greedyHeuristic(S, initial_oligo, n, l):

    copyS = copy.deepcopy(S)
    solution_l = 0
    solution_c = 0

    solution = Solution()
    solution.add_oligo(initial_oligo)
    solution_c = l
    solution_l = 1

    while solution.path_len < n and solution_l < n - l + 1:

        index = choose_next_oligo(solution.path[-1], copyS, 'greedy')
        solution_l += 1
        solution.add_oligo(copyS.pop(index))

    if solution.path_len > n:
        find_best_subpath(solution.path, n)

    return solution

def greedyLagHeuristic(S, initial_oligo, n, l):

    copyS = copy.deepcopy(S)
    solution_l = 0

    solution = Solution()
    solution.add_oligo(initial_oligo)
    solution_l = 1

    while solution.path_len < n and len(copyS) > 1:

        index = choose_next_oligo(solution.path[-1], copyS, 'greedy_lag')
        solution_l += 1
        solution.add_oligo(copyS.pop(index))

    if solution.path_len < n:
        solution.add_oligo(copyS[0])

    if solution.path_len > n:
        find_best_subpath(solution.path, n)

    return solution


if __name__ == "__main__":

    pass