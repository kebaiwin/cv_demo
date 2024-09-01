# 轮廓检测
import cv2
img = cv2.imread('data/shape.png')
# 彩色图片转换为灰色图片
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# 图像边缘检测
canny = cv2.Canny(gray, 100, 200)
# 轮廓检测
contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
for contour in contours:
    # 函数会在原图img上以蓝色的线条(0, 255, 0) 画出所有找到的轮廓，线宽为3。
    cv2.drawContours(img, contour, -1, [255, 0, 0], 3)
    # 计算轮廓面积
    area = cv2.contourArea(contour)
    if area >200:
        # 计算轮廓长度
        length = cv2.arcLength(contour, True)
        epsilon = 0.02 * length
        # 计算近似多边形
        approx = cv2.approxPolyDP(contour, epsilon, True)
        corners = len(approx)
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 4)
        if corners == 3:
            # 三个点 三角形
            cv2.putText(img, 'triangle', (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
        elif corners == 4:
            # 四个点 矩形
            cv2.putText(img, 'rectangle', (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0., 0, 255))
        elif corners == 5:
            # 五个点 五边形
            cv2.putText(img, 'pentagon', (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
        elif corners >5:
            # 大于5个点 圆形
            cv2.putText(img, 'circle', (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
cv2.imshow("img", img)
cv2.waitKey(0)