from src.metaheuristic import ACO_metaheuristic
from src.sequenceFactory import get_data_from_file
from src.solution import Solution, solutionQuality
from src.heuristics import greedyHeuristic, greedyLagHeuristic
from src.usefullFunctions import max_common_part, set_global_parameters, get_file_list
import os
import sys
from src import constants
import json
import time
import numpy as np

def gather_statistics(limit=None, init=False, random_files=False):

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
    scores["description"] = "greedy heuristic tested"
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
            
            if cnt == limit:
                break

            stats = {}
            with open(absolute_benchmark_path + relative_path_sequence + '/' + file_sequence, 'r') as f:
                target_seq = f.read()
                stats["target sequence"] = target_seq



            n, l, S = get_data_from_file(absolute_benchmark_path + relative_path_oligo + '/' + file)

            stats["n"] = n
            stats["l"] = l

            com_matrix = np.zeros((len(S), len(S)), dtype=int)

            timer_start = time.time()
            if init == False:
                solution = ACO_metaheuristic(S, n, l, gather_stats=True, stats=stats)
            else:
                

                for i in range(com_matrix.shape[0]):
                    for j in range(com_matrix.shape[1]):
                        com_matrix[i][j] = max_common_part(S[i], S[j])
                # solution = greedyLagHeuristic(S, None, n, l, commons_matrix=com_matrix)

                solution = greedyHeuristic(
                    S, n=n, l=l, choose_init_alg='worst_best'
                )

            stats["time"] = time.time() - timer_start

            stats["oligo used"] = solution.get_path_len()
            stats["output length"] = solution.path_len
            stats["output sequence"] = str(solution)
            stats["quality"] = solutionQuality(solution, target_seq, n, l)
            stats["quality-needleman"] = solutionQuality(solution, target_seq, n, l, name='needleman-wunsch')

            scores["files"][e_rate][file] = stats
            cnt += 1 

    print(json.dumps(scores))

def meta_tuning(file_list, output_file=None,
        det_rate_list=[constants.det_rate], init_det_rate_list=[constants.init_det_rate], 
        _rcl_list=[constants.rcl_card], duration_list=[constants.MAX_DURATION], _nf_list=[constants.NF],
        _nb_list=[constants.NB], _init_crd_list=[constants.init_crd]
    ):

    output_results = {}

    it = 0

    number_of_iter = len(_init_crd_list) *len(det_rate_list) * len(init_det_rate_list) * len(_rcl_list) * len(duration_list) * len(_nf_list) * len(_nb_list)
    max_time_of_iter = len(file_list) * max(duration_list)
    max_total_time = number_of_iter * max_time_of_iter
    print('Begin computation, number of iterations: ',number_of_iter)
    print('Maximum time expected: ', max_total_time / 60, 'min.')

    output_results["init det. rate list"] = init_det_rate_list
    output_results["det. rate list"] = det_rate_list
    output_results["nb list"] = _nb_list
    output_results["nf list"] = _nf_list
    output_results["init rcl card"] = _init_crd_list
    output_results["rcl card"] = _rcl_list
    output_results["iterations"] = {}

    for __det_rate in det_rate_list:
        for __init_det_rate in init_det_rate_list:
            for __rcl_card in _rcl_list:
                for __duration in duration_list:
                    for __nf in _nf_list:
                        for __nb in _nb_list:
                            for __init_card in _init_crd_list:
                            
                                print('Iteration no.', it)

                                global_quality = 0

                                set_global_parameters(
                                    _max_duration=__duration,
                                    _crd_list=__rcl_card,
                                    _nf=__nf,
                                    _nb=__nb,
                                    _det_rate=__det_rate,
                                    _init_det_rate=__init_det_rate,
                                    _init_crd=__init_card
                                )
                                scores = {}

                                scores["nf"] = __nf
                                scores["nb"] = __nb
                                scores["rcl_card"] = __rcl_card
                                scores["rho"] = constants.rho
                                scores["kib"] = constants.kib
                                scores["krb"] = constants.krb
                                scores["kbs"] = constants.kbs
                                scores["max duration"] = __duration
                                scores["conv threshold"] = constants.CONV_THRESHOLD   
                                scores["determinism rate"] = __det_rate
                                scores["init det. rate"] = __init_det_rate
                                scores["init det. card"] = __init_card

                                for data_file, seq_file in file_list:
                                    with open(seq_file, 'r') as f:
                                        target_seq = f.read()

                                    n, l, S = get_data_from_file(data_file)

                                    solution = ACO_metaheuristic(S, n, l)

                                    global_quality += solutionQuality(solution, target_seq, n, l, name='needleman-wunsch')

                                scores['quality'] = global_quality / len(file_list)

                                
                                output_results["iterations"][it] = scores
                                it += 1
    
    if output_file is None:
        print(output_results)

    else:
        with open(output_file, 'w') as f:
            f.write(json.dumps(output_results))

if __name__ == "__main__":
    
    work_path = os.path.dirname(os.path.realpath(__file__))
    dna_files_paths = [work_path + '/../testFiles/benchmark/error_rate_20/stand20/20',
        work_path + '/../testFiles/benchmark/error_rate_10/stand10/10',
        work_path + '/../testFiles/benchmark/error_rate_5/stand5/5'
    ]
    seq_files_paths = [work_path + '/../testFiles/benchmark/error_rate_20/sequence',
        work_path + '/../testFiles/benchmark/error_rate_10/sequence',
        work_path + '/../testFiles/benchmark/error_rate_5/sequence'
    ]

    
    # gather_statistics(limit=None, init=True)

    file_list = get_file_list(dna_files_paths, seq_files_paths, limit=60, shuff=True)
    print(file_list)

    meta_tuning(
        file_list, duration_list=[5], det_rate_list=[0.25, 0.6, 0.8, 0.95], _rcl_list=[3, 5, 10, 20], output_file='_det_corr.txt'
    )