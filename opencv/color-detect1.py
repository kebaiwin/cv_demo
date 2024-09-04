import cv2
import numpy as np
def empty(x):
    print(x)
img = cv2.imread('data/apple.jpg')

cap = cv2.VideoCapture(0)
# 创建一个命名窗口
cv2.namedWindow('trackbar', cv2.WINDOW_AUTOSIZE)
# 创建色调滑动条 控制最小色调值
cv2.createTrackbar('hue-min', 'trackbar', 0, 180, empty)
# 创建色调滑动条 控制最大色调值
cv2.createTrackbar('hue-max', 'trackbar', 180, 180, empty)
# 创建饱和度滑动条 最小值
cv2.createTrackbar('sat-min', 'trackbar', 0, 255, empty)
# 创建饱和度滑动条 最大值
cv2.createTrackbar('sat-max', 'trackbar', 255, 255, empty)
# 创建亮度滑动条 控制最小亮度
cv2.createTrackbar('val-min', 'trackbar', 0, 255, empty)
# 创建亮度滑动条 控制最大亮度
cv2.createTrackbar('val-max', 'trackbar', 255, 255, empty)

while True:
    ret, img = cap.read()
    img =cv2.resize(img,(500,500))
    # brg to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)



    h_min = cv2.getTrackbarPos('hue-min', 'trackbar')
    h_max = cv2.getTrackbarPos('hue-max', 'trackbar')
    s_min = cv2.getTrackbarPos('sat-min', 'trackbar')
    s_max = cv2.getTrackbarPos('sat-max', 'trackbar')
    val_min = cv2.getTrackbarPos('val-min', 'trackbar')
    val_max = cv2.getTrackbarPos('val-max', 'trackbar')
    # 创建最小颜色范围
    lower = np.array([h_min, s_min, val_min])
    # 创建最大颜色范围
    upper = np.array([h_max, s_max, val_max])
    print('最小范围',lower,'最大范围', upper)
    mask = cv2.inRange(hsv, lower, upper)
    mask_contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for mask_contour in mask_contours:
        if cv2.contourArea(mask_contour) > 500:
            x, y, w, h = cv2.boundingRect(mask_contour)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)  # drawing rectangle

    result = cv2.bitwise_and(img, img, mask=mask)
    cv2.imshow('mask', mask)
    cv2.imshow('trackbar',result)
    cv2.imshow('img', img)
    cv2.waitKey(1)
