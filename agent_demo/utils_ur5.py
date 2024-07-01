# utils_robot.py
# 同济子豪兄 2024-5-22
# 启动并连接机械臂，导入各种工具包

print('导入机械臂连接模块')
import rtde_control
import rtde_receive
import cv2
import numpy as np
import time

# 连接机械臂,需要获取机器人的IP地址
rtde_c = rtde_control.RTDEControlInterface("127.0.0.1")
rtde_r = rtde_receive.RTDEReceiveInterface("127.0.0.1")

def back_zero():
    '''
    机械臂归零
    '''
    print('机械臂归零')
    # 六自由度关节角度，速度，加速度
    rtde_c.moveJ([0, 0, 0, 0, 0, 0], 0.5, 0.3)
    time.sleep(3)


def head_shake():
    # 左右摆头
    # 六自由度关节角度，速度，加速度
    rtde_c.moveJ([0.87,(-50.44),47.28,0.35,(-0.43),(-0.26)],0.5,0.3)
    time.sleep(1)
    # 得到目前真实的关节角度
    actual_q = rtde_r.getActualQ()
    for count in range(2):
        actual_q[4]=30
        rtde_c.moveJ(actual_q,0.5,0.3)
        time.sleep(0.5)
        actual_q[4]=-30
        rtde_c.moveJ(actual_q,0.5,0.3)
        time.sleep(0.5)
    rtde_c.moveJ([0, 0, 0, 0, 0, 0], 0.5, 0.3)
    time.sleep(2)

def head_dance():
    # 跳舞
    rtde_c.moveJ([0.87,(-50.44),47.28,0.35,(-0.43),(-0.26)],0.5,0.3)
    time.sleep(1)
    for count in range(1):
        rtde_c.moveJ([(-0.17),(-94.3),118.91,(-39.9),59.32,(-0.52)],0.5,0.3)
        time.sleep(1.2)
        rtde_c.moveJ([67.85,(-3.42),(-116.98),106.52,23.11,(-0.52)],0.5,0.3)
        time.sleep(1.7)
        rtde_c.moveJ([(-38.14),(-115.04),116.63,69.69,3.25,(-11.6)],0.5,0.3)
        time.sleep(1.7)
        rtde_c.moveJ([2.72,(-26.19),140.27,(-110.74),(-6.15),(-11.25)],0.5,0.3)
        time.sleep(1)
        rtde_c.moveJ([0,0,0,0,0,0],0.5,0.3)

def head_nod():
    # 点头
    rtde_c.moveJ([0.87,(-50.44),47.28,0.35,(-0.43),(-0.26)],0.5,0.3)
    actual_q = rtde_r.getActualQ()
    for count in range(2):
        actual_q[3]=13
        rtde_c.moveJ(actual_q,0.5,0.3)
        time.sleep(0.5)
        actual_q[3]=-20
        rtde_c.moveJ(actual_q,0.5,0.3)
        time.sleep(1)
        actual_q[3]=13
        rtde_c.moveJ(actual_q,0.5,0.3)
        time.sleep(0.5)
    rtde_c.moveJ([0.87,(-50.44),47.28,0.35,(-0.43),(-0.26)],0.5,0.3)


def single_joint_move(joint_index, angle):
    print('关节 {} 旋转至 {} 度'.format(joint_index, angle))
    actual_q = rtde_r.getActualQ()
    actual_q[joint_index-1] = angle
    rtde_c.moveJ(actual_q,0.5,0.3)
    time.sleep(2)


def top_view_shot(check=False):
    '''
    拍摄一张图片并保存
    check：是否需要人工看屏幕确认拍照成功，再在键盘上按q键确认继续
    '''
    print('    移动至俯视姿态')
    #move_to_top_view()
    
    # 获取摄像头，传入0表示获取系统默认摄像头
    cap = cv2.VideoCapture(0)
    # 打开cap
    cap.open(0)
    time.sleep(0.3)
    success, img_bgr = cap.read()
    
    # 保存图像
    print('    保存至temp/vl_now.jpg')
    cv2.imwrite('temp/vl_now.jpg', img_bgr)

    # 屏幕上展示图像
    cv2.destroyAllWindows()   # 关闭所有opencv窗口
    cv2.imshow('zihao_vlm', img_bgr) 
    
    if check:
        print('请确认拍照成功，按c键继续，按q键退出')
        while(True):
            key = cv2.waitKey(10) & 0xFF
            if key == ord('c'): # 按c键继续
                break
            if key == ord('q'): # 按q键退出
                # exit()
                cv2.destroyAllWindows()   # 关闭所有opencv窗口
                raise NameError('按q退出')
    else:
        if cv2.waitKey(10) & 0xFF == None:
            pass
        
    # 关闭摄像头
    cap.release()
    # 关闭图像窗口
    # cv2.destroyAllWindows()