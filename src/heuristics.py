import numpy as np
import copy

from src.usefullFunctions import choose_next_oligo, max_common_part, find_best_subpath, choose_init_oligo
from src.solution import Solution, is_valid
from src.sequenceFactory import generateSampleOligo
from src.constants import MAX_OLIGO_LEN

def greedyHeuristic(S, init_oligo_index=None, n=None, l=None, choose_next_alg='greedy', use_phermone=False, phermone_model=None, backward=False,
        commons_matrix=None    
    ):

    precomputed_com = False

    if commons_matrix is not None and type(commons_matrix) == np.ndarray:
        precomputed_com = True
        for i in range(commons_matrix.shape[0]):
            commons_matrix[i][i] = 1

    copyS = copy.deepcopy(S)

    solution_l = 0 # number of oligo in sequence
    solution_c = 0 # total length of current solution

    solution = Solution()

    if init_oligo_index is not None:
        solution.add_oligo(copyS[init_oligo_index], vertex_no=init_oligo_index)
    else:
        init = choose_init_oligo(copyS, 'greedy')
        solution.add_oligo(copyS.pop(init), vertex_no=init)
        if precomputed_com == True:
            commons_matrix[init][init] = -1

    solution_c = l
    solution_l = 1

    while solution.path_len < n and solution_l < n - l + 1:
        
        last_vertex = solution.graph_path[-1]

        phermone_values = None
        if use_phermone == True:
            phermone_values = phermone_model[:, last_vertex]
        index = choose_next_oligo(solution.path[-1], copyS, choose_next_alg, use_phermone=use_phermone, phermone_model=phermone_values, 
            commons_matrix=commons_matrix, index_prec=last_vertex
        )

        solution_l += 1

        solution.add_oligo(copyS.pop(index), index)
        if precomputed_com:
            commons_matrix[index][index] = -1

    if solution.path_len > n:
        find_best_subpath(solution, n)

    return solution

def greedyLagHeuristic(S, init_oligo_index, n, l, commons_matrix=None):

    copyS = copy.deepcopy(S)
    solution_l = 0

    prec_com = False
    if commons_matrix is not None and type(commons_matrix) == np.ndarray:
        prec_com = True
        for i in range(commons_matrix.shape[0]):
            commons_matrix[i][i] = 1

    solution = Solution()

    if init_oligo_index is None:
        init = choose_init_oligo(copyS, 'random')
        solution.add_oligo(copyS.pop(init), init)
        if prec_com:
            commons_matrix[init][init] = -1
    else:
        solution.add_oligo(copyS[init_oligo_index], init_oligo_index)
    
    solution_l = 1

    while solution.path_len < n and len(copyS) > 1:
        
        last_vertex = solution.graph_path[-1]

        index = choose_next_oligo(solution.path[-1], copyS, 'greedy_lag', commons_matrix=com_matrix, index_prec=last_vertex)
        solution_l += 1
        solution.add_oligo(copyS.pop(index), index)
        if prec_com:
            commons_matrix[index][index] = -1

    # if solution.path_len < n:
    #     solution.add_oligo(copyS[0])

    if solution.path_len > n:
        find_best_subpath(solution, n)

    return solution


if __name__ == "__main__":

    init_oligo, last_oligo, S = generateSampleOligo(8, 400, initial_oligo=False, last_oligo=False)

    com_matrix = np.zeros((len(S), len(S)), dtype=int)

    for i in range(com_matrix.shape[0]):
        for j in range(com_matrix.shape[1]):
            com_matrix[i][j] = max_common_part(S[i], S[j])

    solution = greedyLagHeuristic(S, None, 400, 8, commons_matrix=com_matrix)

    print(solution)

    print(is_valid(solution, S))