# -*- coding: utf-8 -*-
# 解析 config 配置文件用的
import os
import configparser

from singleton import Singleton


class Config(metaclass=Singleton):
    def __init__(self, filename):
        self.filename = filename
        self.config = self.parse_conf()

    def parse_conf(self):
        cur_path = os.path.dirname(__file__)
        filename_dir = os.path.join(cur_path, self.filename)
        cp = configparser.ConfigParser()
        cp.read(filename_dir, encoding='utf-8')
        return cp


file_name = 'config.ini'
CONFIG = Config(file_name).parse_conf()
