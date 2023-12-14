import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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