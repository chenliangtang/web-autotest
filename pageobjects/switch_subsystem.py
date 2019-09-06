# -*- coding: utf-8 -*-

import time
from selenium.webdriver.common.action_chains import ActionChains

from utils import CONFIG


def switch_subsystem(driver, subsystem_btn_xpath):
    main_menu_xpath = CONFIG['homepage']['main_menu_xpath']
    main_menu_elem = driver.find_element_by_xpath(main_menu_xpath)
    ActionChains(driver).move_to_element(main_menu_elem).perform()
    subsystem_btn_elem = driver.find_element_by_xpath(subsystem_btn_xpath)
    time.sleep(1)
    subsystem_btn_elem.click()
    time.sleep(0.5)
