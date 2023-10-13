import torch
import cv2
# from ultralytics import YOLO
import cvzone
import numpy as np
import time
from deep_sort.utils.parser import get_config
from deep_sort.deep_sort import DeepSort
from suport import *

cfg = get_config()
cfg.merge_from_file("./Yolov5_DeepSort_Pytorch/deep_sort/configs/deep_sort.yaml")
deepsort = DeepSort('osnet_x0_25',
                    max_dist=cfg.DEEPSORT.MAX_DIST,
                    max_iou_distance=cfg.DEEPSORT.MAX_IOU_DISTANCE,
                    max_age=cfg.DEEPSORT.MAX_AGE, n_init=cfg.DEEPSORT.N_INIT, nn_budget=cfg.DEEPSORT.NN_BUDGET,
                    use_cuda=True)
    

video_path = "E:/TEST/0929/Yolov5_DeepSort_Pytorch/videos/th.mp4"
video = cv2.VideoCapture(video_path)
model = torch.hub.load('ultralytics/yolov5', 'custom', 'E:/TEST/0929/Yolov5_DeepSort_Pytorch/best.pt')

while True:
    ret, frame = video.read()
    if not ret:
        break
    results = model(frame)
    boxes = []
    for _, row in results.pandas().xyxy[0].iterrows():
        x1 = (row['xmin'])
        y1 = (row['ymin'])
        x2 = (row['xmax'])
        y2 = (row['ymax'])
        conf = round(float(row["confidence"]), 2)
        cls = row['class']
        name = row['name']
        boxes.append([x1, y1, x2, y2, conf, cls, name])
    
    # boxes = result_tolistboxes(results, 0)


    # for box in boxes:
    #     x1, y1, x2, y2, conf, cls, name = box
    #     x = (x1+x2)/2
    #     y = (y1+y2)/2
    #     w = x2-x1
    #     h = y2-y1
    #     xywhs = (x, y, w, h)
    #     print('1')
    #     outputs = deepsort.update(xywhs, conf, cls, frame)

    #     print(outputs)
    
    cv2.imshow('FRAME', frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
   
video.release()
cv2.destroyAllWindows()