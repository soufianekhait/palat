from ivy.std_api import IvyInit, IvyStart, IvyBindMsg, IvyMainLoop

recorded_data = None
null_cb = lambda *a: None
app_name = "Receiver"


def on_msg(agent, *data):
    global recorded_data
    recorded_data = data[0]
    print(recorded_data)


IvyInit(app_name, app_name + " is ready", 0, null_cb, null_cb)
IvyStart("127.255.255.255:2010")
IvyBindMsg(on_msg, r"^APLAT p=(\S+)")
IvyMainLoop()