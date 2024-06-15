import numpy as np

acid_map = {1: "A", 2: "C", 3: "G", 0: "T"}
acid_rev_map = {"A": 1, "C": 2, "G": 3, "T": 0}
dummy_oligo = -1                 # initial fake oligo
MAX_OLIGO_LEN = 100

# metaheuristic
rcl_card = 3 # restricted candidate list cardinality
det_rate = 0.95 # determinism rate
init_det_rate = 0.25
init_crd = 20
rho = 0.01    # learning rate
kib = 0.3
krb = 0.3
kbs = 0.4

def set_init_det_rate(val):
    global init_det_rate
    init_det_rate = val

MAX_DURATION = 1

NF = 3
NB = 0

CONV_THRESHOLD = 0.9999

