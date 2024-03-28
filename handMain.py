from email.mime import image
from http.client import ImproperConnectionState
from inspect import Parameter
import cv2 as cv
import numpy as np
import mediapipe as mp
import time
from numpy import linalg
from utils import Jdict
import json
import os
import socket
from threading import Thread
import platform
# from handDemo import roi,detect_hands_gesture
# from handtest import detect2
import os, sys
os.chdir(sys.path[0])

# DETECT TIMES
detect_times = 0
# RESULT LIST
result_list = ['1','2','3','4','5','6','7','8','9','10']

# 视频设备号
DEVICE_NUM = 0

# UDP SEND MESSAGE
def send_message(data):
    global client_addr
    try:
        s.sendto(data,client_addr)
    except Exception as e:
        print("Gesture detect udpsend error:",e)


# 手指检测
# point1-手掌0点位置，point2-手指尖点位置，point3手指根部点位置
def finger_stretch_detect(point1, point2, point3):
    result = 0
    # 计算向量的L2范数
    dist1 = np.linalg.norm((point2 - point1), ord=2)
    dist2 = np.linalg.norm((point3 - point1), ord=2)
    if dist2 > dist1:
        result = 1

    return result


# READ JSON FILE
parameter = Jdict(json.loads(open('config.json', 'r').read()))
file_f = 0

def detect():
    #计算fps用到的参数pTime初始化
    # 接入USB摄像头时，注意修改cap设备的编号
    cap = cv.VideoCapture(0) #,cv.CAP_DSHOW)
    # 加载手部检测函数


    global file_f
    

    if not cap.isOpened():
        print("Can not open camera.")
        exit()

    while True:
        ret, frame = cap.read()
        # print(frame)
        if(platform.system()=='Linux'):
            if os.path.isfile("handtest.py"):
                from handtest import detect2
                file_f = 1
        else:
            from handtest import detect2
            file_f = 1
        if file_f == 1:
            [frame,s ]= detect2(frame)
        if(platform.system()=='Windows'):
            cv.imshow('Gesture Detect', frame)
            cv.moveWindow("Gesture Detect",100,100)
            # print('Windows系统')
        elif(platform.system()=='Linux'):
            cv.imshow('Gesture Detect', frame)
            # WINDOW POSION
            cv.moveWindow("Gesture Detect",100,100)
            # print('Linux系统')
        elif(platform.system()=='Darwin'):
            cv.imshow('Gesture Detect', frame)
            cv.moveWindow("Gesture Detect",100,100)
            # print('Mac系统')
       
        if cv.waitKey(1) == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()



if __name__ == '__main__':
    detect()


