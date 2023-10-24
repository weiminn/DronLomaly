import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import collections

line_colors = ['#008000', '#e803fc', '#03b1fc']
line_labels = ['Roll', 'Pitch', 'Yaw']

# function to update the data
def visualize(i, xyz, ax):
    # clear axis
    ax.cla()
    # ax1.cla() # plot cpu
    ax.axhline(y=1, linewidth=1, color='r')
    for idx, col in enumerate(xyz):
        ax.plot(col, color=line_colors[idx], label=line_labels[idx])
    plt.tight_layout()
    plt.legend()

    # ax.text(len(cpu)-1, cpu[-1]+2, "{}%".format(cpu[-1]))
    # ax.text(len(ram)-1, ram[-1]+2, "{}%".format(ram[-1]))
    # ax.set_ylim(0, max(thres) + (max(thres)*.1)) 
    ax.set_ylim(0, 2) 
    ax.set_xlim(0, 60) 

def animate(xyz):

    # define and adjust figure
    fig = plt.figure( facecolor='#DEDEDE')
    ax = plt.subplot()
    ax.set_facecolor('#DEDEDE')

    # animates
    ani = FuncAnimation(fig, visualize, fargs=(xyz, ax), interval=400)
    plt.show()

# animate()