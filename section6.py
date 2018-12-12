import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
from scipy.stats import gamma, kstest 

with open('ISIsimulated.txt', 'r') as spikes:
	spike_times = [float(spike_time) for spike_time in spikes.readlines()]

spike_ints = np.diff(spike_times)

# Estimate mean and variance of ISI and correlation between successive ISI 
mu = spike_ints.mean()
sigma_2 = spike_ints.var()
corr = np.corrcoef(spike_ints[:-1], spike_ints[1:])[1, 0]

# Plot histogram
plt.figure(figsize=(15, 12))
host = host_subplot(111, axes_class=AA.Axes)
hist_plt = plt.hist(spike_ints, bins=20, label='Histogram')
host.set_title('ISI Histogram and Estimated PDF')
host.set_xlabel('Inter-Spike Interval')
host.set_ylabel('Number of Occurrences')

# Generate gamma model for ISI and measure goodness of fit
a, _, _ = gamma.fit(spike_ints, floc=0, fscale=1)
model = gamma(a)
_, gof = kstest(spike_ints, model.cdf)

# Plot model pdf on separate y-axis
par = host.twinx()
x = np.arange(np.min(spike_ints), np.max(spike_ints), 0.1)
model_plt = par.plot(x, model.pdf(x), label='PDF')
host.legend()
par.set_ylabel('Probability Density')
par.axis['right'].toggle(all=True)
plt.tight_layout()
plt.subplots_adjust(bottom=0.1, right=0.9)
plt.figtext(
	x=0,
	y=0,
	s='\n'.join([
		'Mean: {:.3}',
		'Variance: {:.3}',
		'Correlation Between Successive ISI: {:.3}',
		'Goodness of Fit: {:.3}'
	]).format(
		mu, sigma_2, corr, gof
	)
)

plt.savefig('section_6_fig1.pdf', bbox_inches='tight')

# Analyze ISI of neuron 2
n2_spikes = np.genfromtxt('binned_spikes_cell_2.txt', delimiter=',')
n2_isi = []
count = 0
for spikes in n2_spikes:
	if spikes == 0:
		count += 1
	elif count < 100:
		n2_isi.append(count)
		count = 0
	else:
		count = 0  # Don't include unusually large ISI

# Plot histogram of neuron 2's ISI
plt.figure(figsize=(15, 12))
plt.hist(n2_isi, bins=100)
plt.title('Second Neuron ISI Histogram')
plt.xlabel('Inter-Spike Interval')
plt.ylabel('Number of Occurrences')
plt.savefig('section_6_fig2.pdf', bbox_inches='tight')

open('figures6', 'w').close()  # For makefile
