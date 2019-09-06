# -*- coding: utf-8 -*-

import unittest
from selenium.common.exceptions import NoSuchElementException

from pageobjects.login import login
from pageobjects.components.driver import driver_method_decorator
from utils import CONFIG


class TestLoginPage(unittest.TestCase):
    @driver_method_decorator
    def test_login(self, driver):
        username = CONFIG['common']['username']
        password = CONFIG['common']['password']
        welcome_login_xpath = CONFIG['login']['welcome_login_xpath']
        login(driver, username, password)
        try:
            welcome_login_elem = driver.find_element_by_xpath(welcome_login_xpath)
        except NoSuchElementException:
            welcome_login_elem = ''
        self.assertEqual(welcome_login_elem, '')
