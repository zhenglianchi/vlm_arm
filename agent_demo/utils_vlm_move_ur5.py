# utils_vlm_move.py
# 同济子豪兄 2024-5-22
# 输入指令，多模态大模型识别图像，吸泵吸取并移动物体

# print('神行太保：能看懂“图像”、听懂“人话”的机械臂')
#from utils_ur5 import *
from utils_asr import *
from utils_vlm import *

import time

def top_view_shot(check=False):
    '''
    拍摄一张图片并保存
    check：是否需要人工看屏幕确认拍照成功，再在键盘上按q键确认继续
    '''
    print('移动至俯视姿态')
    #move_to_top_view()
    
    # 获取摄像头，传入0表示获取系统默认摄像头
    cap = cv2.VideoCapture(0)
    # 打开cap
    cap.open(0)
    time.sleep(2)
    success, img_bgr = cap.read()
    
    # 保存图像
    print('保存至temp/vl_now.jpg')
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
    cv2.destroyAllWindows()


def vlm_move(PROMPT='帮我把绿色方块放在小猪佩奇上', input_way='keyboard'):
    '''
    多模态大模型识别图像，吸泵吸取并移动物体
    input_way：speech语音输入，keyboard键盘输入
    '''

    print('多模态大模型识别图像，吸泵吸取并移动物体')
    
    # 机械臂归零
    print('机械臂归零')
    #back_zero()
    time.sleep(3)
    
    ## 第一步：完成手眼标定
    print('第一步：完成手眼标定')
 
    print('第二步，给出的指令是：', PROMPT)
    
    ## 第三步：拍摄俯视图
    print('第三步：拍摄俯视图')
    top_view_shot(check=True)
    
    ## 第四步：将图片输入给多模态视觉大模型
    print('第四步：将图片输入给多模态视觉大模型')
    img_path = 'temp/vl_now.jpg'
    
    n = 1
    while n < 5:
        try:
            print('    尝试第 {} 次访问多模态大模型'.format(n))
            result = yi_vision_api(PROMPT, img_path='temp/vl_now.jpg')
            print('    多模态大模型调用成功！')
            print(result)
            break
        except Exception as e:
            print('    多模态大模型返回数据结构错误，再尝试一次', e)
            n += 1
    
    ## 第五步：视觉大模型输出结果后处理和可视化
    print('第五步：视觉大模型输出结果后处理和可视化')
    START_X_CENTER, START_Y_CENTER, END_X_CENTER, END_Y_CENTER = post_processing_viz(result, img_path, check=True)
    
    ## 第六步：手眼标定转换为机械臂坐标
    print('第六步：手眼标定，将像素坐标转换为机械臂坐标')
    # 起点，机械臂坐标
    #START_X_MC, START_Y_MC = eye2hand(START_X_CENTER, START_Y_CENTER)
    # 终点，机械臂坐标
    #END_X_MC, END_Y_MC = eye2hand(END_X_CENTER, END_Y_CENTER)
    
    ## 第七步：吸泵吸取移动物体
    print('第七步：移动物体')
    #pump_move(mc=mc, XY_START=[START_X_MC, START_Y_MC], XY_END=[END_X_MC, END_Y_MC])
    
    ## 第八步：收尾
    print('第八步：任务完成')
    #GPIO.cleanup()            # 释放GPIO pin channel
    cv2.destroyAllWindows()   # 关闭所有opencv窗口
    # exit()
    
    
    
    
