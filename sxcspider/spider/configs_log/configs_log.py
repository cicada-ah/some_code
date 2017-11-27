import os
import time
import logging


class Logging(object):
    def __init__(self, name, logfile_name=None, level=logging.DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        format_log = logging.Formatter(
            "%(asctime)s - [%(levelname)s] %(name)s - %(message)s")
        ch = None
        if logfile_name == None:
            ch = logging.StreamHandler()  # 设置一个logging输出到控制台
        else:
            logDir = os.path.dirname(os.path.abspath(__file__))
            if logDir != '' and not os.path.exists(logDir):
                os.mkdir(logDir)
                pass
            now = time.localtime()
            suffix = '.%d%02d%02d' % (
                now.tm_year, now.tm_mon, now.tm_mday)  # 格式化一下时间
            os.chdir(logDir)
            ch = logging.FileHandler(logfile_name + suffix)  # 输出log文件名
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(format_log)
        self.logger.addHandler(ch)

    def set_level(self, level):
        if level.lower() == "debug":
            self.logger.setLevel(logging.DEBUG)
        elif level.lower() == "info":
            self.logger.setLevel(logging.INFO)
        elif level.lower() == "warning":
            self.logger.setLevel(logging.WARNING)
        elif level.lower() == "error":
            self.logger.setLevel(logging.ERROR)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warn(self, message):
        self.logger.warn(message)

    def error(self, message):
        self.logger.error(message)
