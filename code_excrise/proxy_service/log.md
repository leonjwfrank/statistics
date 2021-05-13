# logging
## 基础
     # 问题的提出和解决，谷歌论坛，comp.lang.python Usenet
     https://groups.google.com/forum/#!forum/comp.lang.python 
     # 各级别含义
     debug()，  # 细节信息，仅当诊断问题时适用。
        类同logging.info() 函数(当有诊断目的需要详细输出信息时使用 logging.debug() 函数)
     info()，    # 确认程序按预期运行
        程序的普通操作发生时提交事件报告，状态监控和错误调查
         
     warning()， # 表明有已经或即将发生的意外（例如：磁盘空间不足）。程序仍按预期进行
     
     error()    # 由于严重的问题，程序的某些功能已经不能正常执行
        
     exception()
     critical() # 严重的错误，表明程序已不能继续执行
        以上三个是报告错误而不引发异常(如在长时间运行中的服务端进程的错误处理)
    
    # 记录到日志文件
        logging.basicConfig(filename='example.log',level=logging.DEBUG)
        logging.debug('This message should go to the log file')
        logging.info('So should this')
        logging.warning('And this, too')
    
    # 从命令行设置日志级别 --log=INFO
    getattr(logging, loglevel.upper())
     对 basicConfig() 的调用应该在 debug() ， info() 等的前面。因为它被设计为一次性的配置，只有第一次调用会进行操作，随后的调用不会产生有效操作。
    例如: logging.basicConfig(filename='example.log', filemode='w', level=logging.DEBUG)
    
    # 记录变量数据
        logging.warning('%s before you %s', 'Look', 'leap!')
    
    # 更改显示消息的格式
    import logging
        ##  指定要使用的格式, 一般简化的只需要 levelname （严重性）， message （事件描述，包括可变数据），也许在事件发生时显示
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    logging.debug('This message should appear on the console')
    logging.info('So should this')
    logging.warning('And this, too')
    
        # 以上输出
        DEBUG:This message should appear on the console
        INFO:So should this
        WARNING:And this, too
    # 在消息中显示日期/时间
    import logging
    logging.basicConfig(format='%(asctime)s %(message)s')
    logging.warning('is when this event was logged.')
        # 输出 类似于 ISO8601 或 RFC 3339 的时间格式
        2019-12-12 11:41:42,612 is when this event was logged.
     
    # 自定义时间格式，如果你需要更多地控制日期/时间的格式，请为 basicConfig 提供 datefmt 参数
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.warning('is when this event was logged.')
    
        # 输出 
        12/12/2010 11:46:36 AM is when this event was logged.
        datefmt 参数的格式与 time.strftime() 支持的格式相同
    
    
    
## 高级
     
     # 日志库的模块级方法，日志事件信息在 LogRecord 实例中的记录器、处理程序、过滤器和格式化程序之间传递。
     # 通过调用 Logger 类（以下称为 loggers ， 记录器）的实例来执行日志记录
     # 记录器名称可以是你想要的任何名称，并指示记录消息源自的应用程序区域。
     记录器
        有三个目的任务
            首先，它们向应用程序代码公开了几种方法，以便应用程序可以在运行时记录消息。
            其次，记录器对象根据严重性（默认过滤工具）或过滤器对象确定要处理的日志消息。
            第三，记录器对象将相关的日志消息传递给所有感兴趣的日志处理程序
        广泛的方法分为两类：
            配置
                Logger.setLevel() 指定记录器将处理的最低严重性日志消息，其中 debug 是最低内置严重性级别， critical 是最高内置严重性级别。 
                    例如，如果严重性级别为 INFO ，则记录器将仅处理 INFO 、 WARNING 、 ERROR 和 CRITICAL 消息，并将忽略 DEBUG 消息
                Logger.addHandler() 和 Logger.removeHandler() 从记录器对象中添加和删除处理程序对象。
                Logger.addFilter() 和 Logger.removeFilter() 可以添加或移除记录器对象中的过滤器。 
            消息发送
                Logger.exception() 同时还记录当前的堆栈追踪。仅从异常处理程序调用此方法
                Logger.log() 将日志级别作为显式参数。对于记录消息而言，这比使用上面列出的日志级别方便方法更加冗长，但这是自定义日志级别的方法
        
        记录器暴露了应用程序代码直接使用的接口
        # 命名记录器时使用的一个好习惯是在每个使用日志记录的模块中使用模块级记录器
        # 这样的命名的 记录器名称跟踪包或模块的层次结构，并且直观地从记录器名称显示记录事件的位置
        logger = logging.getLogger(__name__)
        
            * getLogger() 返回对具有指定名称的记录器实例的引用（如果已提供），或者如果没有则返回 root 。
            名称是以句点分隔的层次结构。多次调用 getLogger() 具有相同的名称将返回对同一记录器对象的引用。
              
        # 记录器层次结构的根称为根记录器。
            记录器具有 有效等级 的概念。如果未在记录器上显式设置级别，则使用其父级别作为其有效级别，根记录器始终具有显式设置级别WARNING
        # 功能和方法具有相同的签名。 根记录器的名称在记录的输出中打印为 'root' 。
            子记录器将消息传播到与其上级记录器关联的处理程序。因此，不必为应用程序使用的所有记录器定义和配置处理程序。
            为顶级记录器配置处理程序并根据需要创建子记录器就足够了。
            （但是可以通过将记录器的 propagate 属性设置 False 来关闭传播）
        # 将消息记录到不同的地方
        目标由 handler 类提供。 如果你有任何内置处理程序类未满足的特殊要求，则可以创建自己的日志目标类。
        默认情况下，没有为任何日志记录消息设置目标。 你可以使用 basicConfig() 指定目标（例如控制台或文件）
         如果你调用函数 debug() 、 info() 、 warning() 、 error() 和 critical() ，他们将检查是否有设置目的日志保存地；
         如果没有设置，它们将在委托给根记录器进行实际的消息输出之前设置目标为控制台（ sys.stderr ）和默认格式的显示消息。
        
        # basicConfig() 设置的消息默认格式，可以通过使用 format 参数将格式字符串传递给 basicConfig() 来更改此设置。
        # 有关如何构造格式字符串的所有选项，请参阅 Formatter Objects 。
        severity:logger name:message
        
        # 记录流程，两个流
        Logger flow， Handler flow
        
        
     处理程序
        处理程序将日志记录（由记录器创建）发送到适当的目标。
        Handler 对象负责将适当的日志消息（基于日志消息的严重性）分派给处理程序的指定目标。
        Logger 对象可以使用 addHandler() 方法向自己添加零个或多个处理程序对象。
        教程主要使用 StreamHandler 和 FileHandler 
        
        setlevel()
            setLevel() 方法，就像在记录器对象中一样，指定将被分派到适当目标的最低严重性。
            注意这两个 setLevel()方法
                记录器中设置的级别确定将传递给其处理程序的消息的严重性。
                每个处理程序中设置的级别确定处理程序将发送哪些消息。
        setFormatter() 选择一个该处理程序使用的 Formatter 对象.
        addFilter() 和 removeFilter() 分别在处理程序上配置和取消配置过滤器对象.
        应用程序代码不应直接实例化并使用 Handler 的实例。 相反， Handler 类是一个基类，它定义了所有处理程序应该具有的接口，
        并建立了子类可以使用（或覆盖）的一些默认行为.
        
     过滤器
        过滤器提供了更精细的附加功能，用于确定要输出的日志记录
        参考高级用法:https://docs.python.org/zh-cn/3/howto/logging-cookbook.html
     格式化程序
        格式化程序指定最终输出中日志记录的样式
        格式化程序对象配置日志消息的最终顺序、结构和内容。 
        与 logging.Handler 类不同，应用程序代码可以实例化格式化程序类，但如果应用程序需要特殊行为，则可能会对格式化程序进行子类化。
        构造函数有三个可选参数 —— 消息格式字符串、日期格式字符串和样式指示符
     
        logging.Formatter.__init__(fmt=None, datefmt=None, style='%')
        如果没有消息格式字符串，则默认使用原始消息。如果没有日期格式字符串，则默认日期格式为
        %Y-%m-%d %H:%M:%S
        最后加上毫秒数。 style 是 ％，'{ ' 或 '$' 之一。 如果未指定其中一个，则将使用 '％'。
        
        以下消息格式字符串将以人类可读的格式记录时间、消息的严重性以及消息的内容，按此顺序:
        '%(asctime)s - %(levelname)s - %(message)s'

