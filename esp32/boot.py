import network

NET_SSID = "MartinHotspot123"
NET_PASS = "eaah6847"

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

def run_application():
    import machine
    import socketserver
    
    from webserver import webcam

    #socketserver.create_socket_server(on_connect=socketserver.on_connect_clb)

    server = webcam()
    server.run()
    
run_application()