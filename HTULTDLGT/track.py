import torch
import cv2
# from ultralytics import YOLO
import cvzone
from UI_TEST.Sort.sort import *
import numpy as np
from suport import *
from UI_TEST.speed_calculator import *
import time

import argparse
import os
import platform
import shutil
import time
from pathlib import Path
import cv2
import cvzone
import torch
import torch.backends.cudnn as cudnn

from yolov5.models.experimental import attempt_load
from yolov5.utils.downloads import attempt_download
from yolov5.models.common import DetectMultiBackend
from yolov5.utils.dataloaders import LoadImages, LoadStreams
from yolov5.utils.general import (LOGGER, check_img_size, non_max_suppression, scale_coords, 
                                  check_imshow, xyxy2xywh, increment_path)
from yolov5.utils.torch_utils import select_device, time_sync
from yolov5.utils.plots import Annotator, colors
from DeepSort.deep_sort.utils.parser import get_config
from DeepSort.deep_sort.deep_sort import DeepSort

import sys
# sys.path.insert(0, './DeepSort')


class Track():
    def __init__(self, yolomodelname, trackername):
        self.detector = self.load_model(yolomodelname)
        self.tracker = self.load_tracker(trackername)
        self.tracker_name = trackername

    def load_model(self, name):
        model = torch.hub.load('ultralytics/yolov5', 'custom', 'E:/LuanVan/UI_TEST/best.pt')
        return model
    
    def parse_opt(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--yolo_model', nargs='+', type=str, default='E:/TEST/0929/DeepSort/best.pt', help='model.pt path(s)')
        parser.add_argument('--deep_sort_model', type=str, default='osnet_x0_25')
        parser.add_argument('--source', type=str, default='E:/TEST/0929/DeepSort/videos/th.mp4', help='source')  # file/folder, 0 for webcam
        parser.add_argument('--output', type=str, default='inference/output', help='output folder')  # output folder
        parser.add_argument('--imgsz', '--img', '--img-size', nargs='+', type=int, default=[480, 852], help='inference size h,w')
        parser.add_argument('--conf-thres', type=float, default=0.5, help='object confidence threshold')
        parser.add_argument('--iou-thres', type=float, default=0.5, help='IOU threshold for NMS')
        parser.add_argument('--fourcc', type=str, default='mp4v', help='output video codec (verify ffmpeg support)')
        parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
        parser.add_argument('--show-vid', action='store_false', help='display tracking video results')
        parser.add_argument('--save-vid', action='store_false', help='save video tracking results')
        parser.add_argument('--save-txt', action='store_true', help='save MOT compliant results to *.txt')
        # class 0 is person, 1 is bycicle, 2 is car... 79 is oven
        parser.add_argument('--classes', nargs='+', type=int, default=4, help='filter by class: --class 0, or --class 16 17')
        parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
        parser.add_argument('--augment', action='store_true', help='augmented inference')
        parser.add_argument('--evaluate', action='store_true', help='augmented inference')
        parser.add_argument("--config_deepsort", type=str, default="E:/TEST/0929/DeepSort/deep_sort/configs/deep_sort.yaml")
        parser.add_argument("--half", action="store_true", help="use FP16 half-precision inference")
        parser.add_argument('--visualize', action='store_true', help='visualize features')
        parser.add_argument('--max-det', type=int, default=1000, help='maximum detection per image')
        parser.add_argument('--dnn', action='store_true', help='use OpenCV DNN for ONNX inference')
        # parser.add_argument('--project', default=ROOT / 'runs/track', help='save results to project/name')
        parser.add_argument('--name', default='exp', help='save results to project/name')
        parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
        opt = parser.parse_args()
        opt.imgsz *= 2 if len(opt.imgsz) == 1 else 1  # expand
        return opt
    
    def load_tracker(self, name):
        if name == 'SORT':
            print("Load SORT")
            self.tracker = Sort(max_age=20, min_hits=2, iou_threshold=0.3)
        if name == 'DeepSORT':
            print("Load DeepSORT")
            opt = self.parse_opt()
            cfg = get_config()
            cfg.merge_from_file(opt.config_deepsort)
            self.tracker = DeepSort(opt.deep_sort_model,
                                max_dist=cfg.DEEPSORT.MAX_DIST,
                                max_iou_distance=cfg.DEEPSORT.MAX_IOU_DISTANCE,
                                max_age=cfg.DEEPSORT.MAX_AGE, n_init=cfg.DEEPSORT.N_INIT, nn_budget=cfg.DEEPSORT.NN_BUDGET,
                                )

    def track_SORT(self, image):
        results = self.model(image)
        boxes = result_tolistboxes(results, 0)
        detections = np.empty((0, 5))
        for box in boxes:
            x1, y1, x2, y2, conf, cls, name = box
            currentArray = np.array([x1, y1, x2, y2, conf])
            detections = np.vstack((detections, currentArray))
    
        tracks = self.tracker.update(detections)
        for track in tracks:
            x1, y1, x2, y2, id = track
            x1, y1, x2, y2, id = int(x1), int(y1), int(x2), int(y2), int(id)
            w, h = x2 -x1, y2-y1
            cx = (x1+x2)//2
            cy = (y1+y2)//2

            cv2.circle(image, (cx, cy), 2, (255,0,0),2)
            cvzone.cornerRect(image, (x1, y1, w, h), l=0, rt=2, colorR=(255,0,0))
            cvzone.putTextRect(image, f' {int(id)}', (max(0, x1),max(35,y1)), 
                                    scale=1, thickness=1, offset=0)
        return image
    
    def track_DeepSORT(self, frame):
        results = self.detector(frame)
        r = results.xyxy[0]
        xywhs = xyxy2xywh(r[:, 0:4])
        confs = r[:, 4]
        clss = r[:, 5]
        outputs = self.tracker.update(xywhs.cpu(), confs.cpu(), clss.cpu(), frame)
        for output in outputs:
            x1, y1, x2, y2, track_id, class_id = output
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255,0,0),2)
            cvzone.putTextRect(frame, f' {int(track_id)}{str(self.detector.names[class_id])}', (max(0, x1),max(35,y1)), 
                                scale=1, thickness=1, offset=0)         
        return frame

    def detect(self, image):
        # sys.path.insert(0, './DeepSort')
        print("decting")
        if self.tracker_name == 'DeepSORT':
            return self.track_DeepSORT(image)
        if self.tracker_name == 'SORT':
            return self.track_SORT(image)