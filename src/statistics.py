from src.metaheuristic import ACO_metaheuristic
from src.sequenceFactory import get_data_from_file
from src.solution import Solution, solutionQuality
from src.heuristics import greedyHeuristic, greedyLagHeuristic
from src.usefullFunctions import max_common_part
import os
import sys
from src import constants
import json
import time
import numpy as np

def gather_statistics(limit=None, init=False):

    absolute_benchmark_path = os.path.dirname(os.path.realpath(__file__)) + '/../testFiles/benchmark'

    error_rate = ['5', '10', '20']
    cnt = 0

    scores = {}

    scores["nf"] = constants.NF
    scores["nb"] = constants.NB
    scores["rcl_card"] = constants.rcl_card
    scores["rho"] = constants.rho
    scores["kib"] = constants.kib
    scores["krb"] = constants.krb
    scores["kbs"] = constants.kbs
    scores["max duration"] = constants.MAX_DURATION
    scores["conv threshold"] = constants.CONV_THRESHOLD
    scores["description"] = "ant colony applied, initial oligo is random, only instances with length 200"
    scores["files"] = {}

    #for each error rate instances
    for e_rate in error_rate:

        relative_path_oligo = '/error_rate_{}/stand{}/{}'.format(e_rate, e_rate, e_rate)
        relative_path_sequence = '/error_rate_{}/sequence'.format(e_rate)
        data_files = os.listdir(absolute_benchmark_path + relative_path_oligo)
        target_sequences = os.listdir(absolute_benchmark_path + relative_path_sequence)
        
        data_files.sort()
        target_sequences.sort()

        scores["files"][e_rate] = {}

        for file, file_sequence in zip(data_files, target_sequences):
            
            if file[:3] != "200":
                continue
            if cnt == limit:
                break

            stats = {}
            with open(absolute_benchmark_path + relative_path_sequence + '/' + file_sequence, 'r') as f:
                target_seq = f.read()
                stats["target sequence"] = target_seq



            n, l, S = get_data_from_file(absolute_benchmark_path + relative_path_oligo + '/' + file)

            stats["n"] = n
            stats["l"] = l
            
            timer_start = time.time()
            if init == False:
                solution = ACO_metaheuristic(S, n, l, gather_stats=True, stats=stats)
            else:
                com_matrix = np.zeros((len(S), len(S)), dtype=int)

                for i in range(com_matrix.shape[0]):
                    for j in range(com_matrix.shape[1]):
                        com_matrix[i][j] = max_common_part(S[i], S[j])
                solution = greedyLagHeuristic(S, None, n, l, commons_matrix=com_matrix)

            stats["time"] = time.time() - timer_start

            stats["oligo used"] = solution.get_path_len()
            stats["output length"] = solution.path_len
            stats["output sequence"] = str(solution)
            stats["quality"] = solutionQuality(solution, target_seq, n, l)
            stats["quality-needleman"] = solutionQuality(solution, target_seq, n, l, name='needleman-wunsch')

            scores["files"][e_rate][file] = stats
            cnt += 1         
            # print(stats)   

    print(json.dumps(scores))

if __name__ == "__main__":

    gather_statistics(limit=None, init=False)