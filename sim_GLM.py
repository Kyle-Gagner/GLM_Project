import math
import numpy as np
import statsmodels.api as sm

def sim_GLM(s, f, h, b):
	''' takes stimulus s, stimulus filter f, self interaction filter h, offset b
	returns simulated results of GLM
	'''
	# the formula in section 3 suggests only past values in the stimulus are used
	# this makes sense in the case of the self interaction filter, but not stimulus filter
	# I suggest we ask in class whether the stimulus filter extends from t=0 or t=1
	# assuming starts at t=1 for consistency with formula
	
	# filtered stimulus (padded according to formula discussed above)
	x = np.convolve(s, np.concatenate([[0], f]))[0:len(s)]
	# spike history: to make indexing easier, history is padded to negative time
	# t in the range -len(h) to len(s)-1 inclusive
	y = np.zeros(len(h) + len(s))
	for i in range(len(h), len(h)+len(s)):
		l = x[i - len(h)] + b
		for j in range(len(h)):
			l += y[i - j - 1] * h[j]
		if l > 25:
			l = 25
		# ensure no more than one spike per bin
		y[i] = min(np.random.poisson(math.exp(l)), 1)
	# return the spike history sans zero padding
	return y[len(h):]
