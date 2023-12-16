'''
    这个模块是测试在内存共享中互相转输摄像头数据 2023.09
'''

import cv2
import numpy as np
import mmap
import time



mmap_len = 1024*1024*10



def readvideo():
    import mmap
    read_conf = None
    recwidth = None
    recheight = None
    reccount = None
    start = time.time()
    allcount = 0

    if read_conf is None:
        read_conf = mmap.mmap(0, mmap_len, access=mmap.ACCESS_WRITE, tagname='aivvideo') 
    

    while(1):
        read_conf.seek(0)
        flag = read_conf.read(1)
        #print('收到flag值是：',flag)
        if flag == b'1':
            try:
                if reccount is None:
                    read_conf.seek(1)
                    nparray = read_conf.readline()[:-1] #把回车符删除
                    print('长度是：{},内容是：\n{}'.format(len(nparray),nparray))
                    arr = np.frombuffer(nparray,dtype=np.float64)
                    print(arr)

                    recwidth,recheight = int(arr[3]),int(arr[4])
                    print('分辨率是：{} x {}'.format(recwidth,recheight))
                    reccount = recwidth * recheight * 3

                read_conf.seek(1024)
                buffer = read_conf.read(reccount)
                if len(buffer)>0:  
                    #print('收到的长度：',len(buffer))
                    img = np.frombuffer(buffer,dtype=np.uint8).reshape(recheight,recwidth,3)
                    #gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                    allcount += 1
                    end = time.time()
                    title = round(allcount/(end-start),1)
                    cv2.putText(img, str(title), (5,50 ), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
                    cv2.imshow('camera01',img) 
            except Exception as e:
                print('发生错误：\n',e)
            finally:
                read_conf.seek(0)   
                read_conf.write(b'0')
                


        if cv2.waitKey(1) & 0xFF == ord('q'):
            print('退出 readvideo() 函数')
            read_conf.close()
            cv2.destroyAllWindows()
            break

def opencamera():
    # 指定IP摄像头的IP地址和端口号
    #ip_address = 'http://192.168.1.100:8080/video'
    # 创建VideoCapture对象
    #cap = cv2.VideoCapture(0) #不打开 CAP_DSHOW函数,有些摄像头不能读取视频
    cap =cv2.VideoCapture(0,cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("无法打摄像机")
        return
    
    param = []
    for i in range(10):
        param.append(cap.get(i))
    #par = bytes(param)
    param = np.array(param)

    byt = param.tobytes()
    leng = len(byt)
    print('cap:\n类型是：{},内容是：{},长度是：{},\n字节码是：{}'.format(param.dtype,param,leng,byt))
    print('视频大小：{} x {}'.format(int(param[3]),int(param[4])))
    
    mmap_conf = mmap.mmap(0, mmap_len, access=mmap.ACCESS_WRITE, tagname='aivvideo')

    while True:
        # 从摄像头中读取一帧图像
        ret, frame = cap.read()
        #print('frame:\n',frame)
        if frame is None: 
            continue

        mmap_conf.seek(0)
        flag = mmap_conf.read(1)
        #print('flag开始的值是：',flag)
        if flag==b'\x00' or flag==b'0':
            try:
                #print('发送长度：',mylen)
                mmap_conf.seek(1)
                mmap_conf.write(byt)
                mmap_conf.write(b'\n')
                
                mmap_conf.seek(1024)
                temparray = frame.tobytes()
                mmap_conf.write(temparray)
                # 显示图像
                #cv2.imshow('IP Camera', frame)
                #readvideo()
                # 按下q键退出程序
            except Exception as e:
                print('出错了：\n',e)
            finally:
                mmap_conf.seek(0)
                mmap_conf.write(b'1')

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print('退出 opencamera() 函数')
            cap.release()
            mmap_conf.close()
            break

    

if __name__ == '__main__':
    from multiprocessing import Process
    import time 
    import os
    #print('主线程ID是：',os.getppid())

    p = Process(target=opencamera)
    p.daemon=True #主进程退出,线程也退出
    
    p.start()
    print('主线程ID是：{}线程Id是：{}'.format(os.getppid(),p.pid))
    readvideo()

    # 释放资源

    #cap.release()
    #cv2.destroyAllWindows()
