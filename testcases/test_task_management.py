# -*- coding: utf-8 -*-

import time
import unittest

from pageobjects.components.driver import driver_method_decorator
from selenium.webdriver.support import expected_conditions

class TestSearchTask(unittest.TestCase):
    @driver_method_decorator
    def test_search_task(self, driver):
        driver.switch_to_frame('outerLink')
        item_category_elem = driver.find_element_by_xpath(
            '//*[@id="app"]/div/div[2]/div/div'
        )
        item_category_elem.click()
        time.sleep(0.5)
        selected_elems = driver.find_elements_by_xpath(
            #'//*[@class="ant-select-dropdown-content"]/ul/li[4]'
            '//*[@class="ant-select-dropdown-content"]/ul/child::li'
        )
        time.sleep(0.5)
        print(selected_elems, type(selected_elems))
        for elem in selected_elems:
            print(expected_conditions.element_to_be_selected, elem.text, elem.is_displayed(), elem.is_enabled(), elem.is_selected())
        time.sleep(0.5)
        #selected_elems.click()
        driver.switch_to.default_content()
