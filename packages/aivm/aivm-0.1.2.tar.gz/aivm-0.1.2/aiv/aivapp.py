'''
### 初始化Aiv应用全局参数
* 全局路径、Logger、环境变量等设置
* 无论是AivC、Aiv Ship模块,都可以使用
* _aiv_app_init() 函数必须早于任何模块调用,在任何 import 之前调用,否则有可能路径失效,
报找不到模块,或import错误. (2023.8)
'''
import os,sys


logger = None

def _aiv_app_init(exe_file :str, isMain=False, loglvl=None):
    '''
    ### 注册Aiv app的模块 
    * 参数:
        exe_file : 是主模块路径
        isship : 是否是ship模块,如果是ship模块,将被以子进程加载,ship模块的工作目录会被设为 ship上级目录。
                原因是ship上级目录里,包含有公共的python模块以及其它公共的数据文件夹(如mode,data,bin目录)
                如果ship模块要使用自己的自定义包,则可以复制到ship模块目录下(比如cv2模块)
        loglevel : 默认是Debug,也可以输入0~50之间的数值,也可以用 aiv.aivlog.AivLogLevel 的值:
            Enum = (AIV=2,TRACE=5,DEBUG=10,INFO=20,SUCCESS=25,WARNING=30,ERROR=40,CRITICAL=50)
    * 此函数在其它代码前(在 import 前运行)
    * 设置路径/环境变量/日志等级等
    * 强制设置工作路径为当前执行程序的上一级目录
    '''
    LOCAL_PATH = os.path.dirname(os.path.abspath(exe_file))
    # parent_path = os.path.dirname(LOCAL_PATH) #获取上级目录
    
    #如果上级目录的平级目录下有 lib目录,则说明当前模块是子进程模块 (lib的目录放的是python模块)
    # is_child = False
    # if os.path.exists(os.path.join(parent_path,'lib')): 
    #     is_child = True
    #ship模块的工作目录会被设为 ship上级目录。原因是ship上级目录里,包含有公共的python模块以及其它公共的数据
    if isMain:
        os.chdir(os.path.join(LOCAL_PATH, '..')) #设置当前目录为执行文件的上级目录

    #初始化导入包目录（系统包、用户自定义包）--------------
    # 指定"lib"目录作为的 python 系统库目录(Aiv系统包库), import 搜索的目录
    sys.path.insert(0,'lib')     

    #把执行文件所在的文件夹也加入sys.path，目的是执行文件可以优先从本目录下导入包（优先于系统指定的包）
    # sys.path.insert(0,os.path.basename(LOCAL_PATH)) #插入 sys.path 的顺序不能调换
    #---------------------------------------------------
    # 如果目录下有 venv 目录,则把 venv/Lib/site-packages 加入 搜索路径
    currPath = os.getcwd()
    if os.path.exists(os.path.join(currPath,'venv')):
        sys.path.insert(0, os.path.join(currPath,'venv/Lib/site-packages')) #添加到第一位

        # 把当前目录下的 venv/Scripts/ 目录添加到环境路径(与sys.path不一样,sys.path是python的搜索路径, os.getenv('PATH')是可执行程序、dll的搜索路径)
        envPath = os.getenv("PATH")
        scriptsPath = os.path.join(currPath,'venv/Scripts/')
        if scriptsPath not in envPath:
            os.environ["PATH"] = envPath + os.pathsep + scriptsPath

    
    #初始化Aiv的log类（基于loguru)------------------------
    import aiv.aivlog as aivlog 
    global logger
    logger = aivlog._aiv_log_init(loglvl)
    #aivlog._aivlog_change(aivlog.AivLogLevel.DEBUG)
    # logger.debug('Python版本: {}'.format(sys.version))  
    #---------------------------------------------------
    

    # 解决导入  cv2 时的问题-----------------------------
    import site
    site.USER_SITE = os.path.join(os.getcwd(),'lib')
    site.USER_BASE = os.path.join(os.getcwd(),'Scripts') #可以创建，用于存放脚本
    #--------------------------------------------------

    # windows下临时添加路径到系统的 Path 变量中----------------
    #这是为了 动态载入  *.pyd *.so *.dll 文件的路径 ，linux 为 os.environ['LD_LIBRARY_PATH'] site.USER_BASE
    binpath = os.path.join(site.USER_SITE,'bin')
    if not 'PATH' in os.environ:
        os.environ['PATH'] = binpath + ";"
    else :
        os.environ['PATH'] = binpath + ";"+ os.environ['PATH']

    #设置 PythonPath 路径-----------------------------------
    # os.environ['PYTHONPATH'] = '' #设为空，则是屏蔽系统设置的 PYTHONPATH (如果有的话)
    #-------------------------------------------------------

    #调试使用。必须要把日志级别设置为 AIV 级别才执行
    if aivlog.log_check(logger,aivlog.AivLogLevel.AIV):
        _aivpath() #打印路径
        _aivmodules() #打印已导入模块

    logger.debug('初始化Aiv参数完成！')


#读入系统导入路径，调试使用-----------------------------------------------------
def _aivpath():
    logger.debug('\n env path 路径参数: ------------------------------------------------\n')
    for  (key,value) in os.environ.items():
        logger.debug("env path >> {} : {}".format(key,value))

    logger.debug('\n sys.path 路径参数: ------------------------------------------------\n')
    for  value in sys.path:
        logger.debug("sys.path >> {}".format(value))

    #-------------------------------------------------------------
#读取已导入的模块列表。调试使用-----------------------------------------------------
def _aivmodules():
    logger.debug('\n sys.modules 参数: -----------------------------------------------\n')
    for  (key,value) in sys.modules.items():
        logger.debug("modules >> {} : {}".format(key,value))
#-------------------------------------------------------------


if __name__ == "__main__":
    _aiv_app_init(__file__) # test

