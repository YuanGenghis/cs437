import torch
import numpy as np
import cv2
import time
import threading
import matplotlib.pyplot as plt

from IPython import embed

class YOLODetector:
    def __init__(self):
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        self.buffer_lock = threading.Lock()
        self.valid = False
    
    def run(self):
        self.thread = threading.Thread(target=self.run_)
        self.thread.start()
    
    def is_valid(self):
        return self.valid
    
    def get_latest_seen_objects(self):
        self.buffer_lock.acquire()
        assert self.valid
        ret = self.name_arr.copy()
        self.buffer_lock.release()
        return list(ret)

    def get_latest_prediction_viz(self):
        assert self.valid

        self.buffer_lock.acquire()
        viz = self.img_np.copy()
        conf_tmp = self.conf_arr.copy()
        bbox_tmp = self.bbox_arr.copy()
        name_tmp = self.name_arr.copy()
        self.buffer_lock.release()
        for i in range(len(conf_tmp)):
            if conf_tmp[i] > 0.5:
                viz = cv2.rectangle(viz, (bbox_tmp[i][0], bbox_tmp[i][1]), (bbox_tmp[i][2], bbox_tmp[i][3]), (0, 255, 0), 2)
                viz = cv2.putText(viz, name_tmp[i], (bbox_tmp[i][0], bbox_tmp[i][1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

        return viz

    def run_(self):
        try:
            cap = cv2.VideoCapture(0)
            while True:
                ret, img_np = cap.read()
                if not ret:
                    raise Exception('Failed to read from camera.')

                # Preprocess & detect
                img_np = self.preprocess_(img_np)
                conf_arr, bbox_arr, name_arr = self.detect_(img_np)

                # Update shared storage
                self.buffer_lock.acquire()
                self.img_np = img_np.copy()
                self.conf_arr = conf_arr.copy()
                self.bbox_arr = bbox_arr.copy()
                self.name_arr = name_arr.copy()
                if not self.valid:
                    self.valid = True
                self.buffer_lock.release()
        finally:
            print('Stopping camera...')
            cap.release()
    
    def preprocess_(self, img):
        img = cv2.resize(img, (320, 240))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img

    def detect_(self, img):
        results = self.model(img)

        conf_arr = results.pandas().xyxy[0]['confidence'].to_numpy()
        bbox_arr = results.pandas().xyxy[0][['xmin', 'ymin', 'xmax', 'ymax']].to_numpy().astype(int)
        name_arr = results.pandas().xyxy[0]['name'].to_numpy()

        return conf_arr, bbox_arr, name_arr

if __name__ == '__main__':
    yolo = YOLODetector()
    yolo.run()

    while True:
        if yolo.is_valid():
            viz = yolo.get_latest_prediction_viz()
            viz = cv2.cvtColor(viz, cv2.COLOR_RGB2BGR)
            cv2.imshow('YOLO', viz)
            cv2.waitKey(1)
