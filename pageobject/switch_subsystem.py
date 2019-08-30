# -*- coding: utf-8 -*-

import time
from selenium.webdriver.common.action_chains import ActionChains

from pageobject.driver import Browser
import utils

config = utils.parse_conf('home_page.ini')
main_menu_xpath = config['xpath']['main_menu']


def switch_subsystem(subsystem_btn_xpath):
    browser = Browser()
    driver = browser.driver
    main_menu_elem = driver.find_element_by_xpath(main_menu_xpath)
    ActionChains(driver).move_to_element(main_menu_elem).perform()
    subsystem_btn_elem = driver.find_element_by_xpath(subsystem_btn_xpath)
    time.sleep(0.5)
    subsystem_btn_elem.click()
    time.sleep(0.5)
    browser.update(driver)