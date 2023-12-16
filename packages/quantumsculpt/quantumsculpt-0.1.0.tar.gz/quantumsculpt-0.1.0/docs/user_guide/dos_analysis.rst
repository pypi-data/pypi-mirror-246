.. _dos_analysis:
.. index:: dosanalysis

DOS analysis
============

Getting started
---------------

:program:`QuantumSculpt` can perform analysis on DOS files via the :code:`DensityOfStates` class
and the plotting routines as part of the :code:`quantumsculpt` module.

To parse the contents of a :code:`DOSCAR.lobster` file, we execute the following

.. code:: python

    import os
    import matplotlib.pyplot as plt
    from quantumsculpt import DensityOfStates, CrystalOrbitalHamiltonPopulation
    import quantumsculpt as qs

    # load the DOSCAR.lobster file via a DensityOfStates class
    ROOT = os.path.dirname(__file__)
    filename = os.path.join(ROOT, '..', '..', 'samples', 'carbonmonoxide_gasphase', 'pbe', 'DOSCAR.lobster')
    dos = DensityOfStates(filename)

The object :code:`dos` contains the complete contents of the :code:`DOSCAR.lobster` file and can be used
for retrieval of specific data as well as for visualization. For example, to retrieve the energies and
the total density of states, we can use the following

.. code:: python

    print(dos.get_nr_atoms())
    energies = dos.get_energies()
    print(energies.shape, energies[0], energies[-1])
    totaldos = dos.get_total_dos()
    print(totaldos.keys())

The output of the above code is::

    2
    (801,) -30.03755 10.01252
    dict_keys(['energies', 'states', 'istates'])

This output essentially tells us that the DOSCAR file contains 2 atoms and has 801 data points between
the energy interval :math:`E \in (-30.03, 10.01)`. The function :code:`total_dos()` retrieves a dictionary
containing (once more) the energy values, the states per energy and the integrated states. One can directly
use these attributes for visualization purposes.

.. code:: python

    plt.figure(dpi=144, figsize=(4,4))
    plt.plot(totaldos['states'], energies)
    plt.xlabel('States [-]')
    plt.ylabel('Energies $E - E_{f}$ [eV]')
    plt.grid(linestyle='--', alpha=0.5)
    plt.tight_layout()

Alternatively, one can also use one of the plotting routines. These plotting routines are designed such that
they take a Matplotlib axes object as input. This allows the user to easily produce graphs potentially
containing multiple plots. For example, the function :code:`plot_total_dos` can be used to construct
the total density of states for the system under study.

.. code:: python

    fig, ax = plt.subplots(1, 1, dpi=144, figsize=(4,4))
    qs.plot_total_dos(ax, 
                    dos, 
                    grid=True, 
                    ylim=(-25,5),
                    title='Total DOS CO(g)')

.. figure:: ../_static/img/dos/dos00.png

Decompositions and collections
------------------------------

Quite often, the Kohn-Sham states are projected onto spherical harmonics to produce so-called
LM-decomposed density of states. For particular projections, i.e. specific l-states, we wish
to collect the result. A salient example pertains to the identification of the σ and π states
in CO. An example code is provided below.

.. code:: python

    import os
    import matplotlib.pyplot as plt
    from quantumsculpt import DensityOfStates, CrystalOrbitalHamiltonPopulation
    import quantumsculpt as qs

    # load the DOSCAR.lobster file via a DensityOfStates class
    ROOT = os.path.dirname(__file__)
    filename = os.path.join(ROOT, '..', '..', 'samples', 'carbonmonoxide_gasphase', 'pbe', 'DOSCAR.lobster')
    dos = DensityOfStates(filename)

    # build a figure composed of two plots
    fig, ax = plt.subplots(1,2, dpi=144, figsize=(8,4))
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

    qs.plot_gathered_dos(ax[1], 
                        dos,
                        collection, 
                        grid=True, 
                        ylim=(-25,5), 
                        legend=True,
                        title='lm-DOS CO(g)')

    plt.tight_layout()

.. figure:: ../_static/img/dos/dos01.png

Collections are captured by an array of dictionaries containing four mandatory keys:

* :code:`set`: which orbitals to collect (by default done for all atoms)
* :code:`legendlabel`: which label to use in the legend of the figure
* :code:`color`: color of the curve
* :code:`style`: which plotting style to use (:code:`filled` or :code:`integrated`)

:code:`sets` herein corresponds to a list of atom-orbital pairs. For example :code:`all-2s` means the `2s`
states for all atoms, whereas :code:`1-2p_x` would imply the :math:`2p_{x}` orbital on the first atom.
Expanding on the previous example, we can for example add two more subplots where we show the σ and π states
for the carbon and oxygen atoms seperately.

.. code:: python

    import os
    import matplotlib.pyplot as plt
    from quantumsculpt import DensityOfStates, CrystalOrbitalHamiltonPopulation
    import quantumsculpt as qs

    # load the DOSCAR.lobster file via a DensityOfStates class
    ROOT = os.path.dirname(__file__)
    filename = os.path.join(ROOT, '..', '..', 'samples', 'carbonmonoxide_gasphase', 'pbe', 'DOSCAR.lobster')
    dos = DensityOfStates(filename)

    # plot the total dos, including the fitted peaks
    fig, ax = plt.subplots(2,2, dpi=144, figsize=(8,8))
    qs.plot_total_dos(ax[0,0], 
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

    # plot the lm-decomposed DOS according to the collection settings
    qs.plot_gathered_dos(ax[0,1], 
                        dos,
                        collection, 
                        grid=True, 
                        ylim=(-25,5), 
                        legend=True,
                        title='lm-DOS CO(g)')

    # specify which collections of projections to plot
    collection = [
        {'set': ['1-2s', '1-2p_x'], 'legendlabel' : '$\sigma$', 'color': '#FF0000AA', 'style': 'filled'},
        {'set': ['1-2p_y', '1-2p_z'], 'legendlabel' : '$\pi$', 'color': '#0000FFAA', 'style': 'filled'},
        {'set': ['1-2s', '1-2p_x'], 'legendlabel' : '$int - \sigma$', 'color': '#FF0000AA', 'style': 'integrated'},
        {'set': ['1-2p_y', '1-2p_z'], 'legendlabel' : '$int - \pi$', 'color': '#0000FFAA', 'style': 'integrated'}
    ]

    # plot the lm-decomposed DOS according to the collection settings
    qs.plot_gathered_dos(ax[1,0], 
                        dos,
                        collection, 
                        grid=True, 
                        xlim=(0,10),
                        ylim=(-25,5), 
                        legend=True,
                        title='lm-DOS carbon atom')

    # specify which collections of projections to plot
    collection = [
        {'set': ['2-2s', '2-2p_x'], 'legendlabel' : '$\sigma$', 'color': '#FF0000AA', 'style': 'filled'},
        {'set': ['2-2p_y', '2-2p_z'], 'legendlabel' : '$\pi$', 'color': '#0000FFAA', 'style': 'filled'},
        {'set': ['2-2s', '2-2p_x'], 'legendlabel' : '$int - \sigma$', 'color': '#FF0000AA', 'style': 'integrated'},
        {'set': ['2-2p_y', '2-2p_z'], 'legendlabel' : '$int - \pi$', 'color': '#0000FFAA', 'style': 'integrated'}
    ]

    # plot the lm-decomposed DOS according to the collection settings
    qs.plot_gathered_dos(ax[1,1], 
                        dos,
                        collection, 
                        grid=True, 
                        xlim=(0,10),
                        ylim=(-25,5), 
                        legend=True,
                        title='lm-DOS oxygen atom')

    plt.tight_layout()

.. figure:: ../_static/img/dos/dos01b.png

Peak integration
----------------

Another common use case is that one wants to determine the number of states under
a given peak or feature. This can be done either manually or semi-automatically.
First, one needs to determine the start and end point of the peaks. This can be
done visually or via peak detection and curve fitting. We explain both methods here.

Manually
********

Manual characterization of peaks or features is as simple as specifying the starting
and ending position of the peaks and collecting this as a list of tuples. An example
is shown below.

.. code :: python

    .. code:: python

    import os
    import matplotlib.pyplot as plt
    from quantumsculpt import DensityOfStates, CrystalOrbitalHamiltonPopulation
    import quantumsculpt as qs

    # load the DOSCAR.lobster file via a DensityOfStates class
    ROOT = os.path.dirname(__file__)
    filename = os.path.join(ROOT, '..', '..', 'samples', 'carbonmonoxide_gasphase', 'pbe', 'DOSCAR.lobster')
    dos = DensityOfStates(filename)

    # specify where to place the bins for peak integration
    bins = [
        (-23,-21),
        (-6,-5),
        (-3.8,-2.1),
        (-1,1),
    ]

    fig, ax = plt.subplots(1,2, dpi=144, figsize=(8,4))
    qs.plot_total_dos(ax[0], 
                    dos, 
                    grid=True, 
                    ylim=(-25,5),
                    title='Total DOS CO(g)',
                    bins=bins)

    # specify which collections of projections to plot
    collection = [
        {'set': ['2s', '2p_x'], 'legendlabel' : '$\sigma$', 'color': '#FF0000AA', 'style': 'filled'},
        {'set': ['2p_y', '2p_z'], 'legendlabel' : '$\pi$', 'color': '#0000FFAA', 'style': 'filled'},
        {'set': ['2s', '2p_x'], 'legendlabel' : '$int - \sigma$', 'color': '#FF0000AA', 'style': 'integrated'},
        {'set': ['2p_y', '2p_z'], 'legendlabel' : '$int - \pi$', 'color': '#0000FFAA', 'style': 'integrated'}
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
    for res in qs.integrate_dos_bins(dos, bins):
        print(res)

    plt.tight_layout()

.. figure:: ../_static/img/dos/dos02.png

By means of the argument :code:`bins` in the plot functions, we can place horizontal dashed bars to indicate
the peak feature. Next, using the function :code:`integrate_dos_bins`, we can integrate the curve 
under the peaks. The result of the integration is::

    {'bin': (-23, -21), 'idos': 1.9999977052211761}
    {'bin': (-6, -5), 'idos': 1.9959099888801575}
    {'bin': (-3.8, -2.1), 'idos': 3.9999983310699463}
    {'bin': (-1, 1), 'idos': 1.9999994039535522}

Curve fitting
*************

For DOS plots that are not overly complicated, we can also use semi-automatic peak recognition.
This is two-fold technique wherein first the peaks are being recognized after which the whole
DOS is fitted using a series of Gaussians located at the peak centers. The process is shown
in the example below.

.. code :: python

    .. code:: python

    import os
    import matplotlib.pyplot as plt
    from quantumsculpt import DensityOfStates, CrystalOrbitalHamiltonPopulation
    import quantumsculpt as qs

    # load the DOSCAR.lobster file via a DensityOfStates class
    ROOT = os.path.dirname(__file__)
    filename = os.path.join(ROOT, '..', '..', 'samples', 'carbonmonoxide_gasphase', 'pbe', 'DOSCAR.lobster')
    dos = DensityOfStates(filename)

    # try to find perfect peak barriers
    energies = dos.get_energies()
    totaldos = dos.get_total_dos()['states']

    # try to find the peaks via fitting
    peaks = qs.find_peaks(energies, totaldos)
    fitres = qs.fit_gaussians(energies, totaldos, peaks[1])

    # build bins based on Gaussian fit; since the peaks are not true Gaussians,
    # there is some wiggle room. Normally 6-sigma woudl correspond to 99.73% of the
    # curve, but we need slightly larger values here
    bins = []
    for g in fitres['gaussians']:
        bins.append([g['mu'] - 6*g['sigma'], g['mu'] + 6*g['sigma']])

    # plot the total dos, including the fitted peaks
    fig, ax = plt.subplots(1,2, dpi=144, figsize=(8,4))
    qs.plot_total_dos(ax[0], 
                    dos, 
                    grid=True, 
                    ylim=(-25,5),
                    title='Total DOS CO(g)',
                    bins=bins)

    # specify which collections of projections to plot
    collection = [
        {'set': ['all-2s', 'all-2p_x'], 'legendlabel' : '$\sigma$', 'color': '#FF0000AA', 'style': 'filled'},
        {'set': ['all-2p_y', 'all-2p_z'], 'legendlabel' : '$\pi$', 'color': '#0000FFAA', 'style': 'filled'},
        {'set': ['all-2s', 'all-2p_x'], 'legendlabel' : '$int - \sigma$', 'color': '#FF0000AA', 'style': 'integrated'},
        {'set': ['all-2p_y', 'all-2p_z'], 'legendlabel' : '$int - \pi$', 'color': '#0000FFAA', 'style': 'integrated'}
    ]

    # plot the lm-decomposed DOS according to the collection settings
    qs.plot_gathered_dos(ax[1], 
                        dos,
                        collection, 
                        grid=True, 
                        ylim=(-25,5), 
                        legend=True,
                        title='lm-DOS CO(g)',
                        bins=bins)

    # gather the total number of states for the bins
    for res in qs.integrate_dos_bins(dos, bins):
        print(res)

    plt.tight_layout()

.. figure:: ../_static/img/dos/dos03.png

Using automatic feature identification, we find the following number of states per feature::

    {'bin': [-22.525813676686806, -21.52059420564571], 'idos': 1.9975767384457868}
    {'bin': [-6.028714279345682, -5.023495305818278], 'idos': 1.9986334890127182}
    {'bin': [-3.295714904386506, -2.2904935045473827], 'idos': 3.9957660500658676}
    {'bin': [-0.5314182996729327, 0.47380919094380375], 'idos': 1.9983294308185577}
    {'bin': [8.612502992327293, 9.618121650111298], 'idos': 4.013029038906097}

.. note ::

    The width of the peaks remains a bit of tuning on the side of the user. Normally, you would
    expect that :math:`\mu \pm 3\sigma` would constitute about 99.73% of the peak area, but in
    the example above, we needed to use :math:`\mu \pm 5\sigma`.