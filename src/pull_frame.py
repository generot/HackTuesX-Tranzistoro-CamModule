import requests
import numpy as np

def pull_frame_from_cam(cam_IP):
    image = requests.get(f"http://{cam_IP}/getFrame")

    image_bytearr = bytes(image.content)
    jpeg_list = list(image_bytearr)

    np_arr = np.array(jpeg_list, dtype="uint8")

    return np_arr
