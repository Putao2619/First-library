from email.mime import image
from http.client import ImproperConnectionState
from inspect import Parameter
from tkinter import Frame
import cv2 as cv
import numpy as np
import mediapipe as mp
import time
from numpy import linalg
# from utils import Jdict
import json
import os,sys
handDemo = 0



sys.path.append("./task2")
sys.path.append("./train")
sys.path.append("./train/task2")

#if os.path.isfile("./train/task2/handDemo.so"):
#        from handDemo import detect_hands_gesture,roi
#        print("handDemo have")

# 视频设备号
DEVICE_NUM = 0

# 手指检测
# point1-手掌0点位置，point2-手指尖点位置，point3手指根部点位置
# def finger_stretch_detect(point1, point2, point3):
#     result = 0
#     # 计算向量的L2范数
#     dist1 = np.linalg.norm((point2 - point1), ord=2)
#     dist2 = np.linalg.norm((point3 - point1), ord=2)
#     if dist2 > dist1:
#         result = 1
#     return result


#计算fps用到的参数pTime初始化
pTime = 0
# 接入USB摄像头时，注意修改cap设备的编号
# cap = cv.VideoCapture(DEVICE_NUM)
# 加载手部检测函数
mpHands = mp.solutions.hands
hands = mpHands.Hands()
# 加载绘制函数，并设置手部关键点和连接线的形状、颜色
mpDraw = mp.solutions.drawing_utils
handLmsStyle = mpDraw.DrawingSpec(color=(0, 0, 255), thickness=int(5))
handConStyle = mpDraw.DrawingSpec(color=(0, 255, 0), thickness=int(10))
figure = np.zeros(5)
landmark = np.empty((21, 2))

# sys.path.append("/home/e300/E300_file/zcj/e300/pythonfile/")

def detect2(frame):
    pTime = time.time()
    gesture_result =''

    # 读取视频图像的高和宽
    frame_height = frame.shape[0] 
    frame_width = frame.shape[1]

    if os.path.isfile('handDemo.py'):
        from handDemo import detect_hands_gesture,roi,finger_stretch_detect,get_fps
        l = roi(frame)
        if(l[1]>l[0] and l[3]>l[2]):
            cutFrame = frame[l[0]:l[1],l[2]:l[3]]
            cv.rectangle(frame, (l[2],l[0]), (l[3],l[1]), (0,255,0), 3)
        else:
            cutFrame  = frame
    elif os.path.isfile("./train/task2/handTrain.so"):
        from handTrain import detect_hands_gesture,roi,finger_stretch_detect,get_fps
        l = roi(frame)
        if(l[1]>l[0] and l[3]>l[2]):
            cutFrame = frame[l[0]:l[1],l[2]:l[3]]
            cv.rectangle(frame, (l[2],l[0]), (l[3],l[1]), (0,255,0), 3)
        else:
            cutFrame  = frame
    else:
        cutFrame  = frame
        return [frame,'']


    # mediaPipe的图像要求是RGB，所以此处需要转换图像的格式
    frame_RGB = cv.cvtColor(cutFrame, cv.COLOR_BGR2RGB)
    result = hands.process(frame_RGB)

    if result.multi_hand_landmarks:
        # 为每个手绘制关键点和连接线
        for i, handLms in enumerate(result.multi_hand_landmarks):
            mpDraw.draw_landmarks(cutFrame,
                                    handLms,
                                    mpHands.HAND_CONNECTIONS,
                                    landmark_drawing_spec=handLmsStyle,
                                    connection_drawing_spec=handConStyle)

            for j, lm in enumerate(handLms.landmark):
                xPos = int(lm.x * frame_width)
                yPos = int(lm.y * frame_height)
                landmark_ = [xPos, yPos]
                landmark[j, :] = landmark_

            # 通过判断手指尖与手指根部到0位置点的距离判断手指是否伸开(拇指检测到17点的距离)
            for k in range(5):
                if k == 0:
                    figure_ = finger_stretch_detect(landmark[17], landmark[4 * k + 2], landmark[4 * k + 4])
                else:
                    figure_ = finger_stretch_detect(landmark[0], landmark[4 * k + 2], landmark[4 * k + 4])

                figure[k] = figure_

        if os.path.isfile('handDemo.py'):
            from handDemo import detect_hands_gesture,roi
            gesture_result = detect_hands_gesture(figure)
            cv.putText(frame, f"{gesture_result}", (30, 60 * (i + 1)), cv.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 5)
        if os.path.isfile("./train/task2/handTrain.so"):
            from handTrain import detect_hands_gesture,roi
            gesture_result = detect_hands_gesture(figure)
            cv.putText(frame, f"{gesture_result}", (30, 60 * (i + 1)), cv.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 5)


        fps = get_fps(pTime)

        cv.putText(frame, f'FPS: {int(fps)}', (400, 50), cv.FONT_HERSHEY_COMPLEX,
                    1, (255, 0, 0), 3)
        return [frame,gesture_result]
    else:
        return [frame,'']

