# -*- coding: utf-8 -*-

import unittest
import time

from pageobjects.components.driver import driver_method_decorator
from pageobjects.task_management import select_create_time, select_end_time
from utils import CONFIG


class TestDate(unittest.TestCase):
    @driver_method_decorator
    def test_date(self, driver):
        IFRAME_ID = 'outerLink'
        driver.switch_to_frame(IFRAME_ID)
        # 选择创建时间的起止日期
        select_create_time(driver, '2019-8-9~2019-10-1')
        time.sleep(0.5)
        # 选择起止时间的起止日期
        select_end_time(driver, '2019-1-9~2019-12-1')
        time.sleep(0.5)
        driver.switch_to.default_content()
