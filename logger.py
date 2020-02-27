# -*- coding: utf-8 -*-
# 写日志用的
import logging
from logging import handlers

from singleton import Singleton


class Logger(metaclass=Singleton):
    """
    封装了用于写日志的日志库，可以打印 debug、info、error、fatal 级别的日志
    """
    def __init__(
            self,
            logger_name='操作日志记录',
            filename='logs/test.logs',
            when='H',
            interval=1,
            backup_count=999
    ):
        """
        实例化一个 logger 单例

        """
        self._logger = self.set_logger(logger_name, filename, when, interval, backup_count)

    @staticmethod
    def set_logger(logger_name, filename, when, interval, backup_count):
        """
        设置一个自定义的 logger 单实例

        :param logger_name: 指定 logger 的实例名称
        :param filename: 指定日志生成的文件名称
        :param when: 默认按小时，每间隔 1 小时就生成一份日志，总的日志备份 999 份
            S - Seconds
            M - Minutes
            H - Hours
            D - Days
            midnight - roll over at midnight
            W{0-6} - roll over on a certain day; 0 - Monday

            Case of the 'when' specifier is not important; lower or upper case
            will work.
        :param interval: 时间间隔， 默认间隔一小时
        :param backup_count: 日志的备份个数，默认备份 999 份
        :return: 返回一个 logger 实例
        """
        _logger = logging.getLogger(logger_name)
        _logger.setLevel(logging.DEBUG)
        handler = handlers.TimedRotatingFileHandler(
            filename,
            when=when,
            interval=interval,
            backupCount=backup_count,
            encoding='utf-8'
        )
        formatter = logging.Formatter(
            "[ %(asctime)s ] [ %(filename)s@ %(funcName)s@ %(lineno)d 行 ] "
            "| [ %(levelname)s ] %(message)s"
        )
        handler.setFormatter(formatter)
        _logger.addHandler(handler)
        return _logger

    def get_logger(self):
        return self._logger
