import os
import numpy as np
import matplotlib.pyplot as plt
from sim_GLM import *
from fit_GLM import *

d = 20
n1 = np.genfromtxt('binned_spikes_cell_1.txt', delimiter=',')
n2 = np.genfromtxt('binned_spikes_cell_2.txt', delimiter=',')
s1 = np.genfromtxt('binned_stim_cell_1.txt', delimiter=',')
s2 = np.genfromtxt('binned_stim_cell_2.txt', delimiter=',')
f1, h1, b1, se_f1, se_h1, se_b1 = fit_GLM(s1, n1, d)
f2, h2, b2, se_f2, se_h2, se_b2 = fit_GLM(s2, n2, d)
fig = plt.figure(figsize=(7.5, 6))
plt.subplot(4, 1, 1)
plt.errorbar(range(d), f1, yerr=se_f1, linewidth=1)
plt.ylim((-30, 30))
plt.title('Cell 1 Stimulus Filter')
plt.subplot(4, 1, 2)
plt.errorbar(range(d), h1, yerr=se_h1, linewidth=1)
plt.ylim((-10, 5))
plt.title('Cell 1 Self Interaction Filter')
plt.subplot(4, 1, 3)
plt.errorbar(range(d), f2, yerr=se_f2, linewidth=1)
plt.ylim((-25, 25))
plt.title('Cell 2 Stimulus Filter')
plt.subplot(4, 1, 4)
plt.errorbar(range(d), h2, yerr=se_h2, linewidth=1)
plt.ylim((-10, 5))
plt.title('Cell 1 Self Interaction Filter')
plt.tight_layout()
fig.savefig('section_5_fig1.pdf', bbox_inches='tight')

with open('figures5', 'a') as f:
	pass
os.utime('figures5')
