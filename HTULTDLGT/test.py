import cv2
import numpy as np
import torch
from suport import *
from DeepSort.track_deepsort import *
from speed_calculator import *
import time
def result_tolistboxes(result):
    boxes = []
    for _, row in result.pandas().xyxy[0].iterrows():
        x1 = int(row['xmin'])
        y1 = int(row['ymin'])
        x2 = int(row['xmax'])
        y2 = int(row['ymax'])
        conf = round(float(row["confidence"]), 2)
        cls = row['class']
        name = row['name']
        boxes.append([x1, y1, x2, y2, conf, cls, name])
    return boxes

def Capture_Event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print(f"[{x},{y}]")

# video_writer = cv2.VideoWriter('00000000000000.avi', cv2.VideoWriter_fourcc(*'MJPG'), 30, (854,480))


#############################

video_path = 'E:/LuanVan/HTULTDLGT/Videos/CT.mp4'
video= cv2.VideoCapture(video_path)
csv_fpath = 'E:/LuanVan/HTULTDLGT/Videos/csv/'
# add_new_2lines(video_path, csv_fpath)
# add_new_roi(video_path, csv_fpath)
# lines = load_fromcsv('E:/LuanVan/HTULTDLGT/Videos/csv/CT_lines.csv') #Path(video_path).stem
# roi = load_fromcsv('E:/LuanVan/HTULTDLGT/Videos/csv/CT_roi.csv')

model = torch.hub.load('ultralytics/yolov5', 'custom', 'E:/LuanVan/HTULTDLGT/Model_Yolov5/100e.pt')
# model = torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True)
model.conf = 0.3
model.iou = 0.45
# tracker = DeepSORT_Tracker(roi)
frame_num = 1
# speed_calculator = SpeedCalculator(int(9), lines, 'E:/LuanVan/HTULTDLGT/Videos/csv/' + Path(video_path).stem + '_log.csv', 30)
name = ['xe buyt', 'xe container', 'xe cuu hoa', 'xe dap', 'xe hoi', 'xe may', 'xe tai', 'xe van']
offset = 10
s = 0
while True:
    ret, frame = video.read()
    if ret == False:
        break
    frame = cv2.resize(frame, (854,480))
    detect_results = model(frame)

    rs = result_tolistboxes(detect_results)
    for r in rs:
        x1, y1, x2, y2, conf, cls, name = r
        cvzone.putTextRect(frame, f' {str(name)}_{str(conf)} ', (max(0, x1),max(35,y1)), 
                                        scale=1, thickness=1, offset=0)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255,0,0), 1)
    '''
    results = tracker.update_track(detect_results, frame)
    for result in results:
        x1, y1, x2, y2, id, cls = result
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        w, h = x2 -x1, y2-y1
        cx = (x1+x2)//2
        cy = y2
        if cy < (lines[0][1] + offset) and cy > (lines[0][1] - offset):
            speed_calculator.add_SFrame(id, cx, cy, frame_num)
        if cy < (lines[2][1] + offset) and cy > (lines[2][1] - offset): 
            speed_calculator.add_EFrame(id, cx, cy, frame_num)               
        if cy > (lines[2][1] + offset):
            speed_calculator.update(id, cls)

        if id in speed_calculator.speeds:   #colorT = (255,0,0), colorR = (0,0,255)
            cvzone.putTextRect(frame, f' {str(speed_calculator.speeds[id])} Km/h', (max(0, x1),max(35,y1)), 
                                        scale=2, thickness=2, offset=0) #
        else: cvzone.putTextRect(frame, f' {int(id)}_{str(name[cls])}', (max(0, x1),max(35,y1)), 
                                        scale=1, thickness=1,offset=0)
        cv2.circle(frame, (cx, cy), 2, (255,0,0),2)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255,0,0), 1)
        # if cv2.pointPolygonTest(np.array(roi, np.int32), (cx, cy), False) >= 0:
            # if cy < (lines[0][1] + offset) and cy > (lines[0][1] - offset):
            #     speed_calculator.add_SFrame(id, cx, cy, frame_num)
            # if cy < (lines[2][1] + offset) and cy > (lines[2][1] - offset): 
            #     speed_calculator.add_EFrame(id, cx, cy, frame_num)               
            # if cy > (lines[2][1] + offset):
            #     speed_calculator.update(id, cls)

            # if id in speed_calculator.speeds:   #colorT = (255,0,0), colorR = (0,0,255)
            #     cvzone.putTextRect(frame, f' {str(speed_calculator.speeds[id])} Km/h', (max(0, x1),max(35,y1)), 
            #                             scale=2, thickness=2, offset=0) #
            # else: cvzone.putTextRect(frame, f' {int(id)}_{str(name[cls])}', (max(0, x1),max(35,y1)), 
            #                             scale=1, thickness=1,offset=0)
            # cv2.circle(frame, (cx, cy), 2, (255,0,0),2)
            # cv2.rectangle(frame, (x1, y1), (x2, y2), (255,0,0), 1)

    cv2.line(frame, (lines[0][0], lines[0][1]), (lines[1][0], lines[1][1]), (0,0,255), 2)
    cv2.line(frame, (lines[2][0], lines[2][1]), (lines[3][0], lines[3][1]), (0,0,255), 2)
    cv2.polylines(frame, [np.array(roi, np.int32)], True, (255,0,0))
    sf = frame
    cv2.rectangle(sf, (0, 0), (200, 100), (150,0,0), -1)
    cv2.putText(sf, f'Frame: {str(frame_num)}', (10, 20), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255),2)
    cv2.putText(sf, f'VTTB: {str(speed_calculator.avg_speed)} Km/h', (10, 45), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255),2)
    cv2.putText(sf, f'VTTBTT: {str(speed_calculator.cur_avg_speed)} Km/h', (10, 70), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255),2)
    cv2.putText(sf, speed_calculator.last, (10, 95), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255),2)
    # video_writer.write(frame)
    cv2.setMouseCallback('FRAME', Capture_Event)
    '''
    cv2.imshow('FRAME', frame)
    key = cv2.waitKey(s)
    frame_num+=1
    if key == ord('p'):
        s = 0
    if key == ord('o'):
        s = 1
    if key == ord('c'):
        t = time.time()
        ml = int(t * 1000)
        cv2.imwrite('E:/LuanVan/IMG/'+str(ml)+'.jpg', frame) 
    if key == ord('q'):
        break

video.release()
# video_writer.release()
cv2.destroyAllWindows()










    # boxes = result_tolistboxes(results)
    # for box in boxes:
    #     x, y, w, h, c, clas, name = box
    #     cv2.rectangle(frame, (x, y), (w, h), (255,0,0), 2)
    #     cv2.putText(frame, str(name), (x, y), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255),2)






# line = [[0, 0], [100, 100]]
# point = [51, 51]

# result = cv2.pointPolygonTest(np.array(line, np.int32), point, True)

# print(result)
# if result >= 0:
#     print("Điểm chạm vào đường thẳng")
# else:
#     print("Điểm không chạm vào đường thẳng")