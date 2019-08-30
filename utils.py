# -*- coding: utf-8 -*-

import os
import re
import configparser

def parse_conf(filename):
    cur_path = os.path.dirname(__file__)
    #pre_path = re.findall(r'^.*\\', cur_path)[0]
    filename_dir = cur_path + '\\conf\\' + filename
    cp = configparser.ConfigParser()
    cp.read(filename_dir, encoding='utf-8')
    return cp
