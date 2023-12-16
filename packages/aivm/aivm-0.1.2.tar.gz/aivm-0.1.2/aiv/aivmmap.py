'''
    Aiv平台进程共享内存管理模块 (2023.10)
    Aiv系统使用多进程运行模式,包含Aivc.exe主进程、wc进程(websocket + webrtc 进程<使用multiprocessing创建>)、
    还有ship模块(全部是独立进程,window下是用nuitka编译成的独立的exe执行文件,用subprocess.Popen启动)。
    因此,进程之间需要共享数据,在Aiv系统中,使用mmap实现进程数据共享
    在此aivmmap.py类中,实现了各进程需要使用的共享内存管理类,而且实现共享内存锁。
    每个模块（进程）之间,通过mmap互相协作。使用Aiv平台成一个“来料加工”的AI平台
    每个进程之间,可以共享两种数据：控制信息、加工的数据
'''
# from typing import Any
from loguru import logger
import mmap,os,sys,json,asyncio,time
from enum import Enum
from aiv.aivtool import _write_mmap,_read_mmap,AivSys

taskMMAPLen = 1024*1024*10 # 每个任务 10M ,如果有10个任务,则是 10*10M
taskMMAPName = 'aivtask'
taskMMAPStart = 10  #读任务共享内存的起始位置,默认是10, 即前面留10个字节给以后扩展用(第1字节用来存TaskState状态了) 2023.10
newTaskMMAPName = 'aivnewtask' #新任务的共享内存类。只给  AivWcMmap与AivMainMmap类用

confMMAPLen = 1024*1024 # 1M
confMMAPName = 'aivconf'

shipMMAPLen = 1024*1024*10 # 10M
shipMMAPName = 'aivship'


# 这是服务端使用的状态码：在各共享内存中共享
class TaskState(Enum):
    taskNone = 0        # 无任务在流水线中
    # taskNew = 50         # 新任务状态
    # taskCheck = 80       # 检查状态
    taskReady = 100      # 有任务,还在准备阶段(主程序先要把运行任务需要的文件下载)
    # taskOk = 200         # 服务器执行完成（成功)
    taskShip = 300       # 各ship 抢任务阶段 (wc模块把任务 taskShip 状态, ship模块判断如是taskShip就可以接单 2023.11)
    taskRun = 400        # ship锁定,并开始运行阶段
    taskFinished = 500   #ship任务完成,交回流水线中(但任务还没结束,因为接下来还要把生成的文件发回js端。如果任务完成,会设为 TaskEnd状态)
    taskProExit  = 600    # 用户取消
    # taskBusy = 700       # 服务器繁忙
    taskEnd  = 1000      # 任务已经终止 (也许未成功,也许成功,如果出现此标志,websocket马上返回)
    # taskProExit = 2000   # 有关进程退出 2023.11


# 这是前端与服务端交流的任务返回码.前端根据返回的任务码判断任务执行到什么阶段,是否成功等?  2023.11
class TaskResultCode(Enum):
    '''
        返回客户端的标识
        * 类似web请求返回码
        * 在task的'result'字段中记录
    '''
    taskNew = 50   # 接收新任务
    taskReady = 100  # 1xx：信息类，表示客户发送的请求服务端正在处理。
    taskOk = 200    # 2xx：成功类，服务器成功接收请求。
    taskShip = 300   # 3xx：已经进入ship模块处理阶段
    taskId = 400  # 4xx: 客户端验证错误类，对于发的请求服务器无法处理(主要是没登录或权限不够)
    taskSvr = 500   # 5xx: 服务端错误
    taskUser = 600  # 6xx: 客户中止

    def getMsg(self):
        '''
            要调用此getMsg()函数,例如下：
            TaskResultCode.taskOk.getMsg()   TaskResultCode.taskSvr.getMsg()
            因为每个枚举成员（枚举值）都是一个实例
        '''
        if self.value==100:
            return '任务处理准备中'
        elif self.value==200:
            return '任务成功!'
        elif self.value==300:
            return '任务正在由Ship模块处理'
        elif self.value==400:
            return '任务的发起用户权限不足'
        elif self.value==500:
            return '任务引起服务器错误'
        elif self.value==600:
            return '任务的发起用户中止操作'
        else:
            return '未知状态'


class AivBaseMmap:
    def __init__(self,isMain,newTaskMMAPName=None) -> None:
        if newTaskMMAPName is None:
            newTaskMMAPName = taskMMAPName

        # logger.warning('AivBaseMmap新建的名是：{}'.format(newTaskMMAPName))
        self.isMain = isMain  
        # self.state = TaskState.taskNone
        # self.taskBusy = False #是否忙录
        self.task = None
        if isMain:
            self.confMMAP = mmap.mmap(0, confMMAPLen, access=mmap.ACCESS_WRITE, tagname=confMMAPName)
        else:
            self.confMMAP = mmap.mmap(0, confMMAPLen, access=mmap.ACCESS_COPY, tagname=confMMAPName)

        # 每个任务占一格,任务池里就像格子一样
        self.taskMMAP = mmap.mmap(0, taskMMAPLen, access=mmap.ACCESS_WRITE, tagname = newTaskMMAPName)

        #记录了系统的信息,AivSys是附属类。这里AivBaseMmap 的 AivSys 可以从系统读取(isMain==True时候)
        # 也可以从共享内存读取(isMain==False时候)
        self.aivSys = AivSys(isMain)
        self.checkMultipleInstances() #检测程序是否是重复运行 
        self.updateSysInfo()

    def checkMultipleInstances(self):
        ''' 2023.12
            检测程序是否重复运行
            通过检测self.confMMAP共享内存,如果已经写有数据,说明已经启动程序实例
            检测发现重复运行,即中止进程
        '''
        if self.isMain:
            dic = _read_mmap(self.confMMAP,0,0,True)
            # 读取 self.confMMAP内存共享,如果发现已经写有数据,说明已经建立了一个实例程序。因此就在这里把进程终止
            if dic is not None:
                logger.warning('AIV程序已经运行! 不能重复启动。')
                self.aivSys.killMe('AivC')


    def readTask(self,mmap = None):
        tempMmap = mmap
        if mmap is None:
            tempMmap = self.taskMMAP
        return _read_mmap(tempMmap,taskMMAPStart,0,True)    
    
    def writeTask(self,taskData,mmap = None):
        tempMmap = mmap
        if mmap is None:
            tempMmap = self.taskMMAP #默认读写 taskMMAP
        return _write_mmap(tempMmap,taskData,taskMMAPStart)    
    
    # 清空指定索引的任务块内存----2023.11
    def clearTask(self,mmap= None):
        tempMmap = mmap
        if mmap is None:
            tempMmap = self.taskMMAP #默认读写 taskMMAP
        tempMmap.seek(0)
        for i in range(taskMMAPLen):
            tempMmap.write(b'\x00')
        tempMmap.flush()


    # 更新共享内存中的系统信息---2023.10---
    def updateSysInfo(self):
        if self.isMain:
            self.aivSys.updateSysRunTime() #先更新系统运行多久的时间
            sysInfo = self.aivSys.getSysInfo()
            _write_mmap(self.confMMAP,sysInfo)
            # logger.warning('写入共享内存成功！=={}'.format(sysInfo['deviceBingCode']))
        else:
            dic = _read_mmap(self.confMMAP,0,0,True)
            self.aivSys.setSysInfo(dic)

    def getFilePath(self,file):
        '''
            根据前端给的文件 file 信息,生成文件在服务端相对应的绝对路径
        '''
        if file['md5'] is None:
            logger.warning('文件的 MD5 值为空！')
            return ''
        
        md5 = file['md5']
        extName = os.path.splitext(file['name'])[1] #获取文件扩展名
        return os.path.join(self.aivSys.aivTempDir, md5 + extName)


    def checkState(self,value):
       return next((item for item in TaskState if item.value == value), TaskState.taskNone)
    


    def setTaskResultCode(self,state:TaskResultCode):
        '''
            设置任务的返回值 2023.10
            * 每个任务数据,都带有一个  result 参数,里面有 'code' 和 'msg' 'data' 数据字段
            * code和msg的内容固定, data 数据字段可以写扩展内容
            * 无论任务是否成功执行,这个 result 都会返回,result里的数据可以说明什么原因出错,或执行到哪一步返回的
        '''
        if self.task is None:
            return
        self.task['result']['code'] = state.value # 设置返回值的状态
        self.task['result']['msg'] = state.getMsg()


    # 设置共享内存中的任务标志
    def setTaskState(self,state:TaskState,mmap=None):
         # 写入标志位
        tag = state.value
        byte = tag.to_bytes(2, 'big') #写入双字节, 2表示双字节 , 1字节最大只能写 256位
        tempMmap = mmap
        if mmap is None:
            tempMmap = self.taskMMAP
        tempMmap.seek(0)
        tempMmap.write(byte)
        tempMmap.flush()

    #读出任务共享内存中的标志
    def getTaskState(self,mmap=None):
        tempMmap = mmap
        if mmap is None:
            tempMmap = self.taskMMAP #默认是读 taskMMAP

        tempMmap.seek(0)
        chr = tempMmap.read(2) #读入双字节
        value = int.from_bytes(chr, 'big') #读出第一个字节
        return self.checkState(value)


# 主程序的MMAP管理类 2023.10
class AivMainMmap(AivBaseMmap):
    ''' 2023.11
        主进程序的内存管理类
        由AivMainPro类使用,这个类主要功能就是 能过AivSys收集本机的信息,然后写到 confMMAPName 共享内存中,供其它模块使用
        AivMainMmap 类的功能,仅此一项
    '''
    def __init__(self) -> None:
        super().__init__(True)
        


# 主程序的MMAP管理类 2023.11
class AivProMmap(AivBaseMmap):
    '''
        主进程序的ShipPro 内存管理类
        由ShipPro类使用,这个类主要功能是与ship的aivwc模块,ship模块的任务共享内存一起使用  
        用来监控其它两个进程的运行: ship模块 ,aivwc模块 (因为每个任务都建立一套系统: AivProMmap + AivWC + Ship )
    '''
    def __init__(self,newTaskMMAPName) -> None:
        super().__init__(False,newTaskMMAPName)

    # async def allProExit(self): #通知wc,ship退出进程 (往共享内存写入指令)
    #     self.setTaskState(TaskState.taskProExit)
    #     await asyncio.sleep(0.01) # 保险起见,多写一次
    #     self.setTaskState(TaskState.taskProExit)

    def checkTaskProExit(self): 
        ''' 2023.11
            检查任务是否被取消 
            由aivWc 写入取消指令,它通过websocket收到用户指令,然后写入共享内存,通知三方(aivMainPro,ship,aivWc)
            aivMainPro的 AivProMmap 和 ship模块收到通知后,做相应的处理
        '''
        return self.getTaskState()==TaskState.taskProExit

    async def sendProExitMsg(self):
        '''
            用户取消任务
            aivwc、ship模块,看到取消指令,马上停止任务,并退出进程
        '''
        self.setTaskState(TaskState.taskProExit) #通知其它进程退出        

# ship的内存共享管理类
class AivShipMmap(AivBaseMmap):
    def __init__(self,shipName,shipId,newTaskMMAPName) -> None:
        super().__init__(False,newTaskMMAPName)
        self.shipId = shipId
        self.shipName = shipName
        # self.shipMMAP = self.initShipMMAP()
        # self.task = AivTask() #给aivTask 设置一个任务
        self.onStartTask = None #有任务触发的事件
    
    async def run(self):
        '''
            AivShipMmap类的 协程函数入口
            目的就是不断检测是否有新任务可以执行（抢单）
        '''

        logger.debug('AivShipMmap 运行了!')
        while True:
            
            await self.checkTask()

            state = self.getTaskState()
            # logger.warning('AivShipMmap: run() 检测任务情况. state == {}'.format(state))

            if state == TaskState.taskProExit:
                self.endTask(TaskState.taskProExit)
                # self.aivSys.killMe('AivShipMmap')
                # self.killMe(True)

            await asyncio.sleep(0.2)   


    # def killMe(self,isCanecel): #关闭自己的进程
    #     msg = ''
    #     if isCanecel:
    #         msg = '用户取消任务! ship模块 {} 进程退出.'.format(self.shipName)
    #     else:
    #         msg = '任务完成! ship模块 {} 进程退出.'.format(self.shipName)

    #     logger.debug(msg)
    #     # await asyncio.sleep(0.1)
    #     os._exit(0)

    # 只有ship才建立 shipMMAP, 主程序端要建立每个ship模块的MMAP数组
    # def initShipMMAP(self):
    #     if self.aivShip is None or  self.aivShip.pid is None:
    #         logger.error('aivShip.pid is None, 请先创建!')
    #         return None
        
    #     name = shipMMAPName + str(self.aivShip.pid) #每一个ship类的 ship 共享内存类ID = shipMMAPName + 进程ID
    #     return mmap.mmap(0, shipMMAPLen, access=mmap.ACCESS_WRITE, tagname=name)

    # def updateShipInfo(self):
    #     shipInfo = self.aivShip.getShipInfo()
    #     _write_mmap(self.shipMMAP,shipInfo)

    # 从共享内存中读取 任务内容
    async def checkTask(self): # run()中的协程函数
        '''
            抢任务单
            * 通过不断检测任务的共享内存状态,如果有合适自己的任务,即抢过来执行。
            * 匹配的条件一是 shipId 相等, 二是自己处于空闲状态
        '''    

        taskState = self.getTaskState()

        # logger.debug('读到的任务状态是：{}'.format(taskState))

        if taskState != TaskState.taskShip: #如果第一项是taskShip任务标记,则读出里面的内容，然后再分析任务内容是否是自己要执行的
            return

        # 读出任务内容,如果是自己的任务,则开始处理,并锁定共享任务内存
        currTask =  _read_mmap(self.taskMMAP,taskMMAPStart,0,True)  # taskMMAPStart 是从哪个字节开始读,默认是 10
        
        # logger.debug('读到的任务内容是：{}'.format(currTask))
        # 查询当前的任务指定的shipId 是否是自己的Id, 如果是就可以执行的任务（抢单）
        if currTask['shipId'] != self.shipId:
            currTask = None
            logger.error('任务指定的ship 与调用的ship模块的不附! 任务指定: shipId = {},\n 调用的ship模块是: {} shipId = {}'.format(currTask['shipId'],self.shipName,self.shipId))
            return
        
        # logger.warning('开始设置任务的标识： ship== {}'.format(self.aivShip.shipId))
        self.setTaskState(TaskState.taskRun) #把共享任务的标志设置为运行状态
        # 重新读一次看是否成功,如果发现不成功(或被抢了单,则返回)
        await asyncio.sleep(0.01) # 暂停10毫秒,如果不能锁定,则返回
        taskState = self.getTaskState()
        if taskState != TaskState.taskRun:
            currTask = None
            logger.warning('锁定任务 _id = {} 不成功!'.format(currTask['_id']))
            return
        
        # self.state = TaskState.taskRun #把自已的状态设为运行状态, 让自己这函数中止去抢单了
        # logger.debug('ship: readTaskInfo 模块: 抢单成功！任务内容是: {}'.format(currTask))
        self.task = currTask


        # 触发任务开始任务事件
        if self.onStartTask is not None:
            # logger.debug('ship: 准备触发 运行任务Api ,任务内容是：{}'.format(currTask))

            self.setTaskResultCode(TaskResultCode.taskShip) # 设置为进入ship模块处理状态
            self.onStartTask(self.task)

            

    def endTask(self,state = TaskState.taskFinished):
        '''
            这个函数是ship模块调用 2023.10
            * 在ship模块的api函数执行完成后,则调用此函数.
            * 此函数把任务完成标志写入共享内存中, 由aivc.exe端查询触发其它操作
        '''
        # logger.debug('ship: 模块endTask {} 本次任务执行完成！任务内容是 22211 ：{}'.format(self.shipName,self.task))

        # 把任务内容更新回共享内存中: 主要是输出文件是后面增加的内容
        _write_mmap(self.taskMMAP,self.task,taskMMAPStart) # taskMMAPStart 是从哪个字节开始读,默认是 10
        self.task = None
        self.setTaskState(state) # 把任务的共享内存的状态设为 已完成状态, 由后续的 wc.py 从共享内存计出模块处理
        
        self.aivSys.killMe('AivShipMmap')
        # self.killMe(False)
        # self.state = TaskState.taskNone #把自己也置为空闲状态
        # logger.debug('ship: 模块 {} 本次任务执行完成！'.format(self.aivShip.shipName))
        


# wc (websocket + webrtc) 的内存管理类 2023.10
class AivWcMmap(AivBaseMmap):
    ''' 2023.11
        与 AivWc 配置使用的共享内存管理类
        AivWcMmap类主要负责从共享内存中读取任务Task的数据、状态,然后通知AivWc下载、上传文件、通知AivWc与Js端通讯
        AivWc主要是拥有websocket与 webrtc功能,是Aiv pc服务端的文件传输、与客户端勾通的类
        每个任务,都将建立一套AivWc + AivWcMmap, 任务结束自行终止
    '''
    def __init__(self,newTaskMMAPName) -> None:
        super().__init__(False,newTaskMMAPName)
        self.taskList = []
        self.onDownloadFile = None
        self.onTaskReady = None  #任务准备完成时触发
        self.onTaskFinished = None

        # self.maxTaskCount = 50  #最大可以缓存的任务数量
        # self.taskList = {} #缓存的任务列表,用 task._id做 Key

        # 与 AivMainMmap 交流的共享内存类
        # self.newTaskMMAP = mmap.mmap(0, taskMMAPLen, access=mmap.ACCESS_WRITE, tagname= newTaskMMAPName)

    def startTask(self,task):
        '''
            启动任务
            * 这个函数由 wc.py 模块调用。它通过 websocket 接收前端发来的任务后,直接丢给AivWcMmap类处理
            * 这里,把任务内容task记录下来,然后把自己的状态设置为 taskReady 状态
            * 因为任务中,需要客户端的一些文件（图片、视频、音频等）,需要下载到本地才能执行。
            * 因此,把状态设为 taskReady后,由后续的函数 checkFileDownload()处理   
            * 现在,任务的内容还没有写入task的共享内存中。等下载完所有文件时,再写入给 Ship模块抢单(设置为'taskShip'状态).
            * 2023.10
        '''
        
        
        # 查询任务ID是否重复
        # logger.debug('AivWcMmap: 收到的新任务内容是： {} '.format(task))
        
        # 根据缓存的任务列表,如果任务列表不超过系统设置的最大值,就把任务先缓存进 taskList中,
        # 等待 协程 run() 函数从系统一个一个取出处理 2023.11
        # if self.taskList.get(task['_id'],None) is None:
        #     if len(self.taskList) >= self.maxTaskCount:
        #         logger.error('AivWcMmap: 任务数量超过能接收的数量 {} ,任务拒绝！'.format(self.maxTaskCount))
        #         return
        #     self.taskList[task['_id']] = task

        
        # return

        if self.task is not None:
            logger.warning('模块繁忙！')
            return
        
        self.task = task

        self.writeTask(task)

        #接收任务后,先设为 taskNew模式,然后,要等aivMainMmap类检查是否能新增（如果超过可以接任务的数量,就直接拒绝)
        # 如果aivMainMmap调用  AivPro 发现没有安装任务指定的ship模块,也会拒绝新增任务 2023.11.07
        # 如果新增任务获得通过, 任务的状态会改成 TaskResultCode.taskReady ,这样 aivWcMmap就可以能知 wc模块下载任务的文件做准备工作。
        self.setTaskResultCode(TaskResultCode.taskReady) 
        # logger.warning('当前的任务内容是：{}'.format(self.task))
        # self.state = TaskState.taskReady
        self.setTaskState(TaskState.taskReady)

    # 把任务内容更新到 任务的共享内存中-------2023.10
    async def updateTaskInfo(self):
        if self.task is None:
            return
        
        # logger.warning('任务进入抢单模式！')
        # taskDict['test'] = '这是taskShip的'
        _write_mmap(self.taskMMAP,self.task,taskMMAPStart) # taskMMAPStart 是从哪个字节开始读,默认是 10
        # print('aivmmap.py 写入Task共享内存成功！')
        # 写入标志位
        self.setTaskState(TaskState.taskShip) #开始给各 ship 模块抢单

    def cancelTask(self):
        '''
            取消任务
            * 此函数由wc.py模块调用,前端发出停止任务指令,则触发此函数
            * 此函数把任务共享内存清空,标志位也相应变成 taskNone
        '''
        if self.task is None:
            return
        
        self.setTaskResultCode(TaskResultCode.taskUser)
        # 中间可以有其它操作, 比如返回任务状态给前端
        self.task = None

        # 清空任务的共享内存空间---------------
        self.taskMMAP.seek(0)
        for i in range(taskMMAPLen):
            self.taskMMAP.write(b'\x00')
        self.taskMMAP.flush()

    async def taskProExit(self):
        '''
            用户取消任务
            ship模块,看到取消指令,应该马上停止任务,并退出进程
        '''
        self.setTaskState(TaskState.taskProExit) #通知其它进程退出

        self.aivSys.killMe('AivWcMmap')
        # await asyncio.sleep(0.01)
        # logger.debug('AivWcMmap: 进程退出.')
        # os._exit(0)

    async def run(self):
        while True:
            
            await self.checkTaskFinished()

            state = self.getTaskState() #读出newTaskMMap共享内存的状态,如果是 taskNone 就写入
            # logger.warning('AivWcMmap: run() 检测任务情况. state == {}'.format(state))

            if (state == TaskState.taskNone) :
                pass
                # if len(self.taskList) >0 :
                #     key, value = next(iter(self.taskList.items()))
                #     self.setTaskState(TaskState.taskNew)
                #     self.writeTask(value) # 把任务写入共享内存,等待aivprocess.py的 aivPro检查是否可以接收
                #     del self.taskList[key] #把取出的项从 taskList 中删除

            # elif state == TaskState.taskEnd: # 任务完成消息
            #     task = self.readTask()
            #     logger.warning('AivWcMmap: 任务被拒绝,任务内容是：{}'.format(task))
            #     if self.onTaskFinished is not None:
            #         self.onTaskFinished(task)
            #         self.clearTask() # 清除共享内存中的任务数据

            elif state == TaskState.taskProExit:  # 用户取消任务,则马上退出进程。不管 wc 模块任务运行到什么程度
                logger.warning('AivWcMmap: 用户取消任务! AivWcMmap 进程退出.')
                await asyncio.sleep(0.1)
                os._exit(0)    

            elif state == TaskState.taskReady: #准备阶段 (这一阶段需要下载任务内指定的文件)
                await self.checkFileDownload()
                await self.checkTaskReady()

            elif state == TaskState.taskFinished : 
                ''' 2023.11
                    ship模块执行完成后,把共享内存中的状态设为 taskFinished 
                    ship 模块执行的结果, 可能成功 也可能失败。结果保存在 task['result'] 中的 ['code'] 和 ['msg'] 中
                    aivwc 模块应该读出 task['result'] 中的值,如果是 TaskResultCode.taskOk (200),则需要把生成的结果文件传给js端
                    如果 task['result']中记录的 'code' 值是非 200值,表明执行失败。则可以直接返回结果给 js端
                '''
                logger.debug('aivc: 收到ship模块执行完成的指令')   
                # 从任务共享内存中读出任务内容
                self.task = self.readTask() # taskMMAPStart 是从哪个字节开始读,默认是 10

                # 触发 任务完成事件
                if self.onTaskFinished is not None:
                    await self.onTaskFinished(self.task)

                self.task = None
                self.setTaskState(TaskState.taskNone)
                

            await asyncio.sleep(0.2)

    # 下载文件完成,设置任务中的文件相应的下载状态
    async def downloadFileFinished(self,file):
        '''
            修改文件的下载状态
            wc.py 模块下载完文件,调用此函数,修改对应的file的属性'isDownload'设为True
            通过file的 'path'属性判断是否相等
            'path'属性是从js端发过来,值一般是： "blob:http://192.168.2.226:5173/ec82ead4-60e1-4281-a852-d221387cc6e4"
        '''
        if file is None:
            logger.error('下载完成的文件为空！')
            return
        
        # print('准备把文件状态改变! file ==> ',file)
        path = file['path']

        
        # 对比所有需要下载的文件,找到这个文件,把它的 'isDownload'属性设为 True
        if self.task is None:
            return
        
        for param in self.task['paramIn']:
            if param['bsonType'] == 'file':
                files = param['files']
                if files is None:
                    continue
                
                for taskFile in files:
                    if taskFile['path'] == path:
                        # print('找到要修改状态的文件了：==> ',taskFile)
                        taskFile['isDownload'] = True
                        return    
        

    async def checkFileDownload(self): # run() 的协程函数
        ''''
            查询是否有需要下载的文件,如果有,则触发下载函数
            * 通过不断检测 task 中的 ParamIn 参数列表中的 files 字段(如果有的话)
            * files字段是一个 file 数组,file 对象有一个属性是'isDownload',如果是None表示没下载,False表示正在下载,True表示下载完成
            * 当前函数是run()函数中的一个协程任务,通过不断检测 files文件数组的所有文件状态,发现有需要下载的,
            * 则触发 onDownloadFile() 函数,由 wc.py 模块下载相应的文件 2023.10
        '''
        if self.task is None:
            return
        
        # logger.warning('开始检测文件下载111：{}'.format(self.task))
        
        def _checkHaveDownloading(): #查询是否有正在下载的文件?
            # logger.warning('开始检测文件_checkHaveDownloading()')
            for param in self.task['paramIn']:
                if param['bsonType'] == 'file':
                    files = param['files']
                    if files is None:
                        continue
                    
                    for file in files:
                        if file['isDownload'] == False: #如果是 None,则表明此文件还没开始下载,如果是Fale值,则表明正在下载(但未下载好),True表明下载完成
                            return file
            
            return None
        
        
        def _checkHaveFileDownload(): #查询参数的文件列表中是否有需要下载的文件？
            # isHave = False
            # logger.warning('开始检测文件 _checkHaveFileDownload()')
            for param in self.task['paramIn']:
                if param['bsonType'] == 'file':
                    files = param['files']
                    if files is None:
                        return None
                    
                    for file in files:
                        if file['isDownload'] is None: #如果是 None,则表明此文件还没开始下载,如果是Fale值,则表明正在下载(但未下载好),True表明下载完成
                            # 判断服务端是否有此文件,如果有的话,则不用下载,直接设置成已下载完成
                            if not _checkFileExists(file):
                                return file
            return None
        
        def _checkFileExists(file): # 检查文件是否已经下载在本地磁盘? 2023.10 
            # logger.warning('开始检测文件 _checkFileExists()')

            filename = self.getFilePath(file)
            if (filename!='') and  os.path.exists(filename):
                os.utime(filename, (0, time.time())) # 更新文件的最后最后修改时间为现在(预防这个文件长期不被访问,被系统自动清除 2023.11)
                # 在 AivMainPro 的 runCheckFile()函数中,有一个功能是自动清理超过一定时间（默认是1天）的文件,是以最后修改时间判断 2023.11

                file['isDownload'] = True #如果检查服务端的磁盘已经存在此文件,则直接把下载标识'isDownload'设置为True(表示已经下载完成) 2023.10
                return True
            else:
                return False  

        
        # 1、先查询是否有正在下载的文件? 如果有则直接返回
        if _checkHaveDownloading() is not None: #检查是否有文件正在下载(如果下载完,就不用下载)
            # logger.warning('_checkHaveDownloading 检测有文件正在下载!')

            return
        
        # 2、如果没有正在下载的文件,则查询是否有需要下载的文件?
        file = _checkHaveFileDownload()
        
        if file is not None:
            # logger.warning('检测准备要下载的文件, file ==>{}'.format(file))
            file['isDownload'] = False #先把标识设置为 False (表示准备下载) 2023.10
            await self.onDownloadFile(file) # 触发 onDownloadFile(),开始下载文件


    
    async def checkTaskReady(self): # run()函数的协程函数，查询任务是否准备好
        '''
            检测任务是否准备好
            * 只有任务的所有需要的文件都下载到本地,任务才算准备好。
        '''
        # 首先查询任务需要的文件是否下载完成
        if self.task is None:
            return False
        # logger.warning('开始检测文件 checkTaskReady()')
        
        # isReady = True
        for param in self.task['paramIn']:
            if param['bsonType'] == 'file':
                if param['files'] is None:
                    continue

                for file in param['files']:
                    # 只要有一个文件没有'isDownload'标识,或标识为False,都表明任务没准备好（文件没下载完成！）
                    if file['isDownload'] is None or (file['isDownload']==False):
                        return False

        logger.debug('文件都下载完成了！ 准备进入抢单模式')
        # 如果检测发现所有的参数都准备好了（需要下载的文件都下载完成）,则把状态从准备状态,转到 ship 任务运行状态
        await self.updateTaskInfo()      


    async def checkTaskFinished(self):
        '''
            查询任务是否完成
            如果任务完成,则触发 onTaskFinished() 事件
        '''
        taskState = self.getTaskState()
        if taskState != TaskState.taskFinished:
            return

        logger.debug('aivc: 任务完成！')   
        # 从任务共享内存中读出任务内容
        self.task =  _read_mmap(self.taskMMAP,taskMMAPStart,0,True)  # taskMMAPStart 是从哪个字节开始读,默认是 10

        # 触发 任务完成事件
        if self.onTaskFinished is not None:
            await self.onTaskFinished(self.task)

        self.task = None
        self.setTaskState(TaskState.taskNone)


