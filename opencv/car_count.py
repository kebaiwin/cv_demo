import cv2
import numpy as np

# 设置最小检测区域的宽度和高度（以像素为单位）
largura_min = 80  # 最小矩形宽度
altura_min = 80  # 最小矩形高度

# 设置检测线的容差范围
offset = 6  # 允许的像素误差

# 设置计数线的位置（以像素为单位）
pos_linha = 550  # 计数线的位置

# 初始化检测中心点的列表
detec = []
# 车辆计数器
carros = 0


# 定义一个函数用于获取矩形的中心点
def pega_centro(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx, cy


# 打开视频文件
cap = cv2.VideoCapture('data/video.mp4')

# 创建背景减法器对象，用于前景检测
subtracao = cv2.bgsegm.createBackgroundSubtractorMOG()

# 使用一个无限循环处理每一帧视频
while True:
    # 读取视频的每一帧
    ret, frame = cap.read()
    if ret is not True:
        break

    # 将图像转换为灰度图
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 对灰度图应用高斯模糊，去除噪声
    blur = cv2.GaussianBlur(gray, (3, 3), 5)

    # 对模糊处理后的图像应用背景减法
    img_sub = subtracao.apply(blur)

    # 对背景减法后的图像进行膨胀操作，填充前景中的空洞
    dilat = cv2.dilate(img_sub, np.ones((5, 5)))

    # 获取形态学操作的结构元素
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

    # 对膨胀后的图像进行形态学闭操作，进一步填充前景中的空洞
    dilatada = cv2.morphologyEx(dilat, cv2.MORPH_CLOSE, kernel)
    dilatada = cv2.morphologyEx(dilatada, cv2.MORPH_CLOSE, kernel)

    # 查找前景图像中的轮廓
    contorno, h = cv2.findContours(dilat, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 在原始帧上绘制计数线
    cv2.line(frame, (25, pos_linha), (1200, pos_linha), (255, 127, 0), 3)

    # 遍历每一个轮廓
    for (i, c) in enumerate(contorno):
        # 获取每个轮廓的外接矩形
        (x, y, w, h) = cv2.boundingRect(c)
        # 验证外接矩形是否大于最小宽度和高度
        validar_contorno = (w >= largura_min) and (h >= altura_min)

        # 如果验证不通过，则跳过该轮廓
        if not validar_contorno:
            continue

        # 在原始帧上绘制外接矩形
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # 获取外接矩形的中心点
        centro = pega_centro(x, y, w, h)

        # 将中心点添加到检测列表中
        detec.append(centro)

        # 在原始帧上绘制中心点
        cv2.circle(frame, centro, 4, (0, 0, 255), -1)

        # 遍历检测列表中的中心点
        for (x, y) in detec:
            # 检查中心点是否穿过计数线
            if y < (pos_linha + offset) and y > (pos_linha - offset):
                # 如果穿过，则计数器加1
                carros += 1
                # 在原始帧上重新绘制计数线
                cv2.line(frame, (25, pos_linha), (1200, pos_linha), (0, 127, 255), 3)
                # 从检测列表中移除该中心点
                detec.remove((x, y))
                # 打印车辆计数
                print("检测到的车辆数量 : " + str(carros))

    # 在原始帧上显示车辆计数
    cv2.putText(frame, "car count : " + str(carros), (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)

    # 显示原始视频帧
    cv2.imshow("img", frame)

    # 显示前景检测后的图像
    # cv2.imshow("check", dilatada)

    # 如果按下ESC键，则退出循环
    if cv2.waitKey(1) == 27:
        break

# 释放资源
cv2.destroyAllWindows()
cap.release()