
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Import all relevant data from folder to be read by Python
def load():
    data_ATGC = pd.read_csv("ATGC_libv2_FLG001.csv")
    data_J = pd.read_csv("J_libv2_FLG001.csv")
    data_K = pd.read_csv("K_libv2_FLG001.csv")
    data_P = pd.read_csv("P_libv2_FLG001.csv")
    data_Sc = pd.read_csv("Sc_libv2_FLG001.csv")
    data_V = pd.read_csv("V_libv2_FLG001.csv")
    data_X = pd.read_csv("X_libv2_FLG001.csv")
    data_Z = pd.read_csv("Z_libv2_FLG001.csv")

#Extract only KXmer and mean current level from all data
    KXmer_signal_ATGC = data_ATGC[['KXmer', 'Mean level']].copy()
    KXmer_signal_J = data_J[['KXmer', 'Mean level']].copy()
    KXmer_signal_K = data_K[['KXmer', 'Mean level']].copy()
    KXmer_signal_P = data_P[['KXmer', 'Mean level']].copy()
    KXmer_signal_Sc = data_Sc[['KXmer', 'Mean level']].copy()
    KXmer_signal_V = data_V[['KXmer', 'Mean level']].copy()
    KXmer_signal_X = data_X[['KXmer', 'Mean level']].copy()
    KXmer_signal_Z = data_Z[['KXmer', 'Mean level']].copy()
#Merge all paired KXmer and mean level data to one dataframe using pandas concatenate function

    frames = [KXmer_signal_ATGC, KXmer_signal_J, KXmer_signal_K, KXmer_signal_P, KXmer_signal_Sc, KXmer_signal_V, KXmer_signal_X, KXmer_signal_Z]

    KXmer_signal = pd.concat(frames)

    return KXmer_signal
#KXmer_signal is the database of all paired 4mers and their associated signal


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


def xplot(KXmers):

    x_length = len(KXmers)
    len_seq= 4*(len(KXmers)-1)


#generate x axis of step function from input length
    x= list(range(int(1), int(x_length)+1))
    return x


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


def plot(x,y):

#plot step function
    plt.figure(figsize=(10, 5))
#generating data labels above steps

#for i in range(len(sim_seq)):
 #   plt.text(i, , sim_seq[i], fontsize = 22) 
    plt.step(x, y, '-', where='post') 

    plt.title(f"Simulated Nanopore Signal for input genetic sequence")
    plt.xlabel("Base Position")
    plt.ylabel("Normalized Current")

# add shading for noise error 
#add synthetic noise to data and generate arrays for shading
    noise= np.random.normal(0,0.4, len(y))
    y1  = y - noise
    y2  = y + noise
    plt.fill_between(x, y1,y2, alpha=0.2, step='post')

#Set default plot size
#plt.figure().set_figwidth(30)
    plt.show()


def run(): 

    KXmer_signal = load()

    KXmers = input_xna_sequence()

    x = xplot(KXmers)

    y = yplot(KXmer_signal,KXmers)

    plot(x,y)



