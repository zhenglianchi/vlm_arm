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

def move_to_top_view():
    print('移动至俯视姿态')
    rtde_c.moveJ([-62.13, 8.96, -87.71, -14.41, 2.54, -16.34],0.5,0.3)
    time.sleep(3)

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


def eye2hand(X_im=160, Y_im=120):
    '''
    输入目标点在图像中的像素坐标，转换为机械臂坐标
    '''

    # 整理两个标定点的坐标
    cali_1_im = [130, 290]                       # 左下角，第一个标定点的像素坐标，要手动填！
    cali_1_mc = [-21.8, -197.4]                  # 左下角，第一个标定点的机械臂坐标，要手动填！
    cali_2_im = [640, 0]                         # 右上角，第二个标定点的像素坐标
    cali_2_mc = [215, -59.1]                    # 右上角，第二个标定点的机械臂坐标，要手动填！
    
    X_cali_im = [cali_1_im[0], cali_2_im[0]]     # 像素坐标
    X_cali_mc = [cali_1_mc[0], cali_2_mc[0]]     # 机械臂坐标
    Y_cali_im = [cali_2_im[1], cali_1_im[1]]     # 像素坐标，先小后大
    Y_cali_mc = [cali_2_mc[1], cali_1_mc[1]]     # 机械臂坐标，先大后小

    # X差值
    X_mc = int(np.interp(X_im, X_cali_im, X_cali_mc))

    # Y差值
    Y_mc = int(np.interp(Y_im, Y_cali_im, Y_cali_mc))

    return X_mc, Y_mc

# 吸泵吸取并移动物体
#def pump_move(mc, XY_START=[230,-50], HEIGHT_START=90, XY_END=[100,220], HEIGHT_END=100, HEIGHT_SAFE=220):

    '''
    用吸泵，将物体从起点吸取移动至终点

    mc：机械臂实例
    XY_START：起点机械臂坐标
    HEIGHT_START：起点高度
    XY_END：终点机械臂坐标
    HEIGHT_END：终点高度
    HEIGHT_SAFE：搬运途中安全高度
    '''
    
    '''# 初始化GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(20, GPIO.OUT)
    GPIO.setup(21, GPIO.OUT)

    # 设置运动模式为插补
    mc.set_fresh_mode(0)
    
    # # 机械臂归零
    # print('    机械臂归零')
    # mc.send_angles([0, 0, 0, 0, 0, 0], 40)
    # time.sleep(4)
    
    # 吸泵移动至物体上方
    print('    吸泵移动至物体上方')
    mc.send_coords([XY_START[0], XY_START[1], HEIGHT_SAFE, 0, 180, 90], 20, 0)
    time.sleep(4)

    # 开启吸泵
    pump_on()
    
    # 吸泵向下吸取物体
    print('    吸泵向下吸取物体')
    mc.send_coords([XY_START[0], XY_START[1], HEIGHT_START, 0, 180, 90], 15, 0)
    time.sleep(4)

    # 升起物体
    print('    升起物体')
    mc.send_coords([XY_START[0], XY_START[1], HEIGHT_SAFE, 0, 180, 90], 15, 0)
    time.sleep(4)

    # 搬运物体至目标上方
    print('    搬运物体至目标上方')
    mc.send_coords([XY_END[0], XY_END[1], HEIGHT_SAFE, 0, 180, 90], 15, 0)
    time.sleep(4)

    # 向下放下物体
    print('    向下放下物体')
    mc.send_coords([XY_END[0], XY_END[1], HEIGHT_END, 0, 180, 90], 20, 0)
    time.sleep(3)

    # 关闭吸泵
    pump_off()

    # 机械臂归零
    print('    机械臂归零')
    mc.send_angles([0, 0, 0, 0, 0, 0], 40)
    time.sleep(3)'''