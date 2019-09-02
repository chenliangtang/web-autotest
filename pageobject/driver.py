# -*- coding: utf-8 -*-

import logging
from selenium import webdriver
from functools import wraps

from utils import parse_conf


CONF_NAME = 'conf.ini'


def singleton(cls):
    _instance = {}
    @wraps(cls)
    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]
    return inner


@singleton
class Browser(object):
    def __init__(self):
        self.driver = self.__init_driver()

    @staticmethod
    def __init_driver():
        config = parse_conf(CONF_NAME)
        browser_name = config['common']['browser']
        if not isinstance(browser_name, str):
            logging.error('{} is not string!!!'.format(browser_name))
            return None

        if browser_name in ['ie', 'IE', 'Ie']:
            return webdriver.Ie()
        elif browser_name in ['chrome', 'Chrome']:
            return webdriver.Chrome()

    def update(self, driver):
        self.driver = driver

    def close_driver(self):
        if self.driver:
            self.driver.close()
