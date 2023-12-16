import unittest
import numpy as np
import sys
import os

# add a reference to load the module
ROOT = os.path.dirname(__file__)
sys.path.append(os.path.join(ROOT, '..'))

from quantumsculpt import CrystalOrbitalHamiltonPopulation as COHP

filename = os.path.join(ROOT, '..', 'samples', 'COHPCAR.lobster')
cohp = COHP(filename)

cohp.plot_average()