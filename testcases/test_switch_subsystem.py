# -*- coding: utf-8 -*-

import time
import unittest

from pageobjects.switch_subsystem import switch_subsystem
from pageobjects.components.driver import driver_method_decorator
from utils import CONFIG


class TestSwitchSubsystem(unittest.TestCase):
    @driver_method_decorator
    def test_switch_subsystem(self, driver):
        random_system_btn_xpath = CONFIG['homepage']['random_system_btn_xpath']
        main_system_title_xpath = CONFIG['homepage']['main_system_title_xpath']
        switch_subsystem(driver, random_system_btn_xpath)
        main_system_title_elem = driver.find_element_by_xpath(main_system_title_xpath)
        self.assertEqual(main_system_title_elem.text, '宝安双随机项目')
        time.sleep(1)