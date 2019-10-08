# -*- coding: utf-8 -*-

import time
import re

from utils import CONFIG
from components import common


def input_task_code(driver, input_text):
    common.input_text(
        driver,
        CONFIG['task_management']['task_code_xpath'],
        input_text
    )


def select_dropdown_content(driver, selected_content):
    selected_elem_xpath = common.regex_replace_xpath_with_contains_func(
        selected_content,
        CONFIG['task_management']['dropdown_menu_xpath']
    )
    print(selected_elem_xpath)
    common.select_dropdown_item(
        driver,
        CONFIG['task_management']['item_category_xpath'],
        selected_elem_xpath
    )


def select_create_time(driver, start_date_to_end_date):
    """选择抽查任务管理 > 搜索栏里的创建时间

    Args:
        start_date_to_end_date = '2019-8-9~2019-10-1'
    """
    create_time_xpath = CONFIG['task_management']['create_time_xpath']
    common.click_element(driver, create_time_xpath)
    # 选择创建时间的起止日期
    create_time_start_xpaths = [CONFIG['task_management']['create_time_start_month_xpath'],
                                CONFIG['task_management']['create_time_start_month_table_xpath'],
                                CONFIG['task_management']['create_time_start_day_xpath']]
    create_time_end_xpaths = [CONFIG['task_management']['create_time_end_month_xpath'],
                              CONFIG['task_management']['create_time_end_month_table_xpath'],
                              CONFIG['task_management']['create_time_end_day_xpath']]

    common.select_start_end_date(start_date_to_end_date, create_time_start_xpaths, create_time_end_xpaths)


def select_end_time(driver, start_date_to_end_date):
    """选择抽查任务管理 > 搜索栏里的起止时间

    Args:
        start_date_to_end_date = '2019-11-9~2019-12-1'
    """
    end_time_xpath = CONFIG['task_management']['end_time_xpath']
    common.click_element(driver, end_time_xpath)
    # 选择创建时间的起止日期
    end_time_start_xpaths = [CONFIG['task_management']['end_time_start_month_xpath'],
                                CONFIG['task_management']['end_time_start_month_table_xpath'],
                                CONFIG['task_management']['end_time_start_day_xpath']]
    end_time_end_xpaths = [CONFIG['task_management']['end_time_end_month_xpath'],
                              CONFIG['task_management']['end_time_end_month_table_xpath'],
                              CONFIG['task_management']['end_time_end_day_xpath']]

    common.select_start_end_date(start_date_to_end_date, end_time_start_xpaths, end_time_end_xpaths)


def click_search(driver):
    common.click_element(driver, CONFIG['task_management']['search_btn_xpath'])


def search_tasks(
        driver,
        input_text=None,
        selected_content=None,
        create_start_date_to_end_date=None,
        end_start_date_to_end_date=None
    ):
    if input_text is not None:
        input_task_code(driver, input_text)
    if selected_content is not None:
        select_dropdown_content(driver, selected_content)
    if create_start_date_to_end_date is not None:
        select_create_time(driver, create_start_date_to_end_date)
    time.sleep(0.5)
    if end_start_date_to_end_date is not None:
        select_end_time(driver, end_start_date_to_end_date)
    click_search(driver)


def click_reset(driver):
    common.click_element(driver, CONFIG['task_management']['reset_btn_xpath'])


def click_all_status(driver):
    common.click_element(driver, CONFIG['task_management']['all_status_xpath'])


def click_to_be_published_status(driver):
    common.click_element(driver, CONFIG['task_management']['to_be_published_status_xpath'])


def click_to_be_checked_status(driver):
    common.click_element(driver, CONFIG['task_management']['to_be_checked_xpath'])


def click_checking_status(driver):
    common.click_element(driver, CONFIG['task_management']['checking_xpath'])


def click_checked_status(driver):
    common.click_element(driver, CONFIG['task_management']['checked_xpath'])


def click_timeout_status(driver):
    common.click_element(driver, CONFIG['task_management']['timeout_xpath'])


def crawl_sc_task_content(driver):
    # 序号/任务编号/任务创建时间/事项类别/抽查时段/检查对象数量/检察人员数/起止时间/上报时间/任务状态/检查情况
    fields_elems = driver.find_elements_by_xpath(
        CONFIG['task_management']['table_fields_xpath']
    )
    fields_list = []
    for field in fields_elems:
        fields_list.append(field.text)

    contents_list = []
    def crawl_one_page_content():
        """获取抽查任务管理中的表单数据"""
        tbody_elems = driver.find_elements_by_xpath(
            CONFIG['task_management']['sc_task_tbody_xpath']
        )
        for i in range(1, len(tbody_elems) + 1, 1):
            sc_task_tbody_td_xpath = re.sub(
                r'(?<=tr\[)\d.*(?=\])',
                str(i),
                CONFIG['task_management']['sc_task_tbody_td_xpath']
            )
            td_elems = driver.find_elements_by_xpath(sc_task_tbody_td_xpath)
            records_list = []
            for td_elem in td_elems:
                records_list.append(td_elem.text)
            fields_and_records = dict(zip(fields_list, records_list))
            fields_and_records.pop('检查情况')
            contents_list.append(fields_and_records)

    crawl_one_page_content()
    # 翻页提取表单数据
    total_text_elem = driver.find_element_by_xpath(
        CONFIG['task_management']['sc_task_total_text_xpath']
    )
    total_num = total_text_elem.text.split(' ')[1]
    total_num = int(total_num.strip())
    while total_num > 10:
        total_num -= 10
        next_page_btn = driver.find_element_by_xpath(
            CONFIG['task_management']['sc_task_next_page_xpath']
        )
        next_page_btn.click()
        time.sleep(0.5)
        crawl_one_page_content()
    return contents_list

