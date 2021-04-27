from src import heuristics, solution, constants
from src.usefullFunctions import objective_function
import numpy as np
import math
from copy import deepcopy

def apply_phermone_update(cf, bs_update, T, pib, prb, pbs):

    pass

def compute_convergence_factor(T):
    pass

def initialize_phermone_values(phermone_matrix):
    
    phermone_matrix.fill(0.5)

def reset_phermone_values(T):
    pass

def delete_phermone(phermone_matrix, index=None):

    if index != None and index >= 0 and index < np.size(phermone_matrix)[0]:
        phermone_matrix = np.delete(phermone_matrix, index, axis=0)
        phermone_matrix = np.delete(phermone_matrix, index, axis=1)

def terminate_search():
    pass

def ACO_metaheuristic(S, initial_oligo, n, l):
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

    nf = None
    nb = None

    conv_factor = 0
    bs_update = False

    phermone_matrix = np.zeros((len(S) + 1, len(S) + 1))

    initialize_phermone_values(phermone_matrix)

    phermone_copy = deepcopy(phermone_matrix) # this matrix will change within one iteration

    while terminate_search() == False:
        pib = solution.Solution()
        for i in range(nf):
            current_solution = heuristics.greedyHeuristic(S, initial_oligo, n, l, use_phermons=True, phermone_matrix=phermone_matrix)
            if objective_function(current_solution) > objective_function(pib):
                pib = deepcopy(current_solution)
        for i in range(nb):
            current_solution = heuristics.greedyHeuristic(
                S, initial_oligo, n, l, use_phermons=True, phermone_matrix=phermone_matrix,
                backward=True
            )
            if objective_function(current_solution) > objective_function(pib):
                pib = deepcopy(current_solution)

        if prb == None or objective_function(pib) > objective_function(prb):
            prb = deepcopy(pib)
        if pbs == None or objective_function(pib) > objective_function(pbs):
            pbs = deepcopy(pib)

        apply_phermone_update(conv_factor, bs_update, phermone_matrix, pib, prb, pbs)
        conv_factor = compute_convergence_factor(phermone_matrix)

        if conv_factor > 0.9999:
            if bs_update == True:
                reset_phermone_values(phermone_matrix)
                prb = None
                bs_update = False
            else:
                bs_update = True

    return pbs
        

if __name__ == "__main__":

    pass