# -*- coding: utf-8 -*-

import time
from selenium.webdriver.common.action_chains import ActionChains

from utils import CONFIG


def logout(driver):
    personal_center_elem = driver.find_element_by_xpath(
        CONFIG['logout']['personal_center_xpath']
    )
    ActionChains(driver).move_to_element(personal_center_elem).perform()
    time.sleep(1)
    logout_elem = driver.find_element_by_xpath(
        CONFIG['logout']['logout_xpath']
    )
    logout_elem.click()
    time.sleep(1)
    welcome_login_elem = driver.find_element_by_xpath(
        CONFIG['login']['welcome_login_xpath']
    )
    assert welcome_login_elem.text == '欢迎登录'