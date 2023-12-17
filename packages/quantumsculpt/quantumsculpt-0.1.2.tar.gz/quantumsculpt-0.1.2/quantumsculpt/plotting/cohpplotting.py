import numpy as np
from ..cohp import CrystalOrbitalHamiltonPopulation
import matplotlib.axes
from .plotdecorators import composed, addgrid, addlimits, addlegend, addtitle, addbins
from matplotlib.ticker import MultipleLocator

@composed(addgrid, addlimits, addlegend, addtitle, addbins)
def plot_averaged_cohp(ax:matplotlib.axes._axes.Axes,
                       cohp:CrystalOrbitalHamiltonPopulation,
                       icohp=False,
                       **kwargs):
    __plot_cohp(ax,
                cohp.get_energies(),
                cohp.get_average_cohp()['cohp'],
                label='cohp')
    
    if icohp:
        __plot_cohp(ax,
                    cohp.get_energies(),
                    cohp.get_average_cohp()['icohp'],
                    linestyle='--',
                    label='icohp')
        
def cohp_generate_sets(atom1, atom2, orbs):
    sets = []
    for o1 in orbs:
        for o2 in orbs:
            sets.append('%s[%s]->%s[%s]' % (atom1, o1, atom2, o2))
            sets.append('%s[%s]->%s[%s]' % (atom2, o1, atom1, o2))
    return sets
      
@composed(addgrid, addlimits, addlegend, addtitle, addbins)  
def plot_gathered_cohp(ax:matplotlib.axes._axes.Axes,
                       cohp:CrystalOrbitalHamiltonPopulation,
                       collections:list[dict],
                       **kwargs):
    
    for item in collections:
        cohps = np.zeros(cohp.get_npts())
        for s in item['set']:
            for cohpdata in cohp.get_dataitems():
                if cohpdata['label'] == s:
                    cohps += cohpdata['icohp'] if item['style'] == 'integrated' else cohpdata['cohp']
        __plot_cohp(ax,
                    cohp.get_energies(),
                    cohps,
                    color=item['color'],
                    style='line' if item['style'] == 'integrated' else item['style'],
                    linestyle='--' if item['style'] == 'integrated' else '-',
                    label=item['legendlabel'])
    

def __plot_cohp(ax:matplotlib.axes._axes.Axes,
                energies:np.ndarray[np.float32],
                cohpvalues:np.ndarray[np.float32],
                color='#000000',
                label=None,
                style=None,
                linestyle=None,
                dosobject=None):
    
    if linestyle is None:
        linestyle = '-'
    
    # append alpha value if not present
    if len(color) == 7:
        color += 'FF'
    if len(color) != 9:
        raise Exception('Invalid color code: %s' % color)
    
    if style is None or style == 'line':
        ax.plot(cohpvalues, energies, color=color, label=label, linestyle=linestyle)
    elif style == 'filled':
        ax.fill_betweenx(energies, 0, cohpvalues, color=color, edgecolor=color[:7],
                         label=label, linestyle=linestyle)
    else:
        raise Exception('Unknown keyword style = %s' % style)
        
    ax.set_xlabel('COHP [-]')
    ax.set_ylabel('Energy $E - E_{f}$ [eV]')
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    ax.yaxis.set_minor_locator(MultipleLocator(1))