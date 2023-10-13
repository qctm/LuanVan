import cv2
import torch
import numpy as np
import time
from tracking_centroid import *
from speed import *

# Video:
video = cv2.VideoCapture("D:/LuanVan/Videos/vid480.mp4")

# Load mo hinh
model = torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True)
# model = torch.hub.load('ultralytics/yolov5', 'custom', path='D:/LuanVan/Custom_Model/exp3-5n-50e/weights/best.pt')

# Tracker (centroid)
tracker = Tracker_Centroid()

# def mousePos(event, x, y, flags, param):
#     if event == cv2.EVENT_MOUSEMOVE:
#         mp = [x, y]
#         print(mp)
# cv2.namedWindow('FRAME')
# cv2.setMouseCallback('FRAME', mousePos)

#--- DEFINE ---
avg_fps = 0.0
frame_num = 0
count = 0
countline_y1 = 200
countline_y2 = 350
offset = 10
xe_vao = {}
counter = []
xe_ids = {}
sp = SpeedCal()

while True:
    ret, frame = video.read()
    
    start = time.time()
    results = model(frame)
    end = time.time()
    frame_num = frame_num + 1
    fps = 1.0/(end-start)
    avg_fps += fps
    vfps = avg_fps/frame_num

    # print("Average FPS: %.1f" %vfps)
    cv2.line(frame, (0, countline_y1), (852, countline_y1), (0, 0, 255), 2)
    cv2.line(frame,(0, countline_y2),(852, countline_y2), (0,0,255), 2)
    
    bbox_list = []
    
    for index, row in results.pandas().xyxy[0].iterrows():
        x1 = int(row['xmin'])
        y1 = int(row['ymin'])
        x2 = int(row['xmax'])
        y2 = int(row['ymax'])
        if row['class'] == 2 or row['class'] == 3 or row['class'] == 5 or row['class'] == 7:
            bbox_list.append([x1, y1, x2, y2])
    box_id = tracker.tracking(bbox_list)
    for bid in box_id:
        x, y, w, h, id = bid
        cx = (x+w)//2
        cy = (y+h)//2
        cv2.rectangle(frame, (x, y), (w, h), (255,0,0),2)
        cv2.circle(frame, (cx, cy), 2, (255,0,0),2)
        cv2.putText(frame, str(id), (cx, cy), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255),2)
        if countline_y1<(cy+offset) and countline_y1>(cy-offset):
            # xe_vao[id] = cy
            xe_vao[id] = time.time()
            sp.add(id, cx, cy, time.time())
        if id in xe_vao:
            if countline_y2<(cy+offset) and countline_y2>(cy-offset):        
                if id not in sp.done:
                    vt = sp.calcu(id, cx, cy, time.time(), vfps)
                    cv2.putText(frame, str(round(vt,2)), (x, y), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255),2)
                    print(vt)
                if counter.count(id)==0:
                    counter.append(id)
                    
                    
    # print(box_id)
    cnt = len(sorted(set(counter),key=counter.index))
    
    cv2.putText(frame, str(cnt), (100, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255),3)    
    cv2.imshow('FRAME', frame) 
    key = cv2.waitKey(1)
    if key == ord('q'): # press q to stop
        break
    # ret, frame = video.read()
    
video.release()
cv2.destroyAllWindows()







# 阮國沈