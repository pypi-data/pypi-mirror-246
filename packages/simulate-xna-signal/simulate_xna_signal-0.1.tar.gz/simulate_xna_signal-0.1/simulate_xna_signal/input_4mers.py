import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def input_xna_sequence():
#User input
    user_input = input('Enter XNA Sequence: ')
    user_input = user_input.upper()
    input_length = int(len(user_input))

#remove bases from input sequence that can't be plotted as current 
    sim_seq = user_input.replace(user_input[0], "", 1)
    sim_seq = user_input.replace(user_input[-1:-len(sim_seq)], "", 1)
    print(f"Given the input of {user_input}, the expected nanopore signal for {sim_seq} base input is simulated below. This sequence has {len(sim_seq)} bases.")

#split input into a list of KXmers
#objective: find signal where each nucleotide is in the 0th position of the 4mer. this means, generating a list of 4mers where the reading frame
#difference between them is only 1 base. To generate this list of strings, use a 4-loop to specify the reading frame. This skips first base in input

    KXmers = [] # initialize y array
    KXmer1= user_input[0:4]
    KXmers.append(KXmer1)

    for i in range(len(user_input)): #for each base in input:
        KXmer_i= user_input[i+1:i+5]
        if len(KXmer_i)== 4:
            KXmers.append(KXmer_i)
#as artifact of step function plot, repeat the last KXmer to be plotted:
    KXmers.append(KXmers[-1])
    return KXmers
#due to finding average signal from 0th position of KXMer, not every base in the input sequence can be simulated
