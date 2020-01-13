# -*- coding: utf-8 -*-

import random
from datetime import datetime

from pageobjects import Login, Controller, Logout
from webdriver import Driver
from logger import Logger

doc_list = ['日常接待版-稳定性测试', '社会治理平台-稳定性测试']


driver = Driver().driver
logger = Logger().get_logger()

login = Login(driver)
login.login()

controller = Controller(driver)

while True:
    for _ in range(3):
        play_doc = random.choice(doc_list)
        result = controller.choice_doc(play_doc)
        if result is False:
            continue
        controller.start()
        controller.loop_play()

logout = Logout(driver)
logout.logout()
