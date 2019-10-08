# -*- coding: utf-8 -*-

from utils import CONFIG
from components import common
from components.common import click_element, input_text


def login(driver, username, password):
    hostname = CONFIG['common']['hostname']
    username_xpath = CONFIG['login']['username_xpath']
    password_xpath = CONFIG['login']['password_xpath']
    username_check_mark_xpath = CONFIG['login']['username_check_mark_xpath']
    password_check_mark_xpath = CONFIG['login']['password_check_mark_xpath']
    login_btn_xpath = CONFIG['login']['login_btn_xpath']
    path = '/admin'
    url = hostname + path
    driver.get(url)
    driver.maximize_window()
    input_text(driver, username_xpath, username)
    input_text(driver, password_xpath, password)
    common.wait_for_visibility_of_element(
        driver,
        username_check_mark_xpath
    )
    common.wait_for_visibility_of_element(
        driver,
        password_check_mark_xpath
    )
    click_element(driver, login_btn_xpath)
