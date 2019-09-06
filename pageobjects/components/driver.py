# -*- coding: utf-8 -*-

import logging
from functools import wraps
from selenium import webdriver

from utils import Singleton, CONFIG


class Browser(metaclass=Singleton):
    def __init__(self):
        self.driver = self.__init_driver()

    @staticmethod
    def __init_driver():
        browser_name = CONFIG['common']['browser']
        if not isinstance(browser_name, str):
            logging.error('{} is not string!!!'.format(browser_name))
            return None

        if browser_name in ['ie', 'IE', 'Ie']:
            return webdriver.Ie()
        elif browser_name in ['chrome', 'Chrome']:
            return webdriver.Chrome()

    def update(self, driver):
        self.driver = driver

    def get_driver(self):
        return self.driver

    def close_driver(self):
        if self.driver:
            self.driver.close()


def driver_func_decorator(func):
    @wraps(func)
    def inner_func(*args, **kwargs):
        browser = Browser()
        driver = browser.get_driver()
        func(driver, *args, **kwargs)
        browser.update(driver)
    return inner_func


def driver_method_decorator(func):
    @wraps(func)
    def inner_func(self, *args, **kwargs):
        browser = Browser()
        driver = browser.get_driver()
        func(self, driver, *args, **kwargs)
        browser.update(driver)
    return inner_func
