# -*- coding: utf-8 -*-

from pageobjects import Login, Control
from webdriver import driver


login = Login(driver.driver)
login.login()

control = Control(driver.driver)


# control.start()
# control.next()
# control.next()
