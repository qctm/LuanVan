import cv2
video = cv2.VideoCapture("D:/LuanVan/Data/vid480p.mp4")

def handle_left_click(event, x, y, flags, points):
    if event == cv2.EVENT_LBUTTONDOWN and len(points)<=3:
        points.append([x, y])

def draw_lines(frame, points):
    for point in points:
        frame = cv2.circle(frame, (point[0], point[1]), 5, (0,0,255), -1)

    if len(points) == 4:
        pointA, pointB, pointC, pointD = points
        #line 1
        cv2.line(frame, (pointA[0], pointA[1]), (pointB[0], pointA[1]), (100, 100, 255), 2)
        #line 1
        cv2.line(frame, (pointC[0], pointC[1]), (pointD[0], pointC[1]), (14, 200, 255), 2)
    return frame

line_1 = []
line_2 = []
points = []
while True:
    ret, frame = video.read()
    # frame = cv2.resize(frame, (854, 480), interpolation = cv2.INTER_LINEAR)
    print(points)
    frame = draw_lines(frame, points)
    
    if ret:
        cv2.imshow("FRAME", frame)
    else:
        print('no video')
        video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue
    
    cv2.setMouseCallback('FRAME', handle_left_click, points)
    
    key = cv2.waitKey(30)
    if key == ord('r'):
        points = []
    if key == ord('c'):
        break
    
video.release()
cv2.destroyAllWindows()