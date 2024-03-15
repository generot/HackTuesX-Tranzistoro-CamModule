from network import WLAN, STA_IF    
from webserver import webcam
import display

NET_SSID = "MartinHotspot123"
NET_PASS = "eaah6847"

def connect_to_network(_ssid, _pass):
    station = WLAN(STA_IF)

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

def run_application():
    d = display.display_init()
    
    IP = st_interface.ifconfig()[0]
    
    d.fill(0)
    display.println(d, "Module started.")
    display.println(d, "")
    display.println(d, "IP: ")
    display.println(d, IP)
    d.show()

    server = webcam()
    server.run(d)
    
run_application()