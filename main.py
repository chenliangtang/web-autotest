# -*- coding: utf-8 -*-
# 主函数入口文件
import random
from pageobjects import Login, Controller
from webdriver import Driver
from logger import Logger
# 列表中列出测试页面，以逗号分隔，文稿名称用单引号引着
doc_list = ['日常接待版-稳定性测试', '社会治理平台-稳定性测试']
# 初始化驱动
driver = Driver().driver
# 初始化日志
logger = Logger().get_logger()
# 登录
login = Login(driver)
login.login()
# 初始化操作控制器
controller = Controller(driver)
# 选择显示屏
controller.select_screen()
# 死循环去播放文稿的页面
while True:
    for _ in range(3):
        play_doc = random.choice(doc_list)
        result = controller.choice_doc(play_doc)
        if result is False:
            continue
        controller.start()
        controller.loop_play()