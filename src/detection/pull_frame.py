import requests
import socket

import numpy as np

DEF_PORT = 80
DEF_DATABLOCK_SIZE = 1024

def connect_to_camserver(cam_IP, on_receive):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    resp = b""

    sock.connect((cam_IP, DEF_PORT))

    while True:
        data = sock.recv(DEF_DATABLOCK_SIZE)
        
        if len(data) > 0:
            resp += data
        else:
            on_receive(resp)
            resp = b""

def on_image_receive(data):
    bytearr =  bytes(data)
    jpeg_list = list(bytearr)

    np_arr = np.array(jpeg_list, dtype="uint8")

    print(np_arr)

    return np_arr

def pull_frame_from_cam(cam_IP):
    image = requests.get(f"http://{cam_IP}/getFrame")

    np_arr = np.array(bytearray(image.content), dtype="uint8")

    return np_arr
