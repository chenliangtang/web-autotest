# -*- coding: utf-8 -*-

import time

import utils
from pageobject.driver import Browser

login_file = 'login.ini'
config = utils.parse_conf(login_file)
url = config['data']['url']
welcome_login_xpath = config['xpath']['welcome_login']
username_xpath = config['xpath']['username']
password_xpath = config['xpath']['password']
login_btn_xpath = config['xpath']['login_btn']


def login(username, password):
    browser = Browser()
    driver = browser.driver
    driver.get(url)
    driver.maximize_window()
    driver.implicitly_wait(5)
    username_elem = driver.find_element_by_xpath(username_xpath)
    password_elem = driver.find_element_by_xpath(password_xpath)
    login_elem = driver.find_element_by_xpath(login_btn_xpath)
    username_elem.send_keys(username)
    password_elem.send_keys(password)
    time.sleep(0.5)
    login_elem.click()
    time.sleep(0.5)
    browser.update(driver)
