
import os,json,sys,time
from collections import namedtuple
from loguru import logger
import psutil,platform #用 pip3 install psutil 才能安装



#--------------------------------进程IPC数据共享： 内存共享--------------------------------------------
#----------------------------------------------------------------------------------------------------
import mmap
def _create_mmap(name,len=1048576):
    # leng 默认是 1048576 = 1M

    #if mmap_conf is None:
    mmap_conf = mmap.mmap(0, len, access=mmap.ACCESS_WRITE, tagname=name)
    
    return mmap_conf

# 把配置文件（dic)写入进程共享内存块中的数据
def _write_mmap(mmaps,data,start=0,lens=0,tojson=True): # mmaps 是共享内存的指针,一个应用中可能有多块
    '''
    * 参数 lens ,指定共享内存长度
    * 参数 tojson ,表明是否要经json转换
    * 参数 data 中,不能包含 '\x00' 空白字符,否则在读取阶段，会读取不完整
    '''
    if tojson:
        jsonstr = _aiv_json(data)
        
    else:
        jsonstr = data
    jsonlen = len(jsonstr)    
    if lens!=0:
        if jsonlen>= lens:
            logger.warning('配置文件超过长度{}，超出内存长度！自动截断'.format(lens))

    #logger.debug('接收到写入长度为：{}参数到共享内存：\n{}'.format(jsonlen,data))
    mmaps.seek(start)
    mmaps.write(bytes(jsonstr,encoding='utf-8'))
    mmaps.flush()

    #在文件末尾添加结束符 '\x00'-----------------
    mmaps.write(b'\x00')
    mmaps.flush()
    #logger.debug('写长度为：{} 的Json格式参数到共享内存：\n{}'.format(jsonlen,jsonstr))
    

#从进程内存块中,读出配置文件 (json字符串),转为 dic 返回
def _read_mmap(mmaps,start=0,leng=0,return_dict=False):
    '''
    ### 读取共享内存中的数据
    * 在写入阶段,写入的数据不能包含 '\x00' 空白字符,否则在读取阶段，读取不完整
    '''
    if mmaps is None:
        logger.error('未建立配置文件内存区域')
    mmaps.seek(start)
    # 把二进制转换为字符串
    buffer = bytearray()
    
    while True:
        chr = mmaps.read(1) #这里的 read()函数返回值是 bytes 
        if not chr:
            break
        
        if chr == b'\x00': # 如果是 空字符,标明读到尽头,chr是bytes类型 ，所以比较时, b'\x00' 前面的b 不能少
            #logger.warning("找到'\x00'空字符串")
            break
        buffer += chr # b'\x00' 字符不能加到文件末尾,不然 json 不能解析
        

    data = None
    if len(buffer)>0:
        data = buffer.decode('utf-8').rstrip()

    #info_str = mmaps.read().translate(None, b'\x00').decode(encoding='utf-8')
    if data is not None:
        pass
        #logger.debug('_read_mmap()从共享内存读长度为：{}的参数\n{},'.format(len(data),data))

    if data is not None and return_dict:
        return json.loads(data) # 从Json 转成 dic 并返回     
    else:
        return data   


#自定义的 python ==> Json 类,可以处理 fun之类的数据
import datetime,types
class AivJson(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            #print("MyEncoder-datetime.datetime")
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        if isinstance(obj, int):
            return int(obj)
        elif isinstance(obj, float):
            return float(obj)
        elif isinstance(obj, types.FunctionType) or isinstance(obj, types.MethodType):
            pass #返回 None 或 null
        #    return obj.tolist()
        else:
            return super(AivJson, self).default(obj)

def _aiv_json(data):
    '''
        ### Python 数据转 Json
        * 支持 dict/list/tub/datetime/python class (function,byte,str)
        * 直接显示中文 ensure_ascii=False
        * 去除 , : 前后空格separators=(',',':') 
    '''
    return json.dumps(data,cls=AivJson,ensure_ascii=False,separators=(',',':'),indent=4) 

import hashlib

def _calculate_md5(file_path):
    '''
        计算小文件的md5值 2023.10
        * 小于100M可以用它计算
        * (这是百度Ai自动生成的代码)
    '''
    md5_hash = hashlib.md5()
    with open(file_path, 'rb') as f:
        # 读取文件的块大小
        chunk_size = 1024 * 1024
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            md5_hash.update(chunk)
    return md5_hash.hexdigest()

def _calculate_large_file_md5(file_path):
    '''
        计算大文件的md5值 2023.10
        * 大于100M用它计算
        * (这是百度Ai自动生成的代码)
    '''
    file_size = os.path.getsize(file_path)
    md5_hash = hashlib.md5()
    with open(file_path, 'rb') as f:
        # 计算每个块的大小（以MB为单位）
        chunk_size = 1024 * 1024
        start_pos = 0
        end_pos = chunk_size
        while start_pos < file_size:
            if end_pos > file_size:
                end_pos = file_size
            chunk = f.read(end_pos - start_pos)
            if not chunk:
                break
            md5_hash.update(chunk)
            start_pos += chunk_size
        return md5_hash.hexdigest()

def getFileMd5(fileName):
    '''
        获取文件的Md5值
        * 对外使用此函数即可
        * 可以自动根据文件大小,调用不同的函数获取md5值
    '''
    fileSize = os.path.getsize(fileName)
    if fileSize/1024/1024 > 100:
        return _calculate_large_file_md5(fileName)
    else:
        return _calculate_md5(fileName)


def getFileInfo(fileName,reName=False):
    '''
        返回一个文件信息对象 2023.10
        * 如果此文件不存在,则只返回文件的路径、文件名在内的信息
        * 如果文件存在,则返回文件的详细信息,包括文件大小、创建时间、访问时间、文件类型等
        * 如果设置reName参数为True,则会计算文件的md5值,并用md5值重新为文件命名
    '''
    fileInfo = {
        'isDownload': None, # None表示文件没下载, False 表示正在下载, True 表示下载完成
        'path': fileName,
        'name': os.path.basename(fileName),
        'size': 0,
        'md5' : None,
        'lastModified': None,
        'lastModifiedDate': None,
        'type': None,
        'webkitRelativePath': ''
    }

    if os.path.exists(fileName):
        import mimetypes
        mime_type, encoding = mimetypes.guess_type(fileName)
        fileInfo['type'] = mime_type
        fileInfo['md5'] = getFileMd5(fileName)
        fileInfo['size'] = os.path.getsize(fileName)
        fileInfo['createDate'] =  int(os.path.getctime(fileName))
        fileInfo['lastModified'] = int(os.path.getmtime(fileName))
        fileInfo['lastModifiedDate'] = int(os.path.getatime(fileName))

        if reName:
            md5 = fileInfo['md5']
            filePath = os.path.dirname(fileName)
            # print('filePath==',filePath)
            newFileName = os.path.join(filePath,md5+os.path.splitext(fileName)[1])
            # print('newFileName==',newFileName)
            os.rename(fileName,newFileName)
            fileInfo['path'] = newFileName
            fileInfo['name'] = os.path.basename(newFileName)

    return fileInfo

def getDirName(fileName):
    '''
        获取文件所在的文件夹名
    '''
    folder_name = os.path.basename(os.path.dirname(fileName))  # 获取文件夹名
    return folder_name

def createQrCode(data,outFileName,logoFile=None):
    ''' 2023.11
        生成二维码
        根据数据data, 生成一个二维码文件,并保存到 outFileName 目录
        logoFile 参数: 决定是否要生成一个带 logo 的二维码
    '''
    import qrcode,json
    from PIL import Image

    # 创建QRCode对象
    qr = qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2
    )

    # 添加数据到QRCode对象中
    # data = {'cmd': 'test', 'data': 'id_12345678'}
    txt = json.dumps(data)
    qr.add_data(txt)
    qr.make(fit=True)

    # 创建Image对象，并将QRCode对象转化成Image对象
    img = qr.make_image(fill_color="black", back_color="white").convert('RGBA')

    if logoFile is not None:
        # 打开logo图片，并将其resize
        # logo = Image.open("E:/QuickSoft/Demo/Aiv图标/紫色/圆角图标(108x108).png")
        logo = Image.open(logoFile)
        logo = logo.resize((80, 80))

        # 计算logo位置
        img_w, img_h = img.size
        logo_w, logo_h = logo.size
        logo_pos = ((img_w - logo_w) // 2, (img_h - logo_h) // 2)

        # 将logo图片添加到QRCode图片中
        img.paste(logo, logo_pos, logo)

    # 保存QRCode图片
    try:
        img.save(outFileName)
    except Exception as e:
        logger.warning('生成二维码出错 => {}'.format(e))


# Aiv系统操作类
class AivSys:
    
    # 参数isMain控制当前类是自主获取数据,还是通过 共享内存 获取数据
    def __init__(self,isMain=False) -> None:
        self.isMain = isMain
        self.confFile = ''  #配置文件 aiv.ini
        self.userName = None
        self.deviceName = ''
        self.deviceId = ''
        self.deviceBingCode = '' #绑定设备的值
        self.aivDataDir = '' # aiv的数据目录
        self.aivTempDir = '' # aiv的临时目录, 在'AivData'目录下,建立temp目录,专门用来下载客户端的图片存放
        self.aivOutDir = ''  # aiv的输出目录
        self.aivConfDir = '' # 配置文件目录
        self.aivVersion = ''
        self.pyVersion = ''
        self.aivSysInfo = ''
        self.runTime = ''

        if isMain:
            self.aivVersion = '1.0.2' # Aiv 的系统版本    
            self.initSysInfo()
            self.initPyInfo()
            self.initDataPath()
            self.updateSysRunTime()
            # self.initDeviceInfo()
            self.deviceId = self.initDeviceId()

        
    def initDeviceId(self):
        ''' 2023.12
            用psutil获取 网卡的mac地址, 并用md5加密
            这个函数在 window、linux、 Mac下都可以使用
            用于做电脑的唯一标识: deviceId
        '''
        import psutil
        # 获取所有网络接口信息
        net_if_addrs = psutil.net_if_addrs()
        # 遍历所有网络接口,取第一项 2023.12
        i = 0
        mac = None
        if len(net_if_addrs) >0 :
            for interface, addrs in net_if_addrs.items():
                i += 1
                # 遍历当前网络接口的所有地址
                for addr in addrs:
                    # 如果地址类型是MAC地址
                    if addr.family == psutil.AF_LINK:
                        # 输出当前网络接口的MAC地址
                        mac = addr.address
                        # print(f"Interface {interface} MAC address: {addr.address}")
                        break

                if i>0 : #只取第一项
                    break

            import hashlib
            md5 = hashlib.md5() # 用md5加密
            md5.update(mac.encode('utf-8'))
            return md5.hexdigest()
        else:
            return None

    def getSysInfo(self):
        
        sysInfo = {
            'userName' : self.userName,
            'deviceName': self.deviceName,
            'deviceId' : self.deviceId,
            'deviceBingCode': self.deviceBingCode,
            'dataDir':self.aivDataDir,
            'tempDir': self.aivTempDir,
            'outDir' : self.aivOutDir,
            'confDir' : self.aivConfDir,
            'aivVersion': self.aivVersion,
            'pyVersion': self.pyVersion,
            'sysInfo': self.aivSysInfo,
            'sysRunTime': self.runTime
        }
        return sysInfo
    
    def setSysInfo(self,dic):
        if self.isMain:
            return
        
        self.userName = dic['userName']
        self.deviceName = dic['deviceName']
        self.deviceId = dic['deviceId']
        self.deviceBingCode = dic['deviceBingCode']
        self.aivDataDir = dic['dataDir']
        self.aivTempDir = dic['tempDir']
        self.aivOutDir = dic['outDir']
        self.aivConfDir = dic['confDir']
        self.aivVersion = dic['aivVersion']
        self.pyVersion = dic['pyVersion']
        self.aivSysInfo = dic['sysInfo']
        self.runTime = dic['sysRunTime'] 

    def initDeviceInfo(self):
        import platform
        self.deviceName = platform.node()

        if not os.path.exists(self.confFile):
            with open(self.confFile, 'w') as f:
                    pass
            
        
        with open(self.confFile, 'r') as f:
            for line in f.readlines():
                param = line.split()
                if len(param)>0:
                    if param[0]== 'userName':
                        if len(param)>1:
                            self.userName = param[1]
                        else:
                            self.userName = '[notSetUserName]'
                    if param[0]== 'deviceId':
                        if len(param)>1:
                            self.deviceId = param[1]

        if self.deviceId=='':
            with open(self.confFile, 'a') as f:
                f.write('\n')
                f.write('# deviceId  自动生成,无需手动修改 \n')

                import uuid
                self.deviceId  = str(uuid.uuid4())
                self.deviceId = self.deviceId.replace('-','')
                f.write('deviceId  {}\n'.format(self.deviceId))

        if self.userName =='':
            with open(self.confFile, 'a') as f:
                f.write('\n')
                f.write('# userName  后面填入你的用户名\n')
                f.write('userName  \n')

        if self.userName== '[notSetUserName]':
            logger.warning('未设置用户名, 必须重新设置! 目录 aivData/conf/aiv.conf 下设置。')

        # logger.warning('用户名是：{}'.format(self.userName))

        # import configparser

        # # 读取ini文件
        # config = configparser.ConfigParser()
        # config.read(self.confFile)

        # def getValue(config,section,key):
        #     if not config.has_section(section):
        #         config.add_section(section)
            

        # # 读取指定的section中的option
        # if config.has_section('device'):
        #     self.deviceId = config.get('device', 'deviceId')
        #     self.userName = config.get('device', 'userName')
        # else:
        #     config.add_section('device')

        # # 生成唯一设备号. 在websocket中,用于区分同一用户下的不同设备
        # if self.deviceId == '':
        #     import uuid
        #     self.deviceId  = str(uuid.uuid4())
        #     self.deviceId = self.deviceId.replace('-','')
        #     if not config.has_section('device'):
        #         config.add_section('device')
        #     # 修改option的值
        #     config.set('device', 'deviceId', self.deviceId)
            

        # if self.userName == '':
        #     if not config.has_section('device'):
        #         config.add_section('device')
        #     config.set('device', 'userName', self.userName)

        # with open(self.confFile, 'w') as f:
        #         config.write(f)

        # logger.warning('本机编号是：{} ,设备号是：{}, 用户名是：{}'.format(self.deviceName, self.deviceId,self.userName))



    
    # 查询aiv数据目录是否建立,如果没有就建立
    def initDataPath(self):
        ''' 2023.09
            初始化AIV程序路径
            先要建立AivData目录,这是主目录,必须建立在20G空间的磁盘中。默认是建在D盘下
            如果D盘空间不足或没有D盘,则从C盘检查。找到合适的磁盘就创建 AivData目录
            接着依次建立AivData/temp , AivData/out, AivData/conf 目录
        '''
        if not self.isMain:
            return
        
        freeDisk = 30 #30G空间

        def checkPart(d,isCheck=None):        
            aivDir = d + 'AivData'
            if isCheck is None: #如果不要求检测磁盘空间,则直接建立aiv目录并返回 
                if os.path.exists(aivDir) and os.path.isdir(aivDir) : #如果已经建立 aiv目录,则不检查当前磁盘是否足够空间。因此，也可以手动创建 aiv 目录
                    self.aivDataDir = aivDir
                    return True
                else:
                    os.mkdir(aivDir)
                    self.aivDataDir = aivDir
                    return True

            # 如果是要检测磁盘空间的情况 ===
            haveDir = False
            p = psutil.disk_usage(d) #D盘
            tempDisk = int(p.free/1024/1204/1024) #查找可用空间
            if tempDisk >= freeDisk: # >= 30G
                # aivDir = d + 'aiv'
                if os.path.exists(aivDir) and os.path.isdir(aivDir):
                    self.aivDataDir = aivDir
                    haveDir = True
                else:
                    os.mkdir(aivDir)
                    self.aivDataDir = aivDir
                    haveDir = True
            else:
                logger.warning('磁盘：{} 空间不足{} GB, 不能安装 Aiv 数据 AivData 目录'.format(d,freeDisk) )

            return haveDir


        disk = psutil.disk_partitions()
        partCount = len(disk)
        # for i in range(partCount):
        #     logger.debug('磁盘分区: {}'.format(disk[i][0]))

        
        haveDir = False
        #优先查询D盘
        if partCount>1:
            haveDir = checkPart(disk[1][0],True)
        if not haveDir:
            haveDir = checkPart(disk[0][0],True)

        if not haveDir:
             for i in range(partCount,2): #从E盘开始  
                 haveDir = checkPart(disk[i][0],True)
                 if haveDir:
                     break
                 
        if not haveDir:
            logger.warning('提醒：检测发现磁盘所有分区中，剩余可用空间都不足 {} GB'.format(freeDisk)
                           + ', 请准备充足的磁盘空间！'
                           +'\n 系统将自动在C盘或D盘创建aiv数据 AivData 目录')
            
            #比较c盘和d盘的可用空间
            if partCount>1:
                p = psutil.disk_usage(disk[0][0]) 
                cFree = int(p.free/1024/1024/1024)
                p = psutil.disk_usage(disk[1][0]) 
                dFree = int(p.free/1024/1024/1024)
                if dFree>=cFree:
                    checkPart(disk[1][0])
                else:
                   checkPart(disk[0][0])
            else:
                checkPart(disk[0][0])
        
        if self.aivDataDir is None:
            logger.error('Aiv 的 AivData 目录未创建!')
        else:
            # 创建临时目录
            self.aivTempDir = os.path.join(self.aivDataDir,'temp')
            if not os.path.exists(self.aivTempDir) or not os.path.isdir(self.aivTempDir):
                os.mkdir(self.aivTempDir)
            logger.debug('Aiv 的 AivData 目录是: {}'.format(self.aivDataDir))

            # 创建输出目录
            self.aivOutDir = os.path.join(self.aivDataDir,'out')
            if not os.path.exists(self.aivOutDir) or not os.path.isdir(self.aivOutDir):
                os.mkdir(self.aivOutDir)

            # 创建配置目录
            self.aivConfDir = os.path.join(self.aivDataDir,'conf')
            if not os.path.exists(self.aivConfDir) or not os.path.isdir(self.aivConfDir):
                os.mkdir(self.aivConfDir)
            self.confFile = os.path.join(self.aivConfDir,'aiv.conf')
            if not os.path.exists(self.confFile): #建立一个空的文件 'aiv.ini'
                with open(self.confFile, 'w') as f:
                    pass  # pass什么也不做，只是占位符
                    

    # 获取系统运行时间 ：
    def updateSysRunTime(self):
        if not self.isMain:
            return
        
        from psutil import boot_time
        bootTime = time.time() - boot_time()
        self.runTime = "操作系统已运行 {} 小时".format(round(bootTime/3600,1))
        logger.debug(self.runTime)
        return self.runTime

    # 返回Python 的版本
    def initPyInfo(self):
        if not self.isMain:
            return
        self.pyVersion = 'Python版本: {}'.format(sys.version)
        # pyVesion = 'Python版本: {}'.format(sys.version)
        logger.debug(self.pyVersion)  
        

    #打印系统信息
    def initSysInfo(self):
        if not self.isMain:
            return
        self.aivSysInfo = '操作系统：{} , {} {}, Aiv主进程 pid = {}'.format(sys.platform,
                        platform.system(),platform.release(),os.getppid())
        logger.debug(self.aivSysInfo)

    def createCheckPidThread(self,pids,proName):
        ''' 2023.11
            用线程检测 主进程 pid 是否退出
            用线程检测 主进程 pid是否退出(不是用 asyncio协程,是用threading检测),如果主进程退出,线程也跟着退出 
            pids 参数是一个包含多个 pid 的数组
            proName 是当前的进程名字
        '''
        import psutil
        from loguru import logger
        # print('当前 {} 模块进程 pid = {} , 守护进程 ppid = {}'.format(name,os.getpid(),pid))

        def check(pid):   
            # 获取当前子进程的 主进程ppid是否还运行
            if pid is None:
                return
            
            is_run = True
            try:
                pp = psutil.Process(pid)
            except Exception as e:
                is_run = False
                # logger.warning('守护进程 ppid= {} 已退出！错误是：\n{}'.format(wcPid,e))
                
            if not is_run or not pp.is_running():
                logger.debug('进程 {} 退出.'.format(proName))
                os._exit(0) #在调试模式下,python主进程不退出,本进程可能退出也不成功
        
        def threadCheck():
            while True:
                for pid in pids:
                    check(pid) 
                time.sleep(1)

        from threading import Thread
        Thread(target= threadCheck).start() 

    def killMe(self,proName):
        logger.debug('进程 {} 退出.'.format(proName))
        os._exit(0)
    
    