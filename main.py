from ivy.std_api import IvyInit, IvyStart, IvySendMsg, IvyStop
from time import sleep
from math import sin, cos
import scipy.integrate as integrate
from numpy as np import inf

app_name = "Sender"
ivy_bus = "127.255.255.255:2010"


def null_cb(*a):
    pass


def main():
    IvyInit(app_name, app_name + " is ready!", 0, null_cb, null_cb)
    IvyStart(ivy_bus)
    sleep(1.0)

    while(1):
        IvySendMsg("APLAT p=3.5")
        sleep(3.0)
    IvyStop()


if __name__ == "__main__":
    main()