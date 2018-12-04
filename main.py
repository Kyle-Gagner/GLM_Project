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
	plt.plot(f)
	plt.title('stimulus filter')
	plt.subplot(4, 1, 2)
	plt.plot(h)
	plt.title('self interaction filter')
	plt.subplot(4, 1, 3)
	plt.plot(s)
	plt.title('stimulus')
	plt.subplot(4, 1, 4)
	plt.plot(y)
	plt.title('response')
	plt.tight_layout()
	plt.show()
	return (s, y)

def do_4_2(s, n):
	fit_GLM(s, n, 15)	

s, n = do_4_1()
do_4_2(s, n)
