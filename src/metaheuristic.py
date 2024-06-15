from src import heuristics, solution, constants
from src.usefullFunctions import objective_function, roundFloat, max_common_part, set_global_parameters
import random
import numpy as np
import math
from copy import deepcopy
from src.sequenceFactory import generateSampleOligo, get_data_from_file
import time
import os

def apply_phermone_update(cf, bs_update, T, pib, prb, pbs):

    ar = np.zeros(np.shape(T))
    m1 = constants.kib * delta(pib, np.zeros(np.shape(T)))
    m2 = constants.krb * delta(prb, np.zeros(np.shape(T)))
    m3 = constants.kbs * delta(pbs, np.zeros(np.shape(T)))
    m = m1 + m2 + m3
    T += constants.rho * (m - T)

    T = np.clip(T, 0.01, 0.99)

def delta(solution, array):

    for i in range(1, len(solution.graph_path) - 1):
        array[solution.graph_path[i]][solution.graph_path[i + 1]] += 1

    return array

def compute_convergence_factor(T):
    
    _max = np.max(T)
    _min = np.min(T)

    return 2 * ((np.sum(np.maximum(_max - T, T - _min)) / (np.size(T) * (_max - _min))) - 0.5)

def initialize_phermone_values(phermone_matrix):
    
    phermone_matrix.fill(0.5)

def reset_phermone_values(T):
    initialize_phermone_values(T)

def delete_phermone(phermone_matrix, index=None):

    if index != None and index >= 0 and index < np.size(phermone_matrix)[0]:
        phermone_matrix = np.delete(phermone_matrix, index, axis=0)
        phermone_matrix = np.delete(phermone_matrix, index, axis=1)

def terminate_search(duration):
    
    if duration > constants.MAX_DURATION:
        return True

    return False

def ACO_metaheuristic(range_of_appearance, S, n, l, initial_oligo=None, debug=False, gather_stats=False, stats=None):
    """
    ## Ant Cology Optimization algorithm.\n
    ### Parameters:
    - S: set of oligo
    - initial_oligo: first oligo
    - n: length of the original sequence
    - l: length of the oligo\n
    ## Returns:
    - solution: Solution object, representing best found solution
    """
    pib = None
    pbs = None
    prb = None
    random.seed(0)

    if stats is not None:
        stats["iterNo"] = 0 # number of iterations
        stats["resetNo"] = 0 # number of resets
        stats["bestChangeCount"] = 0 # counts how many best solution has changed
        current_time = 0   
        current_solution_value = 0 # objective function of current best solution
        current_best_value = 0

        # for plotting change of the best solution in time and iteration
        stats["time_series"] = []
        stats["best_solution_series"] = []
        stats["current_solution_series"] = []
        stats["iter_no_series"] = []

    nf = constants.NF
    nb = constants.NB

    conv_factor = 0
    bs_update = False

    phermone_matrix = np.zeros((len(S) + 1, len(S) + 1))

    if debug == True:
        print('Initializing values...')

    initialize_phermone_values(phermone_matrix)

    phermone_copy = deepcopy(phermone_matrix) # this matrix will change within one iteration

    edge_matrix = np.zeros((len(S), len(S)), dtype=int)

    for i in range(edge_matrix.shape[0]):
        for j in range(edge_matrix.shape[1]):
            edge_matrix[i][j] = max_common_part(S[i], S[j])

    algorithm_start = time.time()
    duration = 0
    while terminate_search(duration) == False:

        if gather_stats:
            stats["iterNo"] += 1
            stats["iter_no_series"].append(stats["iterNo"])
            stats["time_series"].append(roundFloat(duration, 2))
            stats["current_solution_series"].append(current_solution_value)
            stats["best_solution_series"].append(current_best_value)


        if debug == True:
            print('New iteration')

        pib = solution.Solution()
        for i in range(nf):
            current_solution = heuristics.greedyHeuristic(
                range_of_appearance, S, initial_oligo, n, l, use_phermone=True, phermone_model=phermone_matrix, 
                commons_matrix=edge_matrix
            )
            if objective_function(current_solution) > objective_function(pib):
                pib = deepcopy(current_solution)
        for i in range(nb):
            current_solution = heuristics.greedyHeuristic(
                range_of_appearance, S, initial_oligo, n, l, use_phermone=True, phermone_model=phermone_matrix,
                backward=True
            )
            if objective_function(current_solution) > objective_function(pib):
                pib = deepcopy(current_solution)

        if gather_stats:
            current_solution_value = objective_function(pib)
        if prb == None or objective_function(pib) > objective_function(prb):
            prb = deepcopy(pib)
        if pbs == None or objective_function(pib) > objective_function(pbs):
            pbs = deepcopy(pib)
            current_best_value = objective_function(pbs)
            if gather_stats:
                stats["bestChangeCount"] += 1

        if debug:
            print(
                'Iteration best: ', objective_function(pib), 
                'Reset best: ', objective_function(prb), 
                'Best found: ', objective_function(pbs), 'Convergence factor:', conv_factor
            )

        apply_phermone_update(conv_factor, bs_update, phermone_matrix, pib, prb, pbs)
        conv_factor = compute_convergence_factor(phermone_matrix)

        if conv_factor > constants.CONV_THRESHOLD:
            if bs_update == True:
                reset_phermone_values(phermone_matrix)
                if stats is not None:
                    stats["resetNo"] += 1
                if debug:
                    print('Reset phermone values.')
                prb = None
                bs_update = False
            else:
                bs_update = True
        
        duration = time.time() - algorithm_start
        
        if(objective_function(pbs)) == n - l + 1:
            print("seconds:", duration)
            print("miliseconds:", duration * 1000)
            print("microseconds:", duration * 10 ** 6)
            return pbs

    # if gather_stats:
    #     print(stats)

    print(objective_function(pbs))
    return pbs
        

if __name__ == "__main__":

    work_path = os.path.dirname(os.path.realpath(__file__))
    stats = {}
    
    set_global_parameters(
        _max_duration=20,
        _crd_list=3,
        _nf=3,
        _nb=0,
        _det_rate=0.95,
        _init_det_rate=0.25,
        _init_crd=20,
        _kib=0.3, _krb=0.3, _kbs=0.4
    )

    n, l, S = get_data_from_file(work_path + '/../testFiles/benchmark/error_rate_20/stand20/20/400_10')

    with open(work_path + '/../testFiles/benchmark/error_rate_20/sequence/400_10.seq', 'r') as f:
        seq = f.read()

    result = ACO_metaheuristic(S, n, l, debug=True, gather_stats=True, stats=stats)

    print(result)

    print('quality:', solution.solutionQuality(result, seq, n, l, name='needleman-wunsch'))

    print('valid:', solution.is_valid(result, S))