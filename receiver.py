from ivy.std_api import IvyInit, IvyStart, IvyBindMsg, IvyMainLoop
from config import app_name, ivy_bus, null_cb

recorded_data = {"FCU": {"Heading": None, "Track": None, "Mode": None}, "FGS": {"trueHeading": None, "Point": {"x": None, "y": None}}, "StateVector": {"x": None, "y": None, "z": None, "fpa": None, "psi": None, "phi": None}, "Wind": {"Speed": None, "Dir": None}, "RollRate": {"Min": None, "Max": None}, "MagneticDec": None}
app_name = "Receiver"


def getFCUHeading(agent, *data):
    global recorded_data
    recorded_data["FCU"]["Heading"] = data[0]
    print("FCU Heading: " + recorded_data["FCU"]["Heading"])


def getFCUTrack(agent, *data):
    global recorded_data
    recorded_data["FCU"]["Track"] = data[0]
    print("FCU Track: " + recorded_data["FCU"]["Track"])
    

def getFCUMode(agent, *data):
    global recorded_data
    recorded_data["FCU"]["Mode"] = data[0]
    print("Selected Mode: " + recorded_data["FCU"]["Mode"])


def getStateVector(agent, *data):
    global recorded_data
    recorded_data["StateVector"]["x"] = data[0]
    recorded_data["StateVector"]["y"] = data[1]
    recorded_data["StateVector"]["z"] = data[2]
    recorded_data["StateVector"]["Vp"] = data[3]
    recorded_data["StateVector"]["fpa"] = data[4]
    recorded_data["StateVector"]["psi"] = data[5]
    recorded_data["StateVector"]["phi"] = data[6]
    print("State Vector: {}".format(recorded_data["StateVector"]))


def getFGSTrueHeading(agent, *data):
    global recorded_data
    recorded_data["FGS"]["trueHeading"] = data[0]
    print("FGS True Heading: " + recorded_data["FGS"]["trueHeading"])
    

def getFGSPoint(agent, *data):
    global recorded_data
    recorded_data["FGS"]["Point"]["x"] = data[0]
    recorded_data["FGS"]["Point"]["y"] = data[1]
    
    print("FGS Point: {}".format(recorded_data["FGS"]["Point"]))


def neededDataIsNone():
    recorded_data


def getWind(agent, *data):
    global recorded_data
    recorded_data["Wind"]["Speed"] = data[0]
    recorded_data["Wind"]["Dir"] = data[1]
    print("Wind Speed: " + recorded_data["Wind"]["Speed"] + " Wind Direction: " + recorded_data["Wind"]["Dir"])


def getMagneticDeclinaison(agent, *data):
    global recorded_data
    recorded_data["MagneticDec"] = data[0]
    print("Magnetic Declinaison: " + recorded_data["MagneticDec"])


def getRollRate(agent, *data):
    global recorded_data
    recorded_data["RollRate"]["Min"] = data[1]
    recorded_data["RollRate"]["Max"] = data[0]
    print("Roll Rate Min: " + recorded_data["RollRate"]["Min"] + " Max: " + recorded_data["RollRate"]["Max"])


IvyInit(app_name, app_name + " is ready", 0, null_cb, null_cb)
IvyStart("127.255.255.255:2010")


IvyBindMsg(getFCUHeading, r"^FCULATERAL Mode = SelectedHeading Val=(\S+)")
IvyBindMsg(getFCUTrack, r"^FCULATERAL Mode = SelectedTrack Val=(\S+)")
IvyBindMsg(getFCUMode, r"^FCULATERAL Mode = Managed Val=(\S+)")
IvyBindMsg(getStateVector, r"^StateVector x=(\S+) y=(\S+) z=(\S+) Vp=(\S+) fpa=(\S+) psi=(\S+) phi=(\S+)")
IvyBindMsg(getWind, r"^WindComponent VWind=(\S+) dirWind=(\S+)")
IvyBindMsg(getMagneticDeclinaison, r"^MagneticDeclinaison=(\S+)")
IvyBindMsg(getRollRate, r"^RollRateLim  MaxRollRate=(\S+) / MinRollRate=(\S+)")
IvyBindMsg(getFGSPoint, r"^FGS FgsPt=\((\w+),(\w+)\)")
IvyBindMsg(getFGSTrueHeading, r"^FGS FgsCap=(\S+)")

IvyMainLoop()