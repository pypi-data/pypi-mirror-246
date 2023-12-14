import pandas as pd

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
