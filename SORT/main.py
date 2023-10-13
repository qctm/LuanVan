import torch
import cv2
# from ultralytics import YOLO
import cvzone
from sort import *
import numpy as np
from suport import *
from speed import *
from count import *
import time

# Video Input
video_path = "E:/LuanVan/Videos/th.mp4"
video = loadVideo(video_path)
# Load mo hinh
# model = torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True)
model = torch.hub.load('ultralytics/yolov5', 'custom', 'D:/LuanVan/SORT/best.pt') #base: yolov5n
# SORT
tracker = Sort(max_age=20, min_hits=2, iou_threshold=0.3)

add_new_2lines(video_path)
# pointA, pointB, pointC, pointD = load_indexfromcsv(video_path)
# y_line1, y_line2 = pointA[1], pointC[1]

# add_new_roi(video_path)
area = load_indexfromcsv(Path(video_path).stem + '_roi.csv')
# area = [pointA, pointB, pointD, pointC]

colorR = (0,0,255)
f = 0
offset = 10
counter = []
counter_1 = []
speed = SpeedCal(100, 3)
xevao = {}
frame_num = 1
avg_fps = 0

while True:
    ret, frame = video.read()
    if not ret:
        break
    start = time.time() # start time
    results = model(frame)
    boxes = result_tolistboxes(results, 0)
    detections = np.empty((0, 5))

    cv2.polylines(frame, [np.array(area, np.int32)], True, (0,255,0))

    for box in boxes:
        x1, y1, x2, y2, conf, cls, name = box
        currentArray = np.array([x1, y1, x2, y2, conf])
        detections = np.vstack((detections, currentArray))
    
    resultsTracker = tracker.update(detections)
    # print(resultsTracker)
    end = time.time()
    fps = 1.0/(end-start)
    avg_fps += fps
    vfps = avg_fps/frame_num
    frame_num = frame_num + 1
    for result in resultsTracker:
        x1, y1, x2, y2, id = result
        x1, y1, x2, y2, id = int(x1), int(y1), int(x2), int(y2), int(id)
        w, h = x2 -x1, y2-y1
        cx = (x1+x2)//2
        cy = (y1+y2)//2
        cv2.circle(frame, (cx, cy), 2, (255,0,0),2)
        cvzone.cornerRect(frame, (x1, y1, w, h), l=0, rt=2, colorR=(255,0,0))
        cvzone.putTextRect(frame, f' {int(id)}', (max(0, x1),max(35,y1)), 
                                scale=1, thickness=1, offset=0)

        if cv2.pointPolygonTest(np.array(area, np.int32), (cx, cy), False) >= 0:
            counter_1.append(id)
            t = time.time()
            speed.add(id, cx, cy, t)
        if (cv2.pointPolygonTest(np.array(area, np.int32), (cx, cy), False) <= 0) and (id in speed.vehicle_dict.keys()):
            speed.update(id, vfps)
            cv2.polylines(frame, [np.array(area, np.int32)], True, (0,0,255),2)
        # kiem tra neu ROI trong doi tuong:
    
    # cv2.line(frame, (pointA[0], pointA[1]), (pointB[0], pointA[1]), colorR, 2)
    # cv2.line(frame, (pointC[0], pointC[1]), (pointD[0], pointC[1]), colorR, 2)
    
    # cnt = len(sorted(set(counter),key=counter.index))
    # cv2.putText(frame, str(cnt), (100, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255),3)
    cv2.putText(frame, 'FPS: ' + str(round(vfps)), (50, 90), cv2.FONT_HERSHEY_PLAIN, 3, colorR,3)
    cv2.putText(frame, 'AVG SPEED: ' + str(round(speed.avg_speed, 2)) + "Km/h", (50, 150), cv2.FONT_HERSHEY_PLAIN, 3, colorR,3)
    cv2.imshow('FRAME', frame)
    f+=1
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
   
video.release()
cv2.destroyAllWindows()

print('AVG SPEED: '+str(round(speed.avg_speed)))