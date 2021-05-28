from numpy import pi

# Init variables
g = 9.81                # gravitational constant (m/s)
DEG2RAD = pi/180        # degree to radian
FT2M = 0.3048           # feet to meter
NM2M = 1852             # nautical mile to meter
KTS2MS = NM2M/3600      # knot to m/s
FL2M = 100*FT2M         # flight level to meter
TPSI95 = 10             # Response time in s of 95% of time
TPHI95 = 1              
TAUPSI = TPSI95/3
TAUPHI = TPHI95/3