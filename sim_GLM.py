import math
import numpy as np

def sim_GLM(s, f, h, b):
	''' takes stimulus s, stimulus filter f, self interaction filter h, offset b
	returns simulated results of GLM
	'''
	# filtered stimulus
	x = np.convolve(s, np.concatenate([[0], f]))[0:len(s)]
	# spike history: to make indexing easier, history is padded to negative time
	# t in the range -len(h) to len(s)-1 inclusive
	n = np.zeros(len(h) + len(s))
	for i in range(len(h), len(h)+len(s)):
		l = x[i - len(h)] + b
		for j in range(len(h)):
			l += n[i - j - 1] * h[j]
		# ensure no more than one spike per bin
		n[i] = min(np.random.poisson(math.exp(l)), 1)
	# return the spike history sans zero padding
	return n[len(h):]
