from src.metaheuristic import ACO_metaheuristic
from src.sequenceFactory import get_data_from_file
from src.solution import Solution
import os
import sys

def gather_statistics():

    absolute_benchmark_path = os.path.dirname(os.path.realpath(__file__)) + '/../testFiles/benchmark'

    error_rate = ['5', '10', '20']

    #for each error rate instances
    for e_rate in error_rate:
        
        print('error rate: ', e_rate)
        print('\n')

        relative_path_oligo = '/error_rate_{}/stand{}/{}'.format(e_rate, e_rate, e_rate)
        relative_path_sequence = '/error_rate_{}/sequence'.format(e_rate)
        data_files = os.listdir(absolute_benchmark_path + relative_path_oligo)
        target_sequences = os.listdir(absolute_benchmark_path + relative_path_sequence)

        for file in data_files:
            
            print(file)

            n, l, S = get_data_from_file(absolute_benchmark_path + relative_path_oligo + '/' + file)

            print(n)
            
            solution = ACO_metaheuristic(S, n, l)

            print('found length: {}'.format(solution.path_len))


if __name__ == "__main__":

    gather_statistics()