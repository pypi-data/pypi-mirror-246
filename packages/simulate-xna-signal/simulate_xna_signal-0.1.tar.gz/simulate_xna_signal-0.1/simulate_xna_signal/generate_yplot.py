import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def yplot(KXmer_signal,KXmers):
#generate y data for step function
    y = [] # initialize y array
# signal for each base is dependent on the KMER it is part of. For each base, the signal is equal to the average signal of the KMER for which the base
# is in the 0th position (-1,0,1,2), meaning the second of a group of 4 bases. 
    for i in range(len(KXmers)): #for each KXmer in input:
        if bool(KXmer_signal['KXmer'].str.contains(KXmers[i]).any())==True: #if input KXmer matches one in the database:
                index= KXmer_signal[KXmer_signal['KXmer']==KXmers[i]].index.values #determine index of KXmer in database
                signal_i= KXmer_signal.iloc[index]['Mean level']  #find mean current level corresponding to KXmer with same row index in database
                y.append(signal_i.values[0])
        elif bool(KXmer_signal['KXmer'].str.contains('AAAC').any())==False:
            print("KMER not found in database")
            break

    return y
