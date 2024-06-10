from src.metaheuristic import ACO_metaheuristic
from src.usefullFunctions import set_global_parameters
from src.sequenceFactory import get_data_from_file, get_data_from_xml
from src.solution import Solution, solutionQuality
from src.constants import MAX_DURATION, NF

import argparse

def set_params(_max_duration=5, _nf=3):
    global MAX_DURATION, NF

    MAX_DURATION = _max_duration
    NF = _nf

parser = argparse.ArgumentParser(description='Builds DNA strand of given set of oligonucleotides using ant colony optimization algorithm.')
parser.add_argument('file', help='file with set of oligonucleotides')
parser.add_argument('--initial', help='if known, index of initial oligonucleotide of given set')

if __name__ == "__main__":



    args = parser.parse_args()

    print(args)
    if args.file is None:
        print('No data file found, please add it with --file option.')
    else:

        n, l, S, range_of_appearance, starting_oligo = get_data_from_xml(args.file)
        #n, l, S = get_data_from_file(args.file)
        
        #init = None
        #if args.initial is not None and int(args.initial) >=0 and int(args.initial) < n - l + 1:
        #    init = int(args.initial)

        solution = ACO_metaheuristic(
            S, n, l, initial_oligo=starting_oligo
        )

        print(solution)
