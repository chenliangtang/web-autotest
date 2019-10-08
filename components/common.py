# -*- coding: utf-8 -*-

import time
import datetime
import re
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

from components.driver import Browser


def __split_date(year_mouth_day):
    date_list = year_mouth_day.split('-')
    year = int(date_list[0])
    mouth = int(date_list[1])
    day = int(date_list[2])
    return year, mouth, day


def __locate_day(year_mouth_day):
    def __str2int(day):
        return 7 if day == '0' else int(day)

    year, mouth, day = __split_date(year_mouth_day)
    first_day_of_the_week = datetime.datetime(year, mouth, 1).strftime('%w')
    first_day_of_the_week = __str2int(first_day_of_the_week)
    day_of_the_week = datetime.datetime(year, mouth, day).strftime('%w')
    day_of_the_week = __str2int(day_of_the_week)
    range = 8 - first_day_of_the_week
    row = 1
    if day <= range:
        return (str(row), str(day_of_the_week))
    else:
        if (day - range) % 7 > 0:
            row += 1
        row += int((day - range) / 7)
        return (str(row), str(day_of_the_week))


def __locate_mouth(year_mmouth_day):
    _, mouth, _ = __split_date(year_mmouth_day)
    row = 0
    mod = mouth % 3
    if mod:
        row += 1
    row += int(mouth / 3)
    column = 3 if mod == 0 else mod
    return (str(row), str(column))


def __modify_table_xpath(table_xpath, tr_td):
    table_xpath = re.sub(r'(?<=tr\[)\d(?=\])', tr_td[0], table_xpath)
    table_xpath = re.sub(r'(?<=td\[)\d(?=\])', tr_td[1], table_xpath)
    return table_xpath


def __select_mouth(mouth_xpath, locate_xpath, year_mmouth_day):
    driver = Browser().get_driver()
    click_element(driver, mouth_xpath)
    mouth_locate = __locate_mouth(year_mmouth_day)
    locate_xpath = __modify_table_xpath(locate_xpath, mouth_locate)
    click_element(driver, locate_xpath)
    Browser().update(driver)


def __select_day(day_xpath, year_mouth_day):
    driver = Browser().get_driver()
    day_locate = __locate_day(year_mouth_day)
    day_xpath = __modify_table_xpath(day_xpath, day_locate)
    click_element(driver, day_xpath)
    Browser().update(driver)


def select_start_end_date(start_end_date, start_xpaths, end_xpaths):
    """ 选择起止时间

     Args：
        start_end_date = '2019-9-4~2010-10-22'
        start_xpaths = [start_mouth_xpath, start_table_xpath, start_day_xpath]
        end_xpaths = [end_mouth_xpath, end_table_xpath, end_day_xpath]
    """
    start_mouth_xpath, start_table_xpath, start_day_xpath = start_xpaths[0], start_xpaths[1], start_xpaths[2]
    end_mouth_xpath, end_table_xpath, end_day_xpath = end_xpaths[0], end_xpaths[1], end_xpaths[2]
    start_end_dates = start_end_date.split('~')
    create_time, end_time = start_end_dates[0], start_end_dates[1]
    # 选择开始的月和日（年暂未支持选择）
    __select_mouth(start_mouth_xpath, start_table_xpath, create_time)
    __select_day(start_day_xpath, create_time)
    # 选择结束的月和日（年暂未支持选择）
    __select_mouth(end_mouth_xpath, end_table_xpath, end_time)
    __select_day(end_day_xpath, end_time)


def wait_for_find_element(driver: WebDriver, elem_xpath: str):
    return WebDriverWait(driver, 5, poll_frequency=0.1).until(
        EC.visibility_of_element_located((By.XPATH, elem_xpath))
    )


def wait_for_find_elements(driver: WebDriver, elems_xpath: str):
    return WebDriverWait(driver, 5, poll_frequency=0.1).until(
        EC.presence_of_all_elements_located((By.XPATH, elems_xpath))
    )


def wait_for_switch_to_iframe(driver, iframe_name):
    WebDriverWait(driver, 5, poll_frequency=0.1).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, iframe_name))
    )


def wait_until_element_disappear(driver, xpath):
    WebDriverWait(driver, 15, poll_frequency=0.1).until(
        EC.invisibility_of_element_located((By.XPATH, xpath))
    )


def click_element(driver, elem_xpath):
    locator = (By.XPATH, elem_xpath)
    WebDriverWait(driver, 15, poll_frequency=0.1).until(
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
            raise Exception('Error')
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
