import numpy as np
import statsmodels.api as sm

def fit_GLM(s, n, d):
	'''takes stimulus s, spiking response n, filter length d
	returns estimates for stimulus filter, self-interaction filter, offset,
	and standard errors for these estimates 
	'''
	exog = get_exog(s, n, d)
	endog = n[d:]
	model_results = sm.GLM(endog, exog, family=sm.families.Poisson()).fit()
	print(model_results.summary())
	print(model_results.bse)

def get_exog(s, n, d):
	'''takes stimulus s, spiking response n, filter length d
	returns a len(s) - d by 2 * d + 1 matrix where the first d columns have
	the prior d values of the spike signal, the next d columns have the
	prior d values of the stimulus signal, and the last column is full of
	ones for the offset & each row is for a particular time sample of the
	dependent variable
 	'''
	exog = np.ones((len(s) - d, 2 * d + 1))
	for i in range(len(s) - d):
		for j in range(d):
			exog[i][j] = n[d + i - j - 1]  # previous spike signal
			exog[i][j + d] = s[d + i - j - 1]  # previous stimulus
	return exog
