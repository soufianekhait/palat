from ivy.std_api import IvySendMsg, IvyStop, IvyInit, IvyStart      # grab Ivy functions
from time import sleep                                              # sleep = happiness
from config import ivy_bus, null_cb                                 # grab ivy variables


def sendData():
    while(1):
        # for test only
        #IvySendMsg("FCULATERAL Mode=SelectedHeading Val=50")
        #IvySendMsg("FCULATERAL Mode=SelectedTrack Val=50")
        # IvySendMsg("FCULATERAL Mode=Managed Val=0")
        IvySendMsg("StateVector x=0 y=0 z=12 Vp=118.3222 fpa=0 psi=0 phi=0")
        IvySendMsg("WindComponent VWind=10 dirWind=200")
        IvySendMsg("MagneticDeclinaison=0")
        IvySendMsg("RollRateLim  MaxRollRate=66 / MinRollRate=0")
        IvySendMsg("FGS FgsPt x=120 y=10")
        IvySendMsg("FGS FgsCap cap=50")
        sleep(10)
    IvyStop()


def main():
    app_name = "Sender"
    IvyInit(app_name, app_name + " is ready to send!", 0, null_cb, null_cb)
    IvyStart(ivy_bus)
    sleep(1.0)
    # send AP LAT data
    sendData()


if __name__ == "__main__":
    main()