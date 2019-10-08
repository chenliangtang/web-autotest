# -*- coding: utf-8 -*-

import time
from selenium.webdriver.common.action_chains import ActionChains

from utils import CONFIG
from components import common


def switch_subsystem(driver, subsystem_name):
    main_menu_elem = common.wait_for_find_element(
        driver,
        CONFIG['homepage']['main_menu_xpath']
    )
    ActionChains(driver).move_to_element(main_menu_elem).perform()
    application_xpath = common.regex_replace_xpath_with_text_func(
        subsystem_name,
        CONFIG['homepage']['sc_application_xpath']
    )
    time.sleep(0.5)
    common.click_element(driver, application_xpath)
