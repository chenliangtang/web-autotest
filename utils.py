# -*- coding: utf-8 -*-

import re
import time

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException


def _modify_table_xpath(table_xpath, tr_td):
    table_xpath = re.sub(r'(?<=tr\[)\d(?=\])', tr_td[0], table_xpath)
    table_xpath = re.sub(r'(?<=td\[)\d(?=\])', tr_td[1], table_xpath)
    return table_xpath


def wait_for_find_element(driver: WebDriver, elem_xpath: str, timeout=5):
    return WebDriverWait(driver, timeout, poll_frequency=0.1).until(
        EC.visibility_of_element_located((By.XPATH, elem_xpath))
    )


def element_exist(driver: WebDriver, elem_xpath: str):
    try:
        return wait_for_find_element(driver, elem_xpath)
    except TimeoutException:
        return False


def wait_for_find_elements(driver: WebDriver, elems_xpath: str):
    return WebDriverWait(driver, 5, poll_frequency=0.1).until(
        EC.presence_of_all_elements_located((By.XPATH, elems_xpath))
    )


def wait_for_switch_to_iframe(driver, iframe_name):
    WebDriverWait(driver, 5, poll_frequency=0.1).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, iframe_name))
    )


def wait_until_element_disappear(driver, xpath):
    WebDriverWait(driver, 5, poll_frequency=0.1).until(
        EC.invisibility_of_element_located((By.XPATH, xpath))
    )


def wait_until_all_elements_visible(driver, xpath):
    WebDriverWait(driver, 5, poll_frequency=0.1).until(
        EC.visibility_of_any_elements_located((By.XPATH, xpath))
    )


def click_element(driver, elem_xpath):
    locator = (By.XPATH, elem_xpath)
    WebDriverWait(driver, 5, poll_frequency=0.1).until(
        EC.element_to_be_clickable(locator)
    ).click()


def click_alert_confirm_button(driver):
    WebDriverWait(driver, 5, poll_frequency=0.1).until(
        EC.alert_is_present()
    ).accept()


def select_dropdown_item(driver, elem_xpath, dropdown_item_xpath):
    click_element(driver, elem_xpath)
    click_element(driver, dropdown_item_xpath)


def wait_for_text_present(driver, xpath, text):
    return WebDriverWait(driver, 10, poll_frequency=0.1).until(
        EC.text_to_be_present_in_element((By.XPATH, xpath), text)
    )


def wait_for_not_equal(driver, key_xpath, value_xpath, key_text, expected_text):
    has_text = wait_for_text_present(driver, key_xpath, key_text)
    assert has_text is True
    while True:
        start_time = time.time()
        end_time = start_time + 10
        try:
            actual_text = wait_for_find_element(driver, value_xpath).text
        except StaleElementReferenceException:
            pass

        if actual_text != expected_text:
            return True
        time.sleep(0.1)
        if time.time() > end_time:
            return False


def select_multi_dropdown_items(
        driver, elem_xpath, items_xpath
):
    click_element(driver, elem_xpath)
    for item_xpath in items_xpath:
        click_element(driver, item_xpath)
    driver.find_element_by_tag_name('body').send_keys(Keys.ESCAPE)


def clear_input_text(driver, elem_xpath):
    wait_for_find_element(driver, elem_xpath).clear()


def wait_for_text_exist(driver, elem_xpath, text):
    WebDriverWait(driver, 5, poll_frequency=0.1).until(
        EC.text_to_be_present_in_element((By.XPATH, elem_xpath), text)
    )


def input_text(driver, elem_xpath, text):
    elem = wait_for_find_element(driver, elem_xpath)
    elem.clear()
    elem.send_keys(text)
    while True:
        start_time = time.time()
        end_time = start_time + 5
        input_elem = driver.find_element_by_xpath(elem_xpath)
        input_value = input_elem.get_attribute('value')
        if input_value == text:
            break
        time.sleep(0.1)
        if time.time() > end_time:
            raise TimeoutException('找不到元素，已超时')
    WebDriverWait(driver, 5, poll_frequency=0.1).until(
        EC.text_to_be_present_in_element_value((By.XPATH, elem_xpath), text)
    )


def wait_for_visibility_of_element(driver, xpath):
    WebDriverWait(driver, 5, poll_frequency=0.1).until(
        EC.visibility_of_element_located((By.XPATH, xpath))
    )


def regex_replace_li_xpath(repl, xpath):
    return re.sub(r'(?<=li\[)\d(?=\])', repl, xpath)


def regex_replace_xpath_with_text_func(repl, xpath):
    return re.sub(r'(?<=text\(\)=\").*?(?=\")', repl, xpath)


def regex_replace_xpath_with_contains_func(repl, xpath):
    return re.sub(r'(?<=\,.\").*?(?=\"\))|(?<=\,\").*?(?=\"\))', repl, xpath)


def regex_replace_tr_xpath(repl, xpath):
    return re.sub(r'(?<=tr\[)\d(?=\])', repl, xpath)


def regex_replace_td_xpath(repl, xpath):
    return re.sub(r'(?<=td\[)\d(?=\])', repl, xpath)
