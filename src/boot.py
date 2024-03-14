#Connect to an internet provider network on boot.
import network

NET_SSID = "VIVACOM_FiberNet"
NET_PASS = "TONIdata"

def connect_to_network(_ssid, _pass):
    station = network.WLAN(network.STA_IF)

    if not station.active():
        station.active(True)

    station.connect(_ssid, _pass)

    while not station.isconnected():
        pass

    print("Network configuration: ", station.ifconfig())

    return station

def disconnect(station):
    station.active(False)

st_interface = connect_to_network(NET_SSID, NET_PASS)

def get_interface():
    return st_interface