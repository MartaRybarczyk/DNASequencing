import numpy as np
import copy

from src.usefullFunctions import choose_next_oligo, max_common_part, find_best_subpath, choose_init_oligo
from src.solution import Solution
from src.sequenceFactory import generateSampleOligo

def greedyHeuristic(S, init_oligo_index=None, n=None, l=None, choose_next_alg='greedy', use_phermone=False, phermone_model=None, backward=False):

    copyS = copy.deepcopy(S)

    solution_l = 0 # number of oligo in sequence
    solution_c = 0 # total length of current solution

    solution = Solution()

    if init_oligo_index is not None:
        solution.add_oligo(copyS[init_oligo_index], vertex_no=init_oligo_index)
    else:
        init = choose_init_oligo(copyS)
        solution.add_oligo(S[init], vertex_no=init)

    solution_c = l
    solution_l = 1

    while solution.path_len < n and solution_l < n - l + 1:
        
        last_vertex = solution.graph_path[-1]

        phermone_values = np.array([i[last_vertex] for i in phermone_model])
        index = choose_next_oligo(solution.path[-1], copyS, choose_next_alg, use_phermone=use_phermone, phermone_model=phermone_values)

        solution_l += 1

        solution.add_oligo(copyS.pop(index), index)

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
        solution.add_oligo(copyS.pop(index), index)

    if solution.path_len < n:
        solution.add_oligo(copyS[0])

    if solution.path_len > n:
        find_best_subpath(solution.path, n)

    return solution


if __name__ == "__main__":

    pass