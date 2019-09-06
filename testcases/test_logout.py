# -*- coding: utf-8 -*-

import unittest

from pageobjects.logout import logout
from pageobjects.components.driver import driver_method_decorator
from utils import CONFIG


class TestLogout(unittest.TestCase):
    @driver_method_decorator
    def test_logout(self, driver):
        welcome_login_xpath = CONFIG['login']['welcome_login_xpath']
        logout(driver)
        welcome_login_elem = driver.find_element_by_xpath(welcome_login_xpath)
        self.assertEqual(welcome_login_elem.text, '欢迎登录')
