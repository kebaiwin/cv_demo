#颜色检测以及跟踪
import cv2
import numpy as np
# 绿色hsv取值范围
green_lower = np.array([37, 108 ,  0])
green_upper = np.array([68, 255, 181])
#蓝色hsv取值范围
blue_lower = np.array([102, 255 , 38])
blue_upper = np.array([151, 255, 255])

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, green_lower, green_upper)
    contours,hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) >200:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 5)
    mask = cv2.inRange(hsv, blue_lower, blue_upper)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) > 200:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 5)

    cv2.imshow('frame', frame)
    cv2.waitKey(1)