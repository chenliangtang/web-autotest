# -*- coding: utf-8 -*-

import time

from utils import CONFIG


def login(driver, username, password):
    url = CONFIG['common']['url']
    username_xpath = CONFIG['login']['username_xpath']
    password_xpath = CONFIG['login']['password_xpath']
    login_btn_xpath = CONFIG['login']['login_btn_xpath']
    driver.get(url)
    driver.maximize_window()
    driver.implicitly_wait(3)
    username_elem = driver.find_element_by_xpath(username_xpath)
    password_elem = driver.find_element_by_xpath(password_xpath)
    login_elem = driver.find_element_by_xpath(login_btn_xpath)
    username_elem.send_keys(username)
    password_elem.send_keys(password)
    time.sleep(0.5)
    login_elem.click()
    time.sleep(0.5)
