import time
import numpy as np

'''
题目1：
roi
功能：设置感兴趣区域，只有在感兴趣区域内的手势才会被检测
参数：frame: 读取的视频帧
返回值：感兴趣区域的左上角和右下角坐标
'''
def roi(frame):
    frame_height = frame.shape[0]  # 视频帧的高度
    frame_width = frame.shape[1]  # 视频帧的宽度

    # 设置感兴趣区域，x_start,y_start,x_end,y_end分别为感兴趣区域的左上角和右下角坐标
    x_start = int(frame_width / 2 - 300)
    x_end = int(frame_width / 2 + 300)
    y_start = int(frame_height / 2 - 150)
    y_end = int(frame_height / 2 + 150)
    return [y_start, y_end, x_start, x_end]


'''
题目2：
finger_stretch_detect
功能：判断手指屈伸
参数：point1-手掌0点位置，point2-手指根点位置，point3手指尖部点位置
返回值：手指屈伸结果result，0代表屈曲，1代表伸直
'''


def finger_stretch_detect(point1, point2, point3):
    result = 0
    # 计算向量的L2范数。dist1为手指根点到手掌0点的距离，dist2为手指尖部点到手掌0点的距离
    dist1 = np.linalg.norm((point2 - point1), ord=2)
    dist2 = np.linalg.norm((point3 - point1), ord=2)

    if dist2 > dist1:
        result = 1

    return result


'''
题目3：
detect_hands_gesture
功能：检测手势
参数：result :用于存储手指屈伸信息，格式为ndarray
返回值：字符串gesture，手势识别结果
'''


def detect_hands_gesture(result):
    # result改为列表
    result = result.tolist()

    # 根据手势的特征向量result，判断手势,如果result为[1,0,0,0,0]，代表大拇指伸直，其余四指弯曲，对应结果gesture为'thumbUp'
    if result == [1, 0, 0, 0, 0]:
        gesture = "thumbUp"
    elif result == [0, 1, 0, 0, 0]:
        gesture = "one"
    elif result == [0, 0, 1, 0, 0]:
        gesture = "Please civilization in testing."
    elif result == [0, 1, 1, 0, 0]:
        gesture = "two"
    elif result == [0, 1, 1, 1, 0]:
        gesture = "three"
    elif result == [0, 1, 1, 1, 1]:
        gesture = "four"
    elif result == [1, 1, 1, 1, 1]:
        gesture = "five"
    elif result == [1, 0, 0, 0, 1]:
        gesture = "six"
    elif result == [0, 0, 1, 1, 1]:
        gesture = "OK"
    elif result == [0, 0, 0, 0, 0]:
        gesture = "fist"
    elif result == [0, 0, 0, 0, 1]:
        gesture = "pink"
    elif result == [1, 1, 0, 0, 1]:
        gesture = "ILoveyou"
    elif result == [1, 1, 0, 0, 0]:
        gesture = "gun"
    else:
        gesture = "Not in detect range..."
    return gesture


'''
题目4：
get_fps
功能：计算帧率
参数：pTime-获取该帧的时间
返回值：fps-帧率
'''


def get_fps(pTime):
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    return fps