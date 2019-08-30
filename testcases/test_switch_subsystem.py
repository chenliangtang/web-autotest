# -*- coding: utf-8 -*-

import time
import unittest

from pageobject.switch_subsystem import switch_subsystem
from pageobject.driver import Browser
from utils import parse_conf


config = parse_conf('home_page.ini')
random_system_btn_xpath = config['xpath']['random_system_btn']
main_system_title_xpath = config['xpath']['main_system_title']


class TestSwitchSubsystem(unittest.TestCase):
    def test_switch_subsystem(self):
        switch_subsystem(random_system_btn_xpath)
        browser = Browser()
        driver = browser.driver
        main_system_title_elem = driver.find_element_by_xpath(main_system_title_xpath)
        self.assertEqual(main_system_title_elem.text, '宝安双随机项目')
        time.sleep(0.5)
        browser.update(driver)