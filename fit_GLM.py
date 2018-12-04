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
	h = model_results.params[:d]
	f = model_results.params[d:-1]
	b = model_results.params[-1]
	se_h = model_results.bse[:d]
	se_f = model_results.bse[d:-1]
	se_b = model_results.bse[-1]
	return (f, h, b, se_f, se_h, se_b)

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
