import sys
import os
import matplotlib.pyplot as plt
import numpy as np

# add a reference to load the module
ROOT = os.path.dirname(__file__)
sys.path.append(os.path.join(ROOT, '..'))

from cloudwatcher import DensityOfStates
import cloudwatcher as cw

###
# create a clean DOS for the CO molecule
###############################################################################
filename = os.path.join(ROOT, '..', 'samples', 'hco_gasphase', 'DOSCAR.lobster')
dos = DensityOfStates(filename)

fig, ax = plt.subplots(1,3, dpi=144, figsize=(12,4))
cw.plot_total_dos(ax[0], 
                  dos, 
                  grid=True,
                  addspins=True,
                  ylim=(-25,5),
                  title='Total DOS')

# specify which collections of projections to plot, by default this is done over
# all the atoms
collection = [
    {'set': ['2s', '2p_x'], 'legendlabel' : '$\sigma$', 'color': '#FF0000AA', 'style': 'filled'},
    {'set': ['2p_y', '2p_z'], 'legendlabel' : '$\pi$', 'color': '#0000FFAA', 'style': 'filled'},
    {'set': ['2s', '2p_x'], 'legendlabel' : '$int - \sigma$', 'color': '#FF0000AA', 'style': 'integrated'},
    {'set': ['2p_y', '2p_z'], 'legendlabel' : '$int - \pi$', 'color': '#0000FFAA', 'style': 'integrated'}
]

# specify where to place the bins for orbital deconvolution
bins = [
    (-23,-21),
    (-6,-5),
    (-3.8,-2.1),
    (-1,1),
]

cw.plot_gathered_dos(ax[1], 
                     dos,
                     collection, 
                     grid=True, 
                     ylim=(-25,5), 
                     legend=True,
                     title='lm-decomposed DOS',
                     bins=bins)

print(cw.integrate_dos_bins(dos, bins))

fig.suptitle('CO (spin-restricted)')

# try to automatically find peaks
res = cw.find_peaks(dos.get_energies(), dos.get_total_dos()['states'])
ax[0].scatter(res[0], res[1], marker='x', color='black')
res = cw.fit_gaussians(dos.get_energies(), dos.get_total_dos()['states'], res[1])
print(res['gaussians'])

ax[0].plot(res['curve'], dos.get_energies())

plt.tight_layout()