# You'll need these imports in your own code
# 您需要在自己的代码中导入这些内容, 多进程同时写一个文件
import logging
import logging.handlers
import multiprocessing

# Next two import lines for this demo only
# 仅此演示的下两个导入行
from random import choice, random
import time


#
# Because you'll want to define the logging configurations for listener and workers, the
# listener and worker process functions take a configurer parameter which is a callable
# for configuring logging for that process. These functions are also passed the queue,
# which they use for communication.
#
# In practice, you can configure the listener however you want, but note that in this
# simple example, the listener does not apply level or filter logic to received records.
# In practice, you would probably want to do this logic in the worker processes, to avoid
# sending events which would be filtered out between processes.
#
# The size of the rotated files is made small so you can see the results easily.
# 由于您要为监听器和工作程序定义日志记录配置，因此listener和worker进程函数采用可调用的configurer参数
# 用于配置该进程的日志记录。这些功能也会传递给队列，他们用于通信的＃号。
# 实际上，您可以根据需要配置侦听器，但请注意，简单的例子，侦听器不对接收到的记录应用级别或过滤器逻辑。
# 实际上，您可能希望在辅助进程中执行此逻辑，以避免发送事件，这些事件将在进程之间被过滤掉。
# 减小旋转文件的大小，以便您轻松查看结果。
def listener_configurer():
    """
    定义记录器和日志格式
    :return:
    """
    root = logging.getLogger()
    h = logging.handlers.RotatingFileHandler('mult_test.log', 'a', 300, 10)
    f = logging.Formatter('%(asctime)s %(processName)-10s %(name)s %(levelname)-8s %(message)s')
    h.setFormatter(f)
    root.addHandler(h)


# This is the listener process top-level loop: wait for logging events
# (LogRecords)on the queue and handle them, quit when you get a None for a
# LogRecord.
# 这是侦听器进程的顶级循环：等待记录事件（LogRecords）在队列上并行处理它们，当您获得一个None时退出LogRecord。
def listener_process(queue, configurer):
    configurer()
    while True:
        try:
            record = queue.get()
            if record is None:  # We send this as a sentinel to tell the listener to quit.
                break
            logger = logging.getLogger(record.name)
            logger.handle(record)  # No level or filter logic applied - just do it!
        except Exception:
            import sys, traceback
            print('Whoops! Problem:', file=sys.stderr)
            traceback.print_exc(file=sys.stderr)


# Arrays used for random selections in this demo
# 本演示中用于随机选择的数组

LEVELS = [logging.DEBUG, logging.INFO, logging.WARNING,
          logging.ERROR, logging.CRITICAL]

LOGGERS = ['a.b.c', 'd.e.f']

MESSAGES = [
    'Random message #1',
    'Random message #2',
    'Random message #3',
]


# The worker configuration is done at the start of the worker process run.
# Note that on Windows you can't rely on fork semantics, so each process
# will run the logging configuration code when it starts.
# 在工作进程运行开始时完成工作进程配置。注意在Windows上您不能依赖fork语义，因此每个过程
# 将在启动时运行日志记录配置代码。
def worker_configurer(queue):
    h = logging.handlers.QueueHandler(queue)  # Just the one handler needed
    root = logging.getLogger()
    root.addHandler(h)
    # send all messages, for demo; no other level or filter logic applied.
    root.setLevel(logging.DEBUG)


# This is the worker process top-level loop, which just logs ten events with
# random intervening delays before terminating.
# The print messages are just so you know it's doing something!
# 这是工作进程顶级循环，它仅记录10个事件
# 终止之前的随机介入延迟。打印消息只是为了让您知道它在做什么！

def worker_process(queue, configurer):
    configurer(queue)
    name = multiprocessing.current_process().name
    print('Worker started: %s' % name)
    for i in range(10):
        time.sleep(random())
        logger = logging.getLogger(choice(LOGGERS))
        level = choice(LEVELS)
        message = choice(MESSAGES)
        logger.log(level, message)
    print('Worker finished: %s' % name)


# Here's where the demo gets orchestrated. Create the queue, create and start
# the listener, create ten workers and start them, wait for them to finish,
# then send a None to the queue to tell the listener to finish.
# 这是协调演示的位置。创建队列，创建并开始侦听器，创建十个工作程序并启动它们，等待它们完成，然后将None发送到队列以告知侦听器完成。
def main():
    queue = multiprocessing.Queue(-1)
    listener = multiprocessing.Process(target=listener_process,
                                       args=(queue, listener_configurer))
    listener.start()
    workers = []
    for i in range(10):
        worker = multiprocessing.Process(target=worker_process,
                                         args=(queue, worker_configurer))
        workers.append(worker)
        worker.start()
    for w in workers:
        w.join()
    queue.put_nowait(None)
    listener.join()


def log_handly():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        filemode='w',
                        filename='test.log',
                        # format='%(asctime)s %(name)-12s %(levelname)-8s %(message)',
                        datefmt='%Y%m-%d %H:%M%:S')
    logging.info("this not console output 1 ")

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    con_formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(con_formatter)
    logging.getLogger('').addHandler(console)

    # root logging
    logging.debug('this is root log debug in console')
    logging.info('this root log info in console')

    logger1 = logging.getLogger('test1')
    logger2 = logging.getLogger('test2')

    logger1.debug('this is test1 debug')
    logger1.info('this is test1 info')
    logger2.debug('this is test2 debug')
    logger2.info('this is test2 info')
    logger2.error('this is test2 error')
    logger2.warning('this is test2 warning')


if __name__ == '__main__':
    log_handly()
    main()
