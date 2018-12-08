import math
import numpy as np
import matplotlib.pyplot as plt
from sim_GLM import *
from fit_GLM import *

def fitter_trial(s, n, f, h, b):
	'''takes stimulus s, spiking history n, stimulus filter f, self interaction filter h, offset b
	fits GLM to s and n, returning absolute error in b, RMSE of f and h, and MSE of f and h
	only coefficients with <=10 standard error are used in the error calculation for h'''
	if len(f) != len(h):
		raise ValueError("Expected len(f) == len(h)")
	fit_f, fit_h, fit_b, fit_se_f, fit_se_h, fit_se_b = fit_GLM(s, n, len(f))
	error_f = np.subtract(fit_f, f)
	error_h = np.subtract(fit_h, h)
	# fudge factor, do not accumulate very large errors
	for i in range(len(h)):
		if fit_se_h[i] > 10:
			fit_se_h[i] = 0
			error_h[i] = 0
	return abs(fit_b - b), rms(error_f), rms(error_h), np.mean(fit_se_f), np.mean(fit_se_h)

def rms(x):
	return np.sqrt(np.mean(np.square(x)))

# section 4.1
print("4.1 Simulating a GLM")
# set up filters and stimulus
d = 15
f = [20*math.exp(-t) for t in range(d)]
h = [-200*math.exp(-t) for t in range(d)]
b = -15
mu = 0.3
sigma = 0.1
s = np.concatenate([np.zeros(2000), sigma * np.random.randn(18000) + mu])
# simulate
n = sim_GLM(s, f, h, b)
# plot
fig1 = plt.figure(figsize=(15, 12))
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
plt.plot(n, linewidth=0.25)
plt.title('Response')
plt.tight_layout()

# section 4.2
print("4.2 Fitting Parameters to a GLM")
# run the fitter
fit_f, fit_h, fit_b, fit_se_f, fit_se_h, fit_se_b = fit_GLM(s, n, d)
# add to the existing plots
plt.subplot(4, 1, 1)
plt.errorbar(range(d), fit_f, yerr=fit_se_f, label='Estimate', linewidth=1)
plt.legend()
plt.ylim((-1, 20))
plt.subplot(4, 1, 2)
plt.errorbar(range(d), fit_h, yerr=fit_se_h, label='Estimate', linewidth=1)
plt.legend()
plt.ylim((-5, 1))
fig1.savefig('section_4_fig1.pdf', bbox_inches='tight')

# section 4.3
print("4.3 GLM Performance")
# these lists will contain the data points for each row of plots
data_by_length = []
data_by_spikes = []
data_by_offset = []
# they contain tuples, the following variables alias the indices in these tuples for convenience
x_value = 0
abs_b = 1
rmse_f = 2
rmse_h = 3
mse_f = 4
mse_h = 5
# compute data for the first two rows of plots
for l in np.repeat([int(x) for x in [1e3, 3e3, 1e4, 3e4]], 6):
	s = sigma * np.random.randn(l) + mu
	n = sim_GLM(s, f, h, b)
	data = fitter_trial(s, n, f, h, b)
	data_by_length.append((l, *data))
	data_by_spikes.append((sum(n), *data))
# compute data for the last row of plots
for b in np.repeat([-14, -16, -18], 6):
	s = sigma * np.random.randn(l) + mu
	n = sim_GLM(s, f, h, b)
	data_by_offset.append((sum(n), *fitter_trial(s, n, f, h, b)))
# describe the rows of plots (dataset, x label)
plotrows = [
	(data_by_length, 'Number of Samples'),
	(data_by_spikes, 'Spike Counts'),
	(data_by_offset, 'Spike Counts')]
# describe the columns of plots ([(index 1, color 1, label 1), (index 2, color 2, label 2)], y label)
plotcols = [([(abs_b, 'blue', 'offset')], 'Offset Error'),
	([(rmse_f, 'blue', 'stimulus filters'), (rmse_h, 'red', 'response filters')], 'RMSE'),
	([(mse_f, 'blue', 'stimulus filters'), (mse_h, 'red', 'response filters')], 'MSE')]
fig2=plt.figure(figsize=(15, 20))
for row in range(3):
	dataset, x_label = plotrows[row]
	for col in range(3):
		plt.subplot(3, 3, row * 3 + col + 1)
		serieslist, y_label = plotcols[col]
		for series in serieslist:
			index, color, label = series
			plt.scatter([x[0] for x in dataset], [x[index] for x in dataset], c=color, label=label)
		plt.xscale('log')
		plt.xlabel(x_label)
		plt.ylabel(y_label)
		if len(serieslist) > 1:
			plt.legend()
plt.subplot(3, 3, 2)
plt.title('Varying Samples')
plt.subplot(3, 3, 5)
plt.title('Varying Samples')
plt.subplot(3, 3, 8)
plt.title('Varying Offset')
plt.tight_layout()
fig2.savefig('section_4_fig2.pdf', bbox_inches='tight')

open('figures4', 'w').close()  # For makefile
