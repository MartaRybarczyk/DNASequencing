import numpy as np

acid_map = {1: "A", 2: "C", 3: "G", 0: "T"}
acid_rev_map = {"A": 1, "C": 2, "G": 3, "T": 0}
dummy_oligo = -1                 # initial fake oligo

# metaheuristic
rcl_card = 3 # restricted candidate list cardinality
det_rate = 0.5 # determinism rate
rho = 0.01    # learning rate
kib = 0.3
krb = 0.3
kbs = 0.3

MAX_DURATION = 20

NF = 10
NB = 0

CONV_THRESHOLD = 0.9999