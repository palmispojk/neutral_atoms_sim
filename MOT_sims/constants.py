import scipy.constants as const
import numpy as np

# Real parameters as defined in the https://python-laser-cooling-physics.readthedocs.io/en/latest/examples/MOTs/03_F0_to_F1_3D_MOT_OBE_temperature.html and Max Mosers simulations
# The based on Sr88
frq_real = 603976506.6e6 * 2 * np.pi # wavelength lambda = c/f
gamma_real = 61.4e6
kmag_real = frq_real / const.c
muB_real = const.physical_constants["Bohr magneton"][0]
mass_real = const.value('atomic mass constant') * 88
alpha_real = 0.4  # in T/m

# Natural units for computation
gamma = 1 # sets the natural unit for line width. For the natural unit for time is 1/gamma
kmag = 1
muB = 1
mass = mass_real * gamma_real / const.hbar / kmag_real**2
alpha = alpha_real * muB_real / (gamma_real * kmag_real * const.hbar)
det = -2.1 * gamma
s = 2
transform = True

# offsets and scale for position and velocity. Used in starting position and velocity for atoms in simulation
rscale = np.array([2, 2, 2]) / alpha
roffset = np.array([0.0, 0.0, 0.0])
vscale = np.array([0.1, 0.1, 0.1])
voffset = np.array([0.0, 0.0, 0.0])