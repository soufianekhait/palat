from ivy.std_api import IvyInit, IvyStart
from time import sleep
from config import app_name, ivy_bus, null_cb
from sender import sendData


def main():
    IvyInit(app_name, app_name + " is ready to send!", 0, null_cb, null_cb)
    IvyStart(ivy_bus)
    sleep(1.0)
    # send AP LAT data
    sendData()


if __name__ == "__main__":
    main()