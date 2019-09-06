# -*- coding: utf-8 -*-

import os
import configparser


class Singleton(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance[cls]


def parse_conf(filename):
    cur_path = os.path.dirname(__file__)
    filename_dir = cur_path + '\\conf\\' + filename
    cp = configparser.ConfigParser()
    cp.read(filename_dir, encoding='utf-8')
    return cp


class Config(metaclass=Singleton):
    def __init__(self, filename):
        self.config = parse_conf(filename)


CONFIG_NAME = 'config.ini'
CONFIG = Config(CONFIG_NAME).config
