# -*- coding: utf-8 -*-

import time
import unittest

from pageobjects.login import login
from pageobjects.logout import logout
from pageobjects.switch_to_sc_system import switch_to_sc_system
from components.driver import driver_method_decorator
from components.driver import Browser
from pageobjects.task_management import search_tasks, crawl_sc_task_content
from utils import CONFIG
from check.search_task import make_contents, make_params
from pageobjects.create_task import make_create_task_params, create_task
from components.common import wait_for_switch_to_iframe

browser = Browser()
driver = browser.get_driver()


# 登录系统并切换到双随机系统
def setUpModule():
    iframe = 'outerLink'
    login(
        driver,
        CONFIG['common']['username'],
        CONFIG['common']['password']
    )
    switch_to_sc_system(driver)
    wait_for_switch_to_iframe(driver, iframe)
    browser.update(driver)


# 登出系统
def tearDownModule():
    driver.switch_to.default_content()
    logout(driver)
    browser.close_driver()


class TestSearchTask(unittest.TestCase):
    # before testcase
    def setUp(self):
        pass

    # after testcase
    def tearDown(self):
        pass

    # before testsuite
    @classmethod
    def setUpClass(cls):
        pass

    # before testsuite
    @classmethod
    def tearDownClass(cls):
        pass

    @driver_method_decorator
    def test_search_task(self, driver):
        args = {
            'input_text': 'GC',
            'selected_content': '防洪排涝和排水类',
            'create_start_date_to_end_date': '2019-10-20~2019-11-1',
            'end_start_date_to_end_date': '2019-1-9~2019-12-1'
        }

        expected_contents = make_contents(make_params(args))
        search_tasks(driver, **args)
        if len(expected_contents) == 0:
            no_data_elem = driver.find_element_by_xpath(
                CONFIG['task_management']['no_data_xpath']
            )
            time.sleep(0.1)
            self.assertEqual('暂无数据', no_data_elem.text)
        else:
            contents = crawl_sc_task_content(driver)
            self.assertEqual(expected_contents, contents)

    @driver_method_decorator
    def test_create_task(self, driver):
        create_task(driver, make_create_task_params())
