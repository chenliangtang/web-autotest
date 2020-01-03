# -*- coding: utf-8 -*-

import logging
from functools import wraps
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from parseconfig import Singleton, CONFIG


class Driver(metaclass=Singleton):
    def __init__(self):
        self.driver = self._init()

    @staticmethod
    def _init():
        browser_name = CONFIG['common']['browser']
        if not isinstance(browser_name, str):
            logging.error('{} is not string!!!'.format(browser_name))
            return

        if browser_name in ['ie', 'IE', 'Ie']:
            return webdriver.Ie()
        elif browser_name in ['chrome', 'Chrome']:
            path = r'C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver.exe'
            return webdriver.Chrome(executable_path=path)
        elif browser_name in ['360', '360浏览器']:
            options = Options()
            options.binary_location = r'D:\Program Files\360se6\Application\360se.exe'
            options.add_argument(r'--lang=zh-CN')
            path = r'D:\Program Files\360se6\Application\chromedriver.exe'
            return webdriver.Chrome(executable_path=path, chrome_options=options)

    def update(self, driver):
        self.driver = driver

    def close(self):
        if self.driver:
            self.driver.close()


def driver_func_decorator(func):
    @wraps(func)
    def inner_func(*args, **kwargs):
        driver = Driver().driver
        func(driver, *args, **kwargs)
        driver.update(driver)
    return inner_func


def driver_method_decorator(func):
    @wraps(func)
    def inner_func(self, *args, **kwargs):
        driver = Driver().driver
        func(self, driver, *args, **kwargs)
        driver.update(driver)
    return inner_func


driver = Driver()