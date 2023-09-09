import torch
import cv2
from ultralytics import YOLO
import cvzone
from sort import *
import numpy as np

def result2boxes(result):
    boxes = []
    for _, row in result.pandas().xyxy[0].iterrows():
        x1 = int(row['xmin'])
        y1 = int(row['ymin'])
        x2 = int(row['xmax'])
        y2 = int(row['ymax'])
        conf = round(float(row["confidence"]), 2)
        cls = row['class']
        name = row['name']
        if row['class'] == 2 or row['class'] == 3 or row['class'] == 5 or row['class'] == 7:
            boxes.append([x1, y1, x2, y2, conf, cls, name])
    return boxes


# Video:
video = cv2.VideoCapture("D:/LuanVan/Videos/vid480p.mp4")

# Load mo hinh
model = torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True)
# model = YOLO("yolov5n.pt")

tracker = Sort(max_age=20, min_hits=2, iou_threshold=0.3)

while True:
    ret, frame = video.read()
        
    results = model(frame)
    boxes = result2boxes(results)
    
    detections = np.empty((0, 5))
    for box in boxes:
        x1, y1, x2, y2, conf, cls, name = box
        w, h = x2 -x1, y2-y1
        # cvzone.cornerRect(frame, (x1, y1, w, h), l=0, rt=5)
        # cvzone.putTextRect(frame, f'{name} {conf}', (max(0, x1),max(35,y1)), 
        #                         scale=1, thickness=1, offset=0)
        currentArray = np.array([x1, y1, x2, y2, conf])
        detections = np.vstack((detections, currentArray))
    
    resultsTracker = tracker.update(detections)
    
    for result in resultsTracker:
        x1, y1, x2, y2, id = result
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        w, h = x2 -x1, y2-y1
        cvzone.cornerRect(frame, (x1, y1, w, h), l=0, rt=2, colorR=(255,0,0))
        cvzone.putTextRect(frame, f' {int(id)}', (max(0, x1),max(35,y1)), 
                                scale=1, thickness=1, offset=0)
    
    cv2.imshow('FRAME', frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
        
video.release()
cv2.destroyAllWindows()



#YOLov8
# for result in resultsDetect:
    #     boxes = result.boxes
    #     for box in boxes:
    #         x1, y1, x2, y2 = box.xyxy[0]
    #         x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
    #         w, h = x2 -x1, y2-y1
    #         cvzone.cornerRect(frame, (x1, y1, w, h))