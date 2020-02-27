# -*- coding: utf-8 -*-
# 工具类文件，封装了常用方法
import time

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from logger import Logger


logger = Logger().get_logger()


def click_element(driver, elem_xpath, timeout=5):
    """
    实现点击页面元素的功能

    :param driver:  webdriver 实例
    :param elem_xpath: 定位元素的 xpath
    :param timeout: 指定超时时间，默认是 5 s
    :return: 无返回值
    """
    locator = (By.XPATH, elem_xpath)
    WebDriverWait(driver, timeout, poll_frequency=0.1).until(
        EC.element_to_be_clickable(locator)
    ).click()


def input_text(driver, elem_xpath, text, timeout=5):
    """
    实现在页面的输入框中输入文本的功能

    :param driver: webdriver 实例
    :param elem_xpath: 定位元素的 xpath
    :param text: 要输入的文本字符串
    :param timeout: 指定超时时间，默认是 5 s
    :return: 无返回值
    """
    elem = wait_for_find_element(driver, elem_xpath)
    elem.clear()
    elem.send_keys(text)
    while True:
        start_time = time.time()
        end_time = start_time + timeout
        input_elem = driver.find_element_by_xpath(elem_xpath)
        input_value = input_elem.get_attribute('value')
        if input_value == text:
            break
        time.sleep(0.1)
        if time.time() > end_time:
            raise TimeoutException('找不到元素，已超时')
    WebDriverWait(driver, timeout, poll_frequency=0.1).until(
        EC.text_to_be_present_in_element_value((By.XPATH, elem_xpath), text)
    )


def wait_for_find_element(driver: WebDriver, elem_xpath: str, timeout=5):
    """
    实现等待查找页面元素的功能，默认会等待 5 s

    :param driver:  webdriver 实例
    :param elem_xpath:  定位元素的 xpath
    :param timeout: 指定超时时间，默认是 5 s
    :return: 成功会返回元素对象，失败会抛出 TimeoutException 异常
    """
    return WebDriverWait(driver, timeout, poll_frequency=0.1).until(
        EC.visibility_of_element_located((By.XPATH, elem_xpath))
    )


def wait_for_find_elements(driver: WebDriver, elems_xpath: str, timeout=5):
    """
        实现等待查找满足条件的所有页面元素的功能，默认会等待 5 s

        :param driver:  webdriver 实例
        :param elems_xpath:  定位元素的 xpath
        :param timeout: 指定超时时间，默认是 5 s
        :return: 成功会返回所有满足条件的元素，失败会抛出 TimeoutException 异常
        """
    return WebDriverWait(driver, timeout, poll_frequency=0.1).until(
        EC.presence_of_all_elements_located((By.XPATH, elems_xpath))
    )


def element_exist(driver: WebDriver, elem_xpath: str):
    """
    实现判断元素是否存在的功能

    :param driver: webdriver 实例
    :param elem_xpath: 定位元素的 xpath
    :return: 成功就返回元素本身，失败就返回 False
    """
    try:
        return wait_for_find_element(driver, elem_xpath, 15)
    except TimeoutException:
        return False
    except Exception as e:
        logger.error("发生未知的异常：{}".format(e))
        return False
