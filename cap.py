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


# Equilibrium vector of interest
xE = np.array([[ve], [fpae], [hdge], [phie]])     # equilibrium state vector 
uE = np.array([[nxe], [nze], [pe]])               # equilibrium command vector


#Derivatives of multivariable function
 
v, gamma, psi, phi = sym.symbols('v gamma psi phi')
f = g * (nxe - sin(fpa))
 
#Differentiating partially w.r.t y
derivative_f = f.diff(v)
print(derivative_f)


# Compute State Vector
def computeStateVector(nx, nz, p):
    vDot = g * (computeNx() - sin(fpa))
    gammaDot = g/v * (nz * cos(phi) - cos(fpa))
    psiDot = g / (v * cos(fpa)) * computeNz * sin(phi)
    phiDot = p
    return np.array([[vDot], [gammaDot], [psiDot], [phiDot]])


# Integrate State Vector
def integrateStateVector(*params):
    v = integrate.quad(vDot, 0, np.inf)


# Capture Heading
def captureHDG():
    computeStateVector()