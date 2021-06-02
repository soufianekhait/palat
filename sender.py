#!/usr/bin/python3
from ivy.std_api import IvySendMsg, IvyStop, IvyInit, IvyStart      # grab Ivy functions
from time import sleep                                              # sleep = happiness
from signal import signal, SIGINT, SIGTERM                          # grab signal functions
from config import ivy_bus, null_cb                                 # grab ivy variables

running = True


def sendData():
    while running:
        # for test only
        #IvySendMsg("FCULATERAL Mode=SelectedHeading Val=50")
        #IvySendMsg("FCULATERAL Mode=SelectedTrack Val=50")
        # IvySendMsg("FCULATERAL Mode=Managed Val=0")
        """
        IvySendMsg("StateVector x=0 y=0 z=12 Vp=118.3222 fpa=0 psi=0 phi=0")
        IvySendMsg("WindComponent VWind=10 dirWind=200")
        IvySendMsg("MagneticDeclinaison=0")
        IvySendMsg("RollRateLim  MaxRollRate=66 / MinRollRate=0")
        IvySendMsg("FGS FgsPt x=120 y=10")
        IvySendMsg("FGS FgsCap cap=50")
        """
        sleep(10)


def stop(*a):
    global running
    running = False
    IvyStop()


def main():
    signal(SIGINT, stop)
    signal(SIGTERM, stop)

    IvyInit("Sender", "Sender is ready to send!", 0, null_cb, null_cb)
    IvyStart(ivy_bus)
    sleep(1.0)
    # send AP LAT data
    sendData()


if __name__ == "__main__":
    main()