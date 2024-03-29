import cv2
import os
import json
import requests

import numpy as np
import multiprocessing as mp

from ultralytics import YOLO
from pull_frame import pull_frame_from_cam

API_KEY = ""

STREAM_FPS = 10
CNN_MIN_CONFIDENCE = 0.55

APP_BACKEND = "192.168.220.133"

def send_attendance_data(cam_ID, dt_count):
    resp = {
        "cameraId": int(cam_ID),
        "count": dt_count,
        "apiKey": API_KEY
    }

    res = requests.post(f"https://{APP_BACKEND}:2999/api/facilities/attendance", data=resp, verify=False)
    print(res)

def ESP32_cam_pull(cam_IP):
    frame = pull_frame_from_cam(cam_IP)

    decoded_image = cv2.imdecode(frame, cv2.IMREAD_COLOR)

    return decoded_image

def process_camera_view(cam_IP, cam_ID):
    net = YOLO("../models/yolov8/yolov8n.pt")

    while True:
        frame = ESP32_cam_pull(cam_IP)

        results = net.track(frame, 
                            verbose=False, 
                            conf=CNN_MIN_CONFIDENCE, 
                            device="cpu", 
                            persist=True,
                            classes=0)

        annotated = results[0].plot()
        detection_count = len(results[0])

        cv2.putText(annotated, f"Person count: {detection_count}", (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Image", annotated)
        send_attendance_data(cam_ID, detection_count)

        key = cv2.waitKey(1000 // STREAM_FPS)

        if key == ord('e'):
            break
    
    cv2.destroyAllWindows()

def main():
    conf_fl = open("./configs/conf.json", "r+")
    conf = json.load(conf_fl)

    global API_KEY
    API_KEY = conf["api_key"]

    procs = []

    for i, ip in enumerate(conf["ip_addresses"]):
        assigned_id = requests.get(f"http://{ip}/assignId?assigned_id={i+1}").text

        print(assigned_id)

        conf["ip_addresses"][i] = (ip, assigned_id)

        p = mp.Process(target=process_camera_view, args=(ip, assigned_id))
        procs.append(p)

    pair = conf["ip_addresses"][0]

    process_camera_view(pair[0], pair[1])

'''
    for p in procs:
        p.start()
        p.join()
'''

if __name__ == "__main__":
    main()
