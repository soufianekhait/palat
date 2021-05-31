from ivy.std_api import IvyInit, IvyStart, IvyBindMsg, IvyMainLoop, IvySendMsg
from config import DEG2RAD, app_name, null_cb, ivy_bus, TAUPHI, TAUPSI, TAUEY, g         # global variables
from math import asin, atan2, sin, cos, pi, sqrt    # grab ain function

# init all variables to zero
recorded_data = {"FCU": {"Mode": "", "ModeValue": 0}, "FGS": {"trueHeading": 0, "Point": {"x": 0, "y": 0}}, "StateVector": {"x": 0, "y": 0, "z": 0, "Vp": 200, "fpa": 0, "psi": 0, "phi": 0}, "Wind": {"Speed": 0, "Dir": 0}, "RollRate": {"Min": 0, "Max": 0}, "MagneticDec": 0}
app_name = "Receiver"

# variables of interest
v = float(recorded_data["StateVector"]["Vp"])           # speed m/s
fpa = float(recorded_data["StateVector"]["fpa"])        # flight path angle in radian
hdg = int(recorded_data["StateVector"]["psi"])          # heading in radian
phi = float(recorded_data["StateVector"]["phi"])        # bank angle in radian
windSpeed = int(recorded_data["Wind"]["Speed"])         # Wind speed
windDir = int(recorded_data["Wind"]["Dir"])             # Wind direction

# derivatives of aiaft position
xDot = v * cos(hdg) * cos(fpa) + windSpeed * cos(windDir + pi)
yDot = v * sin(hdg) * cos(fpa) + windSpeed * sin(windDir + pi)

# Aiaft track, wind effect and Ground Speed
acTrack = atan2(yDot, xDot)
windEffect = asin(windSpeed * sin((acTrack - windDir)/v*cos(fpa)))
Gs = sqrt(xDot**2 + yDot**2)


def getFCUMode(agent, *data):
    global recorded_data
    recorded_data["FCU"]["Mode"] = data[0]
    recorded_data["FCU"]["ModeValue"] = int(data[1])
    p = sendRollRate()
    IvySendMsg("APLAT p={}".format(p))
    print("P sent with value {}".format(p))


def getStateVector(agent, *data):
    global recorded_data
    for key, value in zip(recorded_data["StateVector"].keys(), data):
        recorded_data["StateVector"][key] = value


def getFGSTrueHeading(agent, *data):
    global recorded_data
    recorded_data["FGS"]["trueHeading"] = int(data[0])
    

def getFGSPoint(agent, *data):
    global recorded_data
    recorded_data["FGS"]["Point"]["x"] = int(data[0])
    recorded_data["FGS"]["Point"]["y"] = int(data[1])


def getWind(agent, *data):
    global recorded_data
    recorded_data["Wind"]["Speed"] = int(data[0])
    recorded_data["Wind"]["Dir"] = int(data[1])


def getMagneticDeclinaison(agent, *data):
    global recorded_data
    recorded_data["MagneticDec"] = float(data[0])


def getRollRate(agent, *data):
    global recorded_data
    recorded_data["RollRate"]["Min"] = float(data[1])
    recorded_data["RollRate"]["Max"] = float(data[0])


def sendRollRate():
    # check if Mode is Managed
    if recorded_data["FCU"]["Mode"] == "Managed":
        x = recorded_data["FGS"]["Point"]["x"]
        y = recorded_data["FGS"]["Point"]["y"]
        hdgC = recorded_data["FGS"]["trueHeading"] * DEG2RAD
        return computeRollRate(axis=[x, y, hdgC], track=None, heading=None)

    # check if Mode is on Selected Track
    # True track = Magnetic track - Magnetic declinaison
    if recorded_data["FCU"]["Mode"] == "SelectedTrack":
        return computeRollRate(axis=None, track=((recorded_data["FCU"]["ModeValue"] * DEG2RAD) - recorded_data["MagneticDec"]), heading=None)

    # check if Mode is on Selected Heading
    # True heading = Magnetic heading - Magnetic declinaison
    if recorded_data["FCU"]["Mode"] == "SelectedHeading":
        return computeRollRate(axis=None, track=None, heading=((recorded_data["FCU"]["ModeValue"] * DEG2RAD) - recorded_data["MagneticDec"]))


# check Roll Rate boundaries
def checkBoundaries(value):
    min = recorded_data["RollRate"]["Min"] * DEG2RAD
    max = recorded_data["RollRate"]["Max"] * DEG2RAD
    
    if value >= min and value <= max:
        return value
    elif value > max:
        return max
    else:
        return min


# Set delta max between consigne and real value
def setDelta(consigne, real, max=15*DEG2RAD):
    if abs(consigne - real) > max:
        return max
    else:
        return consigne - real


# Compute Roll Rate (radian)
def computeRollRate(**modes):
    for m in modes:
        if modes[m] is not None:
            if m == "heading":
                print("P value before checking boundaries: {}".format(((v*setDelta(modes[m], hdg)/(TAUPSI*g)) - phi) / TAUPHI))
                return checkBoundaries(((v*setDelta(modes[m], hdg)/(TAUPSI*g)) - phi) / TAUPHI)
            elif m == "track":
                hdgC = modes[m] - windEffect
                print("P value before checking boundaries: {}".format(((v*setDelta(hdgC, hdg)/(TAUPSI*g)) - phi) / TAUPHI))
                return checkBoundaries(((v*setDelta(hdgC, hdg)/(TAUPSI*g)) - phi) / TAUPHI)
            else:
                wpTrack = modes[m][2]
                ey = cos(wpTrack) * (int(recorded_data["StateVector"]["y"]) - modes[m][1]) - sin(wpTrack) * (int(recorded_data["StateVector"]["x"]) - modes[m][0])
                arg = ey/(TAUEY*Gs)
                if arg > 0.5:
                    arg = 0.5
                elif arg < -0.5:
                    arg = -0.5
                trackC = wpTrack - asin(arg)
                hdgC = trackC - windEffect
                print("P value before checking boundaries: {}".format(((v*setDelta(hdgC, hdg)/(TAUPSI*g)) - phi) / TAUPHI))
                return checkBoundaries(((v*setDelta(hdgC, hdg)/(TAUPSI*g)) - phi) / TAUPHI)


def main():
    IvyInit(app_name, app_name + " is ready", 0, null_cb, null_cb)
    IvyStart(ivy_bus)

    IvyBindMsg(getFCUMode, r"^FCULATERAL Mode=(\w+) Val=(\d+)")
    IvyBindMsg(getStateVector, r"^StateVector x=(\d+) y=(\d+) z=(\d+) Vp=(\d+) fpa=(\d+) psi=(\d+) phi=(\d+)")
    IvyBindMsg(getWind, r"^WindComponent VWind=(\d+) dirWind=(\d+)")
    IvyBindMsg(getMagneticDeclinaison, r"^MagneticDeclinaison=(\d+)")
    IvyBindMsg(getRollRate, r"^RollRateLim  MaxRollRate=(\d+) / MinRollRate=(\d+)")
    IvyBindMsg(getFGSPoint, r"^FGS FgsPt x=(\d+) y=(\d+)")
    IvyBindMsg(getFGSTrueHeading, r"^FGS FgsCap cap=(\d+)")

    IvyMainLoop()


if __name__ == "__main__":
    main()