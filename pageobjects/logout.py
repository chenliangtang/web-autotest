# -*- coding: utf-8 -*-

import time
from selenium.webdriver.common.action_chains import ActionChains

from utils import CONFIG


def logout(driver):
    personal_center_xpath = CONFIG['logout']['personal_center_xpath']
    logout_xpath = CONFIG['logout']['logout_xpath']
    personal_center_elem = driver.find_element_by_xpath(personal_center_xpath)
    ActionChains(driver).move_to_element(personal_center_elem).perform()
    time.sleep(1)
    logout_elem = driver.find_element_by_xpath(logout_xpath)
    logout_elem.click()
    time.sleep(1)
