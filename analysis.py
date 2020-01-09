# -*- coding: utf-8 -*-

import os


log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']


def read_file(filename, log_level='ERROR'):
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if line.__contains__(log_level):
                print(line)


def walk_files(root_dir):
    for root, _, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            read_file(file_path)
