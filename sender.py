from ivy.std_api import IvySendMsg, IvyStop
from time import sleep

def sendData():
    while(1):
        IvySendMsg("APLAT p=3.5")
        # for test only
        IvySendMsg("FCULATERAL Mode = SelectedHeading Val=40")
        IvySendMsg("FCULATERAL Mode = SelectedTrack Val=50")
        IvySendMsg("FCULATERAL Mode = Managed Val=10")
        IvySendMsg("StateVector x=33 y=44 z=12 Vp=120 fpa=20 psi=5 phi=5")
        IvySendMsg("WindComponent VWind=10 dirWind=180")
        IvySendMsg("MagneticDeclinaison=2")
        IvySendMsg("RollRateLim  MaxRollRate=66 / MinRollRate=0")
        IvySendMsg("FGS FgsPt=(120,5)")
        IvySendMsg("FGS FgsCap=120")
        sleep(3.0)
    IvyStop()