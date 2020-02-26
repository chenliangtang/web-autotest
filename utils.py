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
    locator = (By.XPATH, elem_xpath)
    WebDriverWait(driver, timeout, poll_frequency=0.1).until(
        EC.element_to_be_clickable(locator)
    ).click()


def input_text(driver, elem_xpath, text, timeout=5):
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
    return WebDriverWait(driver, timeout, poll_frequency=0.1).until(
        EC.visibility_of_element_located((By.XPATH, elem_xpath))
    )


def wait_for_find_elements(driver: WebDriver, elems_xpath: str, timeout=5):
    return WebDriverWait(driver, timeout, poll_frequency=0.1).until(
        EC.presence_of_all_elements_located((By.XPATH, elems_xpath))
    )


def element_exist(driver: WebDriver, elem_xpath: str):
    try:
        return wait_for_find_element(driver, elem_xpath, 15)
    except TimeoutException:
        return False
    except Exception as e:
        logger.error("发生未知的异常：{}".format(e))
        return False
