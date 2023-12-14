import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def xplot(KXmers):

    x_length = len(KXmers)
    len_seq= 4*(len(KXmers)-1)


#generate x axis of step function from input length
    x= list(range(int(1), int(x_length)+1))
    return x
