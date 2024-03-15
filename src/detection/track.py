import cv2
import os
import json

import numpy as np
import multiprocessing as mp

from ultralytics import YOLO
from pull_frame import pull_frame_from_cam

STREAM_FPS = 10
CNN_MIN_CONFIDENCE = 0.55

def ESP32_cam_pull(cam_IP):
    frame = pull_frame_from_cam(cam_IP)

    decoded_image = cv2.imdecode(frame, cv2.IMREAD_COLOR)

    return decoded_image

def process_camera_view(cam_IP):
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
        key = cv2.waitKey(1000 // STREAM_FPS)

        if key == ord('e'):
            break
    
    cv2.destroyAllWindows()

def main():
    conf_fl = open("./configs/conf.json")
    ips = json.load(conf_fl)

    procs = []

    process_camera_view(ips[0])

    for ip in ips:
        p = mp.Process(target=process_camera_view, args=(ip,))
        procs.append(p)
'''
    for p in procs:
        p.start()
        p.join()
'''

if __name__ == "__main__":
    main()

#process_camera_view()
