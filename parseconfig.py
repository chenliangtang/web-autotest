# -*- coding: utf-8 -*-

import os
import configparser


class Singleton(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance[cls]


class Config(metaclass=Singleton):
    def __init__(self, file_name):
        self.file_name = file_name
        self.config = self.parse_conf()

    def parse_conf(self):
        cur_path = os.path.dirname(__file__)
        filename_dir = os.path.join(cur_path, self.file_name)
        cp = configparser.ConfigParser()
        cp.read(filename_dir, encoding='utf-8')
        return cp


file_name = 'config.ini'
CONFIG = Config(file_name).parse_conf()
