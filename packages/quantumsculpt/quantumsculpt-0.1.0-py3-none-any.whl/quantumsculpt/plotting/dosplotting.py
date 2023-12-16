import numpy as np
from ..dos import DensityOfStates
import matplotlib.axes
from .plotdecorators import composed, addgrid, addlimits, addlegend, addtitle, addbins
from matplotlib.ticker import MultipleLocator

@composed(addgrid, addlimits, addlegend, addtitle, addbins)
def plot_total_dos(ax:matplotlib.axes._axes.Axes,
                   dos:DensityOfStates,
                   addspins:bool=False,
                   **kwargs):
    """Plot the total density of states

    Parameters
    ----------
    ax : matplotlib.axes._axes.Axes
        matplotlib axis object
    dos : DensityOfStates
        density of states object

    Raises
    ------
    Exception
        Raises an exception upon unknown spin configuration
    """
    
    if dos.get_spin_state() == 'restricted' or addspins == True:
        __plot_dos(ax,
                   dos.get_total_dos()['energies'],
                   dos.get_total_dos()['states'])
    elif dos.get_spin_state() == 'unrestricted':
        __plot_dos(ax,
                   dos.get_total_dos()['energies'],
                   dos.get_total_dos()['states_up'])
        __plot_dos(ax,
                   dos.get_total_dos()['energies'],
                   -dos.get_total_dos()['states_down'])
    else:
        raise Exception('Unknown spin configuration: %s' % dos.get_spin_state())

@composed(addgrid, addlimits, addlegend, addtitle, addbins)
def plot_gathered_dos(ax:matplotlib.axes._axes.Axes,
                      dos:DensityOfStates,
                      collections:list[dict],
                      addspins=False,
                      **kwargs):
    """Create a plot for specific orbital projections

    Parameters
    ----------
    ax : matplotlib.axes._axes.Axes
        matplotlib axis object
    dos : DensityOfStates
        density of states object
    collections : list[dict]
        list of projections to gather (see below)
    addspins : bool, optional
        whether to combine spin-up and spin-down, by default False

    Raises
    ------
    Exception
        Raises exception upon unknown spin configuration
        
    Notes
    -----
    :code:`collections` are a list of dictionaries composed of the following
    keys: `code:`set`, :code:`legendlabel`, :code:`color`, and :code:`style`.
    The :code:`set` item should contain a list of atom-orbital pairs, e.g. :code:`all-2s`,
    :code:`1-2p_x`, :code:`4-3d_z2` and so on. The keyword :code:`all` implies that
    the particular atomic orbital is captured for all atoms in the system.
    """
    
    if dos.get_spin_state() == 'restricted' or addspins == True:
        for item in collections:
            sumdos = np.zeros(dos.get_npts())
            
            for i in range(1,dos.get_nr_atoms()+1):
                atomdos = dos.get_dos_atom(i-1)
                for state in atomdos['states']:
                    if ('%i-%s' % (i,state['label'])) in item['set']:
                        sumdos += state['states']
                    if ('all-%s' % (state['label'])) in item['set']:
                        sumdos += state['states']
                    if 'all-all' in item['set']:
                        sumdos += state['states']
                    
            __plot_dos(ax, 
                       dos.get_energies(), 
                       sumdos, 
                       color=item['color'],
                       label=item['legendlabel'],
                       style=item['style'] if 'style' in item else None,
                       dosobject = dos)
            
    elif dos.get_spin_state() == 'unrestricted':
        
        for item in collections:
            sumdosup = np.zeros(dos.get_npts())
            sumdosdown = np.zeros(dos.get_npts())
            
            for i in range(1,dos.get_nr_atoms()+1):
                atomdos = dos.get_dos_atom(i)
                for state in atomdos['states']:
                    if ('%i-%s' % (i,state['label'])) in item['set']:
                        sumdosup += state['states_up']
                        sumdosdown += state['states_down']
                    if ('all-%s' % (state['label'])) in item['set']:
                        sumdosup += state['states_up']
                        sumdosdown += state['states_down']
                    if 'all-all' in item['set']:
                        sumdosup += state['states_up']
                        sumdosdown += state['states_down']
                    
            __plot_dos(ax, 
                       dos.get_energies(), 
                       sumdosup, 
                       color=item['color'],
                       label=item['legendlabel'],
                       style=item['style'] if 'style' in item else None,
                       dosobject = dos)
        
            __plot_dos(ax, 
                       dos.get_energies(), 
                       -sumdosdown, 
                       color=item['color'],
                       style=item['style'] if 'style' in item else None,
                       dosobject = dos)
    else:
        raise Exception('Unknown spin configuration: %s' % dos.get_spin_state())

def integrate_dos_bins(dos:DensityOfStates,
                       bins:list,
                       ao:list[str]=['all-all'],
                       **kwargs) -> list[dict]:
    """Calculate the total number of states for a list of bins

    Parameters
    ----------
    dos : DensityOfStates
        density of states object
    bins : list
        list of tuples containing lower and upper limits of the bins
    ao : list[str]
        list of projections to gather (see below)

    Returns
    -------
    list[dict]
        list of dictionaries containing bin limits and total states per bin
    """
    totaldos = np.zeros(dos.get_npts())
    energies = dos.get_energies()
    
    for i in range(1,dos.get_nr_atoms()+1):
        atomdos = dos.get_dos_atom(i-1)
        for state in atomdos['states']:
            if ('%i-%s' % (i,state['label'])) in ao:
                sumdos += state['states']
            if ('all-%s' % (state['label'])) in ao:
                sumdos += state['states']
            if 'all-all' in ao:
                totaldos += np.cumsum(state['states']) * dos.get_energy_interval()

    result = []
    for lim in bins:
        minidx = np.argmax(energies>lim[0])
        maxidx = np.argmax(energies>lim[1])
        idos = totaldos[maxidx] - totaldos[minidx]
        result.append({
            'bin' : lim,
            'idos': idos,
            'ao': ao,
        })
    
    return result
    

def __plot_dos(ax:matplotlib.axes._axes.Axes,
               energies:np.ndarray[np.float32],
               dos:np.ndarray[np.float32],
               color='#000000',
               label=None,
               style=None,
               dosobject=None):
    
    if style is None or style == 'line':
        ax.plot(dos, energies, color=color, label=label)
    elif style == 'filled':
        ax.fill_betweenx(energies, 0, dos, color=color, label=label)
    elif style == 'integrated':
        ax.plot(np.cumsum(dos) * dosobject.get_energy_interval(), energies, color=color, linestyle='--', label=label)
    else:
        raise Exception('Unknown keyword style = %s' % style)
        
    ax.set_xlabel('States [-]')
    ax.set_ylabel('Energy $E - E_{f}$ [eV]')
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    ax.yaxis.set_minor_locator(MultipleLocator(1))

    
