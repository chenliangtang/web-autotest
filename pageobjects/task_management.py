# -*- coding: utf-8 -*-

from utils import CONFIG
from pageobjects.components.date import select_start_end_date


def select_create_time(driver, start_date_to_end_date):
    """选择抽查任务管理 > 搜索栏里的创建时间

    Args:
        start_date_to_end_date = '2019-8-9~2019-10-1'
    """
    create_time_xpath = CONFIG['task_management']['create_time_xpath']
    create_data_elem = driver.find_element_by_xpath(create_time_xpath)
    create_data_elem.click()

    # 选择创建时间的起止日期
    create_time_start_xpaths = [CONFIG['task_management']['create_time_start_mouth_xpath'],
                                CONFIG['task_management']['create_time_start_mouth_table_xpath'],
                                CONFIG['task_management']['create_time_start_day_xpath']]
    create_time_end_xpaths = [CONFIG['task_management']['create_time_end_mouth_xpath'],
                              CONFIG['task_management']['create_time_end_mouth_table_xpath'],
                              CONFIG['task_management']['create_time_end_day_xpath']]

    select_start_end_date(start_date_to_end_date, create_time_start_xpaths, create_time_end_xpaths)


def select_end_time(driver, start_date_to_end_date):
    """选择抽查任务管理 > 搜索栏里的起止时间

    Args:
        start_date_to_end_date = '2019-11-9~2019-12-1'
    """
    end_time_xpath = CONFIG['task_management']['end_time_xpath']
    end_data_elem = driver.find_element_by_xpath(end_time_xpath)
    end_data_elem.click()

    # 选择创建时间的起止日期
    end_time_start_xpaths = [CONFIG['task_management']['end_time_start_mouth_xpath'],
                                CONFIG['task_management']['end_time_start_mouth_table_xpath'],
                                CONFIG['task_management']['end_time_start_day_xpath']]
    end_time_end_xpaths = [CONFIG['task_management']['end_time_end_mouth_xpath'],
                              CONFIG['task_management']['end_time_end_mouth_table_xpath'],
                              CONFIG['task_management']['end_time_end_day_xpath']]

    select_start_end_date(start_date_to_end_date, end_time_start_xpaths, end_time_end_xpaths)