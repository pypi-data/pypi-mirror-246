import sys

from  enum import Enum,EnumMeta

#只在以from 模块名 import *形式导入模块时起作用，而以其他形式，
# 如import 模块名、from 模块名 import 成员时都不起作用

#官网： https://loguru.readthedocs.io/en/stable/api/logger.html#file

#add(sink, *, level='DEBUG', format='<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | 
# <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>
#  - <level>{message}</level>', filter=None, colorize=None, serialize=False, backtrace=True, 
# diagnose=True, enqueue=False, catch=True, **kwargs)[source]

# TRACE=5,DEBUG=10,INFO=20,SUCCESS=25,WARNING=30,ERROR=40,CRITICAL=50

# Python 的枚举-------------
class AivLogLevel(Enum): 
    AIV,TRACE,DEBUG,INFO,SUCCESS,WARNING,ERROR,CRITICAL = 2,5,10,20,25,30,40,50 #最小值不要小于 1

def _find_num(lis,num): #从列表lis或 Enum 找出最接近val的数,
    li = []
    if isinstance(lis,EnumMeta):
        for en in lis:
            li.append(en.value)
    else:
        li = lis
    from heapq import nsmallest
    return nsmallest(1, li, key=lambda x: abs(x-num)) #返回值是一个列表


def _aiv_log_init(level=None):
    '''
    ### 初始化log对像
    * Aiv 使用loguru包管理日志对象。本函数对loguru 的logger对象属性设置,并增加了Aiv级别的日志
    * Aiv 还增加了一个动态修改日志级别的函数,可以在不退出程序的情况下,修改日志级另
    * 参数 : level
        可以传一个数字值,也可以传AivLogLevel对象的值
        如果是数字值,将匹配最接近的日志级别
    ## _aiv_log_init() 函数要在别的模块使用'import loguru'之前运行,不然在这里的设置不会生效
    * 其它模块只要使用 'from loguru import logger' 使用即可,logger是Aiv配置过的。
    '''   
    if level is None:
        level = AivLogLevel.DEBUG
    lev = level
    if isinstance(level,int):
        #找出最相近的值
        val = _find_num(AivLogLevel,level) # 返回的是最接近的值列表,[0] 是最接近的
        lev = AivLogLevel(val[0])
        
            

    #过滤日志的函数
    def stdout_filter(record):
        #可以在这里过滤特定模块的日志，上传服务器，或者发送邮件给开发者
        return  record["level"].no < AivLogLevel.ERROR.value

    #过滤日志的函数
    def stderr_filter(record):
        #可以在这里过滤特定模块的日志，上传服务器，或者发送邮件给开发者
        return record["level"].no >= AivLogLevel.ERROR.value 

    from loguru import logger 
    #global logger
    #logger = _logger
    if not hasattr(logger,'AIV'):
        logger.level(name="AIV", no=2, color="<fg #00005f>", icon="🐞")
    stdout_handler = {"sink": sys.stdout, 
                    "level": 1, #这里要设置最小值,避免有些信息被过滤掉***
                    "format":"<green>{time:YYYY-MM-DD at HH:mm:ss}</green> <level>|{level:^8}| <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>| {message}</level>", 
                    "filter": stdout_filter
                    }

    stderr_handler = {"sink": sys.stderr,
                        "level": "ERROR",
                    "format":"<green>{time:YYYY-MM-DD at HH:mm:ss}</green> <level>|{level:^8}| <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>| {message}</level>", 
                    "filter": stderr_filter
                    }
    #配置日志
    logger.configure(handlers=[stdout_handler, stderr_handler])
    #logger.bind(user_id="aivgan")
    #自定义日志级别
    

    logger.log('AIV','这是AIV消息...')
    def aivlog(msg):
        logger.log("AIV",msg)

    #直接在loguru 的 logger 类上，添加方法 aiv()，函数地址指向  aivlog()---------
    if not hasattr(logger,'aiv'):
        setattr(logger,'aiv',aivlog) 
        #if hasattr(logger,'aiv'):
        #    logger.debug('设置了方法aiv()')
    #------------------------------------------------------------------------

    #利用反射修改 loguru._core 的属性 min_level
    _core = _get_core(logger)
    if _core:
        setattr(_core,'min_level',lev.value) #初始化为指定的日志级别
            
    else:
        logger.error('没有找到 loguru._core 对象')

    return logger
    
    #通过反射取得logger的属性_core对象
def _get_core(logger):
    _core = None
    if hasattr(logger,'_core'):
        _core = getattr(logger,'_core')   
    return _core        
     
#如果loguru中设置的level大（越大越严重的消息）
def log_check(logger,level):
    '''
    # 功能: 检查输入的级别与系统预设的日志级别大小,小于即返回True
    # 参数：需要比较的日志级别, 可以是AivLogLevel类, 或者是0--50之间的数值
    # 用途: 如果一些代码块需要调试, 而又希望在正式发布后不运行,可以使用些函数检查。
    '''
    lev = level
    if isinstance(level,int):
        #找出最相近的值
        val = _find_num(AivLogLevel,level) # 返回的是最接近的值列表,[0] 是最接近的
        lev = AivLogLevel(val[0])

    _core = _get_core(logger)
    min_level = 50
    if _core is not None:
        min_level = getattr(_core,'min_level')
    return min_level <= lev.value

#在应用运行期间，动态改变此值。可以控制输出日志
def _aivlog_change(logger,level):
    '''
    # 功能：动态修改日志级别
    # 参数：需要修改日志级别, 可以是AivLogLevel类, 或者是0--50之间的数值
    # 用途: 在某些场合,需要在不退出软件情况下,修改日志级别. 以便输出有效的信息.
    '''
    lev = level
    if isinstance(level,int):
        #找出最相近的值
        val = _find_num(AivLogLevel,level) # 返回的是最接近的值列表,[0] 是最接近的
        lev = AivLogLevel(val[0])

    logger.debug('接收到修改日志级别指令: {}'.format(lev.value))
    _core = _get_core(logger)
    if _core is not None:
        print('level 值：',lev.value)
        setattr(_core,'min_level',lev.value)


def test_log(logger):
    if logger is None:
        print('loguru未初始化！')
    logger.trace("这是Trace信息")
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
    logger.success("success执行事情")
    logger.aiv("自定义的日志级别显示")



if __name__ == "__main__":
    # print(type(Enum))
    # def findnum(lis,val): #在列表lis找出最接近val的数
    #     li = []
    #     import enum
    #     if isinstance(lis,enum.EnumMeta):
    #         for en in lis:
    #             li.append(en.value)
    #     else:
    #         li = lis
    #     from heapq import nsmallest
    #     return nsmallest(1, li, key=lambda x: abs(x-val))
    
    # val = findnum(AivLogLevel,24)
    # print('日志级别是：',AivLogLevel(val[0]))

    #Test--------
    logg = _aiv_log_init()
    test_log(logg)
    _aivlog_change(logg,26)
    print('------------------------------------------------------------------')
    test_log(logg)
