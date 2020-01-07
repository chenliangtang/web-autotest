# -*- coding: utf-8 -*-

import time

from pageobjects import Login, Controller, Logout
from webdriver import driver
from logger import Logger

logger = Logger().get_logger()

login = Login(driver.driver)
login.login()

controller = Controller(driver.driver)

controller.start()
controller.loop_play()


logout = Logout(driver.driver)
logout.logout()
