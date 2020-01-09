# -*- coding: utf-8 -*-

import random
from datetime import datetime

from pageobjects import Login, Controller, Logout
from webdriver import Driver
from logger import Logger

doc_list = ['多页面测试', '测试测试', 'test123']
# doc_list = ['日常接待版-稳定性测试', '社会治理平台-稳定性测试', '日常接待版', '社会治理平台']

while True:
    driver = Driver().driver
    logger = Logger().get_logger()

    login = Login(driver)
    login.login()

    # controller = Controller(driver)
    # controller.start()
    # controller.loop_play()

    if random.choice([True, False]):
        controller = Controller(driver)
        for _ in range(3):
            play_doc = random.choice(doc_list)
            result = controller.choice_doc(play_doc)
            if result is False:
                continue
            controller.start()
            controller.loop_play()

    logout = Logout(driver)
    logout.logout()
