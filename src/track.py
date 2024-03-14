import cv2
import os
import numpy as np

from ultralytics import YOLO
from pull_frame import pull_frame_from_cam

CAM_IP = "192.168.1.85"

FPS = 60
STREAM_FPS = 20

CNN_MIN_CONFIDENCE = 0.3

def ESP32_cam_pull():
    frame = pull_frame_from_cam(CAM_IP)

    decoded_image = cv2.imdecode(frame, cv2.IMREAD_COLOR)

    return decoded_image

def process_camera_view():
    net = YOLO("../models/yolov8/yolov8n.pt")

    while True:
        frame = ESP32_cam_pull()

        if cv2.waitKey(1000 // STREAM_FPS) == ord("e"):
            break

        results = net.track(frame, 
                            verbose=False, 
                            conf=CNN_MIN_CONFIDENCE, 
                            device="cpu", 
                            persist=True,
                            classes=0)

        annotated = results[0].plot()

        cv2.imshow("Image", annotated)
    
    cv2.destroyAllWindows()

def main():
    #video = cv2.VideoCapture("./sample_florida1.mp4")
    video = cv2.VideoCapture(0)
    net = YOLO("../models/yolov8/yolov8n.pt")

    while video.isOpened():
        ret, frame = video.read()

        frame = frame[100:600]

        if ret == False:
            print("An error occured when pulling a frame...")
            break

        if cv2.waitKey(1000 // FPS) == ord('e'):
            break

        results = net.track(frame, verbose=False, conf=CNN_MIN_CONFIDENCE, device="cpu", persist=True, classes=0)

        annotated = results[0].plot()
        detection_count = len(results[0])

        cv2.putText(annotated, f"Person count: {detection_count}", (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Video", annotated)

    video.release()
    cv2.destroyAllWindows()

#process_camera_view()
main()
