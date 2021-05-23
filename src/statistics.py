from src.metaheuristic import ACO_metaheuristic
from src.sequenceFactory import get_data_from_file
from src.solution import Solution
import os
import sys
from src import constants
import json

def gather_statistics():

    absolute_benchmark_path = os.path.dirname(os.path.realpath(__file__)) + '/../testFiles/benchmark'

    error_rate = ['5', '10', '20']

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
    scores["description"] = "initial oligo is choosen randomly"
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

            stats = {}
            with open(absolute_benchmark_path + relative_path_sequence + '/' + file_sequence, 'r') as f:
                target_seq = f.read()
                stats["target sequence"] = target_seq



            n, l, S = get_data_from_file(absolute_benchmark_path + relative_path_oligo + '/' + file)

            stats["n"] = n
            stats["l"] = l
            
            solution = ACO_metaheuristic(S, n, l, gather_stats=True, stats=stats)

            stats["oligo used"] = solution.get_path_len()
            stats["output length"] = solution.path_len
            stats["output sequence"] = str(solution)

            scores["files"][e_rate][file] = stats

    print(json.dumps(scores))

if __name__ == "__main__":

    gather_statistics()