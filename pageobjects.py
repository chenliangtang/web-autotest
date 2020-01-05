# -*- coding: utf-8 -*-

import time
from utils import click_element, input_text
from selenium.webdriver.common.action_chains import ActionChains

from parseconfig import CONFIG


class Login(object):
    def __init__(self, driver):
        self.driver = driver
        self.url = CONFIG['common']['url']
        self.username = CONFIG['common']['username']
        self.password = CONFIG['common']['password']
        self.username_xpath = CONFIG['login']['username_xpath']
        self.password_xpath = CONFIG['login']['password_xpath']
        self.login_btn_xpath = CONFIG['login']['login_btn_xpath']

    def login(self):
        self.driver.get(self.url)
        self.driver.maximize_window()
        input_text(self.driver, self.username_xpath, self.username)
        input_text(self.driver, self.password_xpath, self.password)
        click_element(self.driver, self.login_btn_xpath)


class Logout(object):
    def logout(self, driver):
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


class Controller(object):
    def __init__(self, driver):
        self.driver = driver
        self.page_xpath = CONFIG['homepage']['nav_content_xpath']
        self.start_xpath = CONFIG['homepage']['start_xpath']
        self.next_xpath = CONFIG['homepage']['next_xpath']
        self.pre_xpath = CONFIG['homepage']['pre_xpath']

    def start(self):
        # click_element(self.driver, self.nav_content_xpath)
        click_element(self.driver, self.start_xpath)

    def next(self):
        click_element(self.driver, self.next_xpath)

    def pre(self):
        click_element(self.driver, self.pre_xpath)




        # while True:
        #     for _ in range(39):
        #         click_element(
        #             driver,
        #             CONFIG['homepage']['next_xpath']
        #         )
        #         sleep_time = random.randint(1, 5)
        #         time.sleep(sleep_time)
        #
        #     for _ in range(39):
        #         utils.click_element(
        #             driver,
        #             CONFIG['homepage']['prev_xpath']
        #         )
        #         sleep_time = random.randint(1, 5)
        #         time.sleep(sleep_time)