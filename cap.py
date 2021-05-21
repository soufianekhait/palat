# Init global variables
vDot, gammaDot, psiDot, phiDot = 0
v, gamma, psi, phi = 0
g = 9.81


# Compute vDot, gammaDot, psiDot and phiDot
def capture_cap(nx, nz, p):
    vDot = g * (nx - sin(gamma))
    gammaDot = g/v * (nz * cos(phi) - cos(gamma))
    psiDot = g / (v * cos(gamma)) * nz * sin(phi)
    phiDot = p
    return [vDot, gammaDot, psiDot, phiDot]


# Integrate cap
def integrate_cap(*params):
    v = integrate.quad(vDot, 0, inf)