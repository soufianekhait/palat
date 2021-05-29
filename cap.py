from config import TAUPHI, TAUPSI, g            # global variables
from receiver import recorded_data              # output dictionnary


# Equilibrium variables of interest
v = recorded_data["StateVector"]["Vp"]          # speed m/s
fpa = recorded_data["StateVector"]["fpa"]       # flight path angle in radian
hdg = recorded_data["StateVector"]["psi"]       # heading in radian
phi = recorded_data["StateVector"]["phi"]       # bank angle in radian


def sendRollRate():
    # check if Mode is Managed
    if int(recorded_data["FCU"]["Mode"]) == 0:
        x = recorded_data["FGS"]["Point"].x
        y = recorded_data["FGS"]["Point"].y
        hdgC = recorded_data["FGS"]["trueHeading"]
        computeRollRate(axis=[x, y, hdgC], track=None, heading=None)
    if int(recorded_data["FCU"]["Track"]) is not None:
        computeRollRate(axis=None, track=int(recorded_data["FCU"]["Track"]), heading=None)
    if int(recorded_data["FCU"]["Heading"]) is not None:
        computeRollRate(axis=None, track=None, heading=int(recorded_data["FCU"]["Heading"]))

    # Reset State Vector dict
    for record in recorded_data["StateVector"].values():
        print(record)
        record = None


def checkBoundaries(value):
    min = recorded_data["RollRate"]["Min"]
    max = recorded_data["RollRate"]["Max"]
    
    if value >= min and value <= max:
        return value
    elif value > max:
        return max
    else:
        return min
        

# compute Roll Rate : the output is in radian
def computeRollRate(**modes):
    for m in modes:
        if modes[m] is not None:
            if m == "heading":
                return checkBoundaries(((v*(modes[m] - hdg)/(TAUPSI*g)) - phi) / TAUPHI)