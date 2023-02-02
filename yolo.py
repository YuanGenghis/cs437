import torch
import numpy as np
import cv2

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

img_np = cv2.imread('stop_sign_2.jpg')
img_np = cv2.resize(img_np, (320, 240))
img_np = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)

results = model(img_np)

results.print()
results.show()
