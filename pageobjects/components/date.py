# -*- coding: utf-8 -*-

import datetime
import re

from pageobjects.components.driver import Browser


def split_date(year_mouth_day):
    date_list = year_mouth_day.split('-')
    year = int(date_list[0])
    mouth = int(date_list[1])
    day = int(date_list[2])
    return year, mouth, day


def locate_day(year_mouth_day):
    def __str2int(day):
        return 7 if day == '0' else int(day)
    year, mouth, day = split_date(year_mouth_day)
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


def locate_mouth(year_mmouth_day):
    _, mouth, _ = split_date(year_mmouth_day)
    row = 0
    mod = mouth % 3
    if mod:
        row += 1
    row += int(mouth / 3)
    column = 3 if mod == 0 else mod
    return (str(row), str(column))


def modify_table_xpath(table_xpath, tr_td):
    table_xpath = re.sub(r'(?<=tr\[)\d(?=\])', tr_td[0], table_xpath)
    table_xpath = re.sub(r'(?<=td\[)\d(?=\])', tr_td[1], table_xpath)
    return table_xpath


def select_mouth(mouth_xpath, locate_xpath, year_mmouth_day):
    driver = Browser().get_driver()
    mouth_elem = driver.find_element_by_xpath(mouth_xpath)
    mouth_elem.click()
    mouth_locate = locate_mouth(year_mmouth_day)
    locate_xpath = modify_table_xpath(locate_xpath, mouth_locate)
    locate_mouth_elem = driver.find_element_by_xpath(locate_xpath)
    locate_mouth_elem.click()
    Browser().update(driver)


def select_day(day_xpath, year_mouth_day):
    driver = Browser().get_driver()
    day_locate = locate_day(year_mouth_day)
    day_xpath = modify_table_xpath(day_xpath, day_locate)
    locate_day_elem = driver.find_element_by_xpath(day_xpath)
    locate_day_elem.click()
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
    select_mouth(start_mouth_xpath, start_table_xpath, create_time)
    select_day(start_day_xpath, create_time)
    # 选择结束的月和日（年暂未支持选择）
    select_mouth(end_mouth_xpath, end_table_xpath, end_time)
    select_day(end_day_xpath, end_time)