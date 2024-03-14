import socket
import camera

LOCALHOST = "0.0.0.0"
PORT = 80

SOCK_DATALEN = 1024

def create_socket_server(*args, **kwargs):
    address = socket.getaddrinfo(LOCALHOST, PORT)[0][-1]

    sock = socket.socket()
    sock.bind(address)
    sock.listen(0)
    
    print(f"Listening on port {PORT}.")
    
    conn, addr = sock.accept()
    
    print("Accepted connection")
    
    kwargs["on_connect"](conn)
                
def on_connect_clb(sock):    
    camera.init(0,
                format=camera.JPEG,
                framesize=camera.FRAME_HD,
                fb_location=camera.PSRAM)
    
    while True:
        img = camera.capture()
        
        sock.send(img)