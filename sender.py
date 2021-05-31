from ivy.std_api import IvySendMsg, IvyStop
from time import sleep

def sendData():
    while(1):
        # for test only
        # IvySendMsg("FCULATERAL Mode=SelectedHeading Val=50")
        IvySendMsg("FCULATERAL Mode=SelectedTrack Val=50")
        # IvySendMsg("FCULATERAL Mode=Managed Val=0")
        IvySendMsg("StateVector x=33 y=44 z=12 Vp=118 fpa=20 psi=5 phi=5")
        IvySendMsg("WindComponent VWind=5 dirWind=200")
        IvySendMsg("MagneticDeclinaison=0")
        IvySendMsg("RollRateLim  MaxRollRate=66 / MinRollRate=0")
        # IvySendMsg("FGS FgsPt x=120 y=5")
        # IvySendMsg("FGS FgsCap cap=50")
        sleep(3.0)
    IvyStop()