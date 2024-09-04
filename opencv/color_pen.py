#颜色检测以及跟踪 实现虚拟画笔
import cv2
import numpy as np
# 绿色hsv取值范围
green_lower = np.array([34, 59 ,  160])
green_upper = np.array([88, 255, 255])
#蓝色hsv取值范围
blue_lower = np.array([102, 255 , 38])
blue_upper = np.array([151, 255, 255])
# 设置画笔的颜色
pen_color =[[0,255,0],[255,0,0]]

# 记录颜色移动的轨迹 x,y,color
pen_coord =[]
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, green_lower, green_upper)
    contours,hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) >500:
            x, y, w, h = cv2.boundingRect(contour)
            # cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 5)
            pen_coord.append([x+w//2,y,pen_color[0]])
            cv2.circle(frame,(x+w//2,y),10,pen_color[0],-1)
    mask = cv2.inRange(hsv, blue_lower, blue_upper)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) > 500:
            x, y, w, h = cv2.boundingRect(contour)
            # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 5)
            pen_coord.append([x + w // 2, y, pen_color[1]])
            cv2.circle(frame, (x + w // 2, y), 10, pen_color[1], -1)
    for e in pen_coord:
        cv2.circle(frame, (e[0], e[1]), 8, e[2], -1)

    # 创建橡皮擦
    if cv2.waitKey(1) ==ord('c'):
        pen_coord.clear()
    cv2.imshow('frame', frame)
    cv2.waitKey(1)