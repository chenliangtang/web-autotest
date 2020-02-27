# -*- coding: utf-8 -*-

from functools import wraps
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from parseconfig import CONFIG
from logger import Logger

logger = Logger(__name__).get_logger()


class Driver(object):
    """
    封装了获取 webdriver 的类，其中 self.driver 中的变量值就是 webdriver 实例
    """
    def __init__(self):
        self.driver = self._init()

    @staticmethod
    def _init():
        browser_name = CONFIG['common']['browser']
        if not isinstance(browser_name, str):
            logger.error('{} is not string!!!'.format(browser_name))
            return

        if browser_name in ['ie', 'IE', 'Ie']:
            return webdriver.Ie()
        elif browser_name in ['chrome', 'Chrome']:
            # path 是你本地安装 chrome 浏览器的路径，chromedriver.exe 要放在 chrome.exe 同级目录下
            path = r'C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver.exe'
            # path = r'C:\Program Files (x86)\Google\Chrome\Application\\chromedriver.exe'
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


# 暂未用到
def driver_func_decorator(func):
    @wraps(func)
    def inner_func(*args, **kwargs):
        driver = Driver().driver
        func(driver, *args, **kwargs)
        driver.update(driver)
    return inner_func


# 暂未用到
def driver_method_decorator(func):
    @wraps(func)
    def inner_func(self, *args, **kwargs):
        driver = Driver().driver
        func(self, driver, *args, **kwargs)
        driver.update(driver)
    return inner_func
