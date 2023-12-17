import sys
import os
import matplotlib.pyplot as plt

# add a reference to load the module
ROOT = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(ROOT, '..'))

from quantumsculpt import DensityOfStates, CrystalOrbitalHamiltonPopulation
import quantumsculpt as qs

###
# create a clean DOS for the CO molecule
###############################################################################
filename = os.path.join(ROOT, '..', 'samples', 'carbonmonoxide_gasphase', 'pbe', 'DOSCAR.lobster')
dos = DensityOfStates(filename)

fig, ax = plt.subplots(1,5, dpi=144, figsize=(14,4))
qs.plot_total_dos(ax[0], 
                  dos, 
                  grid=True, 
                  ylim=(-25,5),
                  title='Total DOS CO(g)')

# specify which collections of projections to plot
collection = [
    {'set': ['all-2s', 'all-2p_x'], 'legendlabel' : '$\sigma$', 'color': '#FF0000AA', 'style': 'filled'},
    {'set': ['all-2p_y', 'all-2p_z'], 'legendlabel' : '$\pi$', 'color': '#0000FFAA', 'style': 'filled'},
    {'set': ['all-2s', 'all-2p_x'], 'legendlabel' : '$int - \sigma$', 'color': '#FF0000AA', 'style': 'integrated'},
    {'set': ['all-2p_y', 'all-2p_z'], 'legendlabel' : '$int - \pi$', 'color': '#0000FFAA', 'style': 'integrated'}
]

# specify where to place the bins for orbital deconvolution
bins = [
    (-23,-21),
    (-6,-5),
    (-3.8,-2.1),
    (-1,1),
    (-35,.5),
]

qs.plot_gathered_dos(ax[1], 
                     dos,
                     collection, 
                     grid=True, 
                     ylim=(-25,5), 
                     legend=True,
                     title='lm-DOS CO(g)',
                     bins=bins)

# gather the total number of states for the bins
print('Bins for gasesous CO')
for b in qs.integrate_dos_bins(dos, bins):
    print(b)

###
# create a clean DOS and COHP for adsorbed CO
###############################################################################

filename = os.path.join('D:/', 'Data', 'Xianxuan', 'COADS', '010', 'DOSCAR.lobster')
dos = DensityOfStates(filename)

atomdos = dos.get_dos_atom(57)

# specify where to place the bins for orbital deconvolution
bins = [
    (-22.8,-21.5),
    (-10,-9.4),
    (-7,-5),
    (-5,0),
    (-35,0.0),
]

sigmaset = qs.dos_generate_sets([57,58], ['2s','2p_x'])
piset = qs.dos_generate_sets([57,58], ['2p_y','2p_z'])

# specify which collections of projections to plot
collection = [
    {'set': sigmaset, 
     'legendlabel' : '$\sigma$', 
     'color': '#FF0000AA', 
     'style': 'filled', 
     'stack': True},
    {'set': piset, 
     'legendlabel' : '$\pi$', 
     'color': '#0000FFAA', 
     'style': 'filled', 
     'stack': True},
    {'set': sigmaset, 
     'legendlabel' : '$int - \sigma$', 
     'color': '#FF0000AA', 
     'style': 'integrated'},
    {'set': piset, 
     'legendlabel' : '$int - \pi$', 
     'color': '#0000FFAA', 
     'style': 'integrated'}
]

qs.plot_gathered_dos(ax[2], 
                     dos, 
                     collection,
                     grid=True,
                     ylim=(-25,5),
                     legend=True,
                     addspins=True,
                     bins=bins,
                     title='lm-DOS COads')

# gather the total number of states for the bins
print('Bins for adsorbed CO: sigma')
for b in qs.integrate_dos_bins(dos, bins, ao=sigmaset):
    print(b)

print('Bins for adsorbed CO: pi')
for b in qs.integrate_dos_bins(dos, bins, ao=piset):
    print(b)
    
print('Bins for adsorbed CO: all')
for b in qs.integrate_dos_bins(dos, bins, ao=['57-all', '58-all']):
    print(b)

filename = os.path.join('D:/', 'Data', 'Xianxuan', 'COADS', '010', 'COHPCAR.lobster')
cohp = CrystalOrbitalHamiltonPopulation(filename)

qs.plot_averaged_cohp(ax[3], 
                      cohp, 
                      grid=True,
                      bins=bins,
                      ylim=(-25,5),
                      icohp=True,
                      title='Total COHP COads',
                      legend=True)

sigmaset = qs.cohp_generate_sets('O58', 'C57', ['2s','2p_x'])
piset = qs.cohp_generate_sets('O58', 'C57', ['2p_y','2p_z'])

# specify which collections of projections to plot
collection = [
    {'set': sigmaset, 
     'legendlabel' : '$\sigma$', 
     'color': '#FF0000AA', 
     'style': 'filled'},
    {'set': piset, 
     'legendlabel' : '$\pi$', 
     'color': '#0000FFAA', 
     'style': 'filled'},
    {'set': sigmaset, 
     'legendlabel' : '$int - \sigma$', 
     'color': '#FF0000AA', 
     'style': 'integrated'},
    {'set': piset, 
     'legendlabel' : '$int - \pi$', 
     'color': '#0000FFAA', 
     'style': 'integrated'}
]

qs.plot_gathered_cohp(ax[4],
                      cohp,
                      collections=collection,
                      grid=True,
                      bins=bins,
                      title='Decomposed COHP',
                      ylim=(-25,5),
                      legend=True)

plt.tight_layout()