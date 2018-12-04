import math
import numpy as np
import matplotlib.pyplot as plt
from sim_GLM import *
from fit_GLM import *

def do_4_1():
	print("4.1 Simulating a GLM")
	# set up filters and stimulus
	f = [20*math.exp(-t) for t in range(15)]
	h = [-200*math.exp(-t) for t in range(15)]
	b = -15
	mu = 0.3
	sigma = 0.1
	s = np.concatenate([np.zeros(2000), sigma * np.random.randn(18000) + mu])
	# simulate
	y = sim_GLM(s, f, h, b)
	# plot
	plt.subplot(4, 1, 1)
	plt.plot(f, label='True', linewidth=1)
	plt.title('Stimulus Filter')
	plt.subplot(4, 1, 2)
	plt.plot(h, label='True', linewidth=1)
	plt.title('Self Interaction Filter')
	plt.subplot(4, 1, 3)
	plt.plot(s, linewidth=0.25)
	plt.title('Stimulus')
	plt.subplot(4, 1, 4)
	plt.plot(y, linewidth=0.25)
	plt.title('Response')
	plt.tight_layout()
	plt.draw()
	return (s, y)

def do_4_2(s, n):
	print("4.2 Fitting Parameters to a GLM")
	d = 15  # filter length
	f, h, b, se_f, se_h, se_b = fit_GLM(s, n, d)	
	plt.subplot(4, 1, 1)
	plt.errorbar(range(d), f, yerr=se_f, label='Estimate', linewidth=1)
	plt.legend()
	plt.subplot(4, 1, 2)
	plt.errorbar(range(d), h, yerr=se_h, label='Estimate', linewidth=1)
	plt.legend()
	plt.ylim((-3, 3))

s, n = do_4_1()
do_4_2(s, n)
plt.show()
