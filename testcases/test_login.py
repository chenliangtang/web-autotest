# -*- coding: utf-8 -*-

import unittest
from selenium.common.exceptions import NoSuchElementException

from pageobject.login import login
from pageobject.driver import Browser
import utils

config = utils.parse_conf('login.ini')
username = config['data']['username']
password = config['data']['password']
welcome_login_xpath = config['xpath']['welcome_login']


class TestLoginPage(unittest.TestCase):
    def test_login(self):
        login(username, password)
        browser = Browser()
        driver = browser.driver
        try:
            welcome_login_elem = driver.find_element_by_xpath(welcome_login_xpath)
        except NoSuchElementException:
            welcome_login_elem = ''
        self.assertEqual(welcome_login_elem, '')
        browser.update(driver)
