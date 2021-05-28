from math import sin, cos           # math functions
from scipy import integrate         # grab integrate functions
import numpy as np                  # grab all of the NumPy functions
from config import g                # global variables
from control.matlab import *        # MATLAB-like functions
from receiver import recorded_data  # output dictionnary
import sympy as sym                 # 


# Equilibrium variables of interest
ve = recorded_data["StateVector"]["Vp"]     # speed
fpae = recorded_data["StateVector"]["fpa"]  # flight path angle
hdge = recorded_data["StateVector"]["psi"]  # heading
phie = recorded_data["StateVector"]["phi"]  # bank angle
nxe = sin(fpae)                             # load factor X
nze = cos(fpae)/cos(phie)                   # load factor Z
pe = 0                                      # roll rate

# time in ms
t0 = 0
T = 150
N = 1000


# Equilibrium vector of interest
xe = np.array([[ve], [fpae], [hdge], [phie]])     # equilibrium state vector 
ue = np.array([[nxe], [nze], [pe]])               # equilibrium command vector

"""
#Derivatives of multivariable function
v, gamma, psi, phi = sym.symbols('v gamma psi phi')
f = g * (nxe - sin(fpa))
 
#Differentiating partially w.r.t y
derivative_f = f.diff(v)
print(derivative_f)


# Compute State Vector

def computeStateVector(nxe, nz, p):
    vDot = g * (nx - sin(fpa))
    fpaDot = g/v * (nz * cos(phi) - cos(fpa))
    psiDot = g / (v * cos(fpa)) * nz * sin(phi)
    phiDot = p
    return np.array([[vDot], [fpa], [psiDot], [phiDot]])


# Capture Heading
def captureHDG():
    computeStateVector()

"""


# Define parameters
# Functions
vDot = lambda fpa, nx: g * (nx - sin(fpa))
fpaDot = lambda fpa, phi, nz, v: g/v * (nz * cos(phi) - cos(fpa))
psiDot = lambda v, fpa, nz, phi: g / (v * cos(fpa)) * nz * sin(phi)
phiDot = p

h = (T-t0)/N                      # Step size
t = np.arange(0, 1 + h, h)        # Numerical grid
# Initial Conditions
v0 = ve
hdg0 = hdge
fpa0 = fpae
phi0 = phie

# Explicit Euler Method
v = np.zeros(len(t))
fpa = np.zeros(len(t))
hdg = np.zeros(len(t))
phi = np.zeros(len(t))
v[0] = v0
fpa[0] = fpa0
hdg[0] = hdg0
phi[0] = phi0


for i in range(0, len(t) - 1):
    v[i + 1] = v[i] + h*vDot(fpa[i], nxe)
    fpa[i + 1] = fpa[i] + h*fpaDot(fpa[i], phi[i], nze, v[i])
    psi[i + 1] = psi[i] + h*psiDot(v[i], fpa[i], nze, phi[i])