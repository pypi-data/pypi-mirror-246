QuantumSculpt: Electronic structure analysis
============================================

:program:`QuantumSculpt` is a bundle of Python scripts to analyze the electronic
structure of systems calculated using `VASP <https://www.vasp.at/>`_. QuantumSculpt
is designed to operate on `VASP WAVECAR <https://www.vasp.at/wiki/index.php/WAVECAR>`_ files 
and on the output files of `Lobster <http://www.cohp.de/>`_, specifically DOS and COHP
type of files.

Tasks and Features
------------------

* Analyze, decompose and extract data from VASP WAVECAR files. :ref:`Read more <orbital_extraction>`.
* Visualize and analyze density of states data as generated via Lobster. :ref:`Read more <dos_analysis>`.
* Visualize and analyze crystal orbital hamilton population analysis data as generated via Lobster. :ref:`Read more <cohp_analysis>`.

:program:`QuantumSculpt` has been developed at the Eindhoven University of Technology,
Netherlands. :program:`QuantumSculpt` and its development are hosted on `github
<https://gitlab.tue.nl/inorganic-materials-chemistry/quantumsculpt>`_.  Bugs and feature
requests are ideally submitted via the `gitlab issue tracker
<https://gitlab.tue.nl/inorganic-materials-chemistry/quantumsculpt/-/issues>`_.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   user_guide/index
   api/index

Indices and tables
------------------

* :ref:`genindex`
* :ref:`search`
