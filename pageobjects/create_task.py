# -*- coding: utf-8 -*-

import calendar
import random
import time
from datetime import datetime

from utils import CONFIG
from components import common
from check.create_task import (available_departments_checker,
                               available_detachment_checker,
                               available_sc_objs)

sc_items_and_ids = {
    '防洪排涝和排水类': '1',
    '在建水务工程类': '2',
    '水资源和水土保持类': '3',
    '测试类别': '4'
}

sc_areas_and_id = {
    '全部区域': '1',
    '福永': '2',
    '福海': '3',
    '新桥': '4',
    '沙井': '5',
    '燕罗': '6',
    '松岗': '7',
    '西乡': '8',
    '新安': '9',
    '航城': '10',
    '石岩': '11'
}

departments_and_ids = {
    '长流陂水库管理站': '1',
    '防洪排涝和排水管理科': '2',
    '测试部': '3',
    '水污染治理科（规划发展科）': '4',
    '技术监管中心': '5',
    '水资源和供水管理办公室': '6',
    '水政监察大队': '7',
    '工程事务中心': '8',
    '罗田水库管理站': '9'
}

detachments_and_ids = {
    '福海水政监察中队': '1',
    '新安水政监察中队': '2',
    '西乡水政监察中队': '3',
    '航城水政监察中队': '4',
    '福永水政监察中队': '5',
    '沙井水政监察中队': '6',
    '新桥水政监察中队': '7',
    '燕罗水政监察中队': '8',
    '石岩水政监察中队': '9',
    '松岗水政监察中队': '10'
}

sc_frequencies_and_ids = {
    '月': '1',
    '季': '2',
    '年': '3',
}


def make_months_and_ids():
    cur_month = datetime.now().month
    months_and_ids = {}
    id = 0
    for month in range(cur_month, 12, 1):
        id += 1
        months_and_ids.update({str(month) + '月': str(id)})
    return months_and_ids


def random_choice_sc_object():
    sc_object = {
        'sc_item': '水资源和水土保持类',
        'sc_areas': ['福永', '西乡'],
        'sc_number': '4'
    }
    selected_sc_object = random.choice(
        available_sc_objs()
    )
    areas_and_numbers = []
    for sc_obj in available_sc_objs():
        if selected_sc_object[0] in sc_obj:
            areas_and_numbers.append({sc_obj[1]: sc_obj[2]})
    selected_number = random.randrange(1, len(areas_and_numbers) + 1, 1)
    selected_sc_areas = random.sample(areas_and_numbers, selected_number)
    areas = []
    sc_number = 0
    for item in selected_sc_areas:
        for area, number in item.items():
            areas.append(area)
            sc_number += number
    sc_object['sc_item'] = selected_sc_object[0]
    sc_object['sc_areas'] = areas
    if sc_number in [2, 3]:
        select_number = 1
    else:
        select_number = random.randrange(2, int(sc_number / 2) + 1, 1)
    sc_object['sc_number'] = str(select_number)
    return sc_object


def random_choice_department_checker():
    department_dict = {
        'departments': None,
        'sc_number': None
    }
    departments_dict = available_departments_checker()
    number = random.randrange(2, len(departments_dict) + 1, 1)
    selected_departments = random.sample(departments_dict, number)
    sc_number = 0
    departments_list = []
    for department in selected_departments:
        for name, number in department.items():
            sc_number += number
            departments_list.append(name)
    department_dict['departments'] = departments_list
    if sc_number in [2, 3]:
        select_number = 1
    else:
        select_number = random.randrange(2, int(sc_number / 2) + 1, 1)
    department_dict['sc_number'] = str(select_number)
    return department_dict


def random_choice_detachment_checker():
    detachment_dict = {
        'detachments': None,
        'sc_number': None
    }
    detachments_dict = available_detachment_checker()
    number = random.randrange(2, len(detachments_dict) + 1, 1)
    selected_detachments = random.sample(detachments_dict, number)
    sc_number = 0
    detachments_list = []
    for department in selected_detachments:
        for name, number in department.items():
            sc_number += number
            detachments_list.append(name)
    detachment_dict['detachments'] = detachments_list
    if sc_number in [2, 3]:
        select_number = 1
    else:
        select_number = random.randrange(2, int(sc_number / 2) + 1, 1)
    detachment_dict['sc_number'] = str(select_number)
    return detachment_dict


def random_choice_sc_frequency():
    return random.choice(['月', '季', '年'])


def random_choice_time_interval():
    months = []
    for month, _ in make_months_and_ids().items():
        months.append(month)
    return random.choice(months)


def random_choice_start_end_time(time_interval):
    month = int(time_interval[:-1])
    now = datetime.now()
    if month == now.month:
        start_date = now.strftime('%Y-%m-%d')
    else:
        start_date = '{}-{}-{}'.format(now.year, month, '01')
    end_month = random.randrange(month + 1, 12 + 1, 1)
    #if end_month == month:
    #    days = calendar.monthrange(now.year, month)[1]
    #    end_day = random.randrange(int(start_date.split('-')[2]), days + 1, 1)
    days = calendar.monthrange(now.year, end_month)[1]
    end_day = random.randrange(1, days + 1, 1)
    end_date = '{}-{}-{}'.format(now.year, end_month, end_day)
    return '{}~{}'.format(start_date, end_date)




def make_create_task_params():
    '''生成创建任务的参数

    Returns:
        >>> create_task_params = {
        'sc_object': {
            'sc_item': '水资源和水土保持类',
            'sc_area': '沙井',
            'sc_number': '1'
        },
        'checker': {
            'department': {
                'departments': ['防洪排涝和排水管理科', '水政监察大队', '罗田水库管理站', '长流陂水库管理站', '工程事务中心'],
                'sc_number': '121'
            },
            'detachment': {
                'detachments': ['沙井水政监察中队', '松岗水政监察中队'],
                'sc_number': '29'
            }
        },
        'sc_frequency': '年',
        'sc_time_interval': '10月',
        'start_and_end_time': '2019-09-28~2019-10-30',
        'task_group': '2'
    }
    '''
    sc_time_interval = random_choice_time_interval()
    create_task_params = {
        'sc_object': random_choice_sc_object(),
        'checker': {
            'department': random_choice_department_checker(),
            'detachment': random_choice_detachment_checker()
        },
        'sc_frequency': random_choice_sc_frequency(),
        'sc_time_interval': sc_time_interval,
        'start_and_end_time': random_choice_start_end_time(sc_time_interval),
        'task_group': '2'
    }
    return create_task_params


def __click_create_task(driver):
    common.click_element(
        driver,
        CONFIG['task_management']['create_task_xpath']
    )


def __select_sc_obj(driver, sc_object):
    """选择创建任务对话框的抽查对象

    Examples:
        >>> sc_object = {
            'sc_item': '水资源和水土保持类',
            'sc_area': '沙井',
            'sc_number': '1'
        }
    """
    sc_items_dropdown_xpath =  common.regex_replace_xpath_with_text_func(
        sc_object['sc_item'],
        CONFIG['task_management']['sc_items_dropdown_xpath']
    )
    time.sleep(0.5)
    common.select_dropdown_item(
        driver,
        CONFIG['task_management']['sc_items_xpath'],
        sc_items_dropdown_xpath
    )
    time.sleep(0.5)
    sc_areas_dropdown_xpath = []
    for sc_area in sc_object['sc_areas']:
        sc_area_id = sc_areas_and_id[sc_area]
        sc_area_dropdown_xpath = common.regex_replace_li_xpath(
            sc_area_id,
            CONFIG['task_management']['sc_area_dropdown_xpath']
        )
        sc_areas_dropdown_xpath.append(sc_area_dropdown_xpath)
    common.select_multi_dropdown_items(
        driver,
        CONFIG['task_management']['sc_area_xpath'],
        sc_areas_dropdown_xpath
    )
    common.input_text(
        driver,
        CONFIG['task_management']['sc_items_input_xpath'],
        sc_object['sc_number']
    )


def __select_checker(driver, checker):
    """选择创建任务对话框的检查人员

    Args：
        driver(WebDriver)
        checker(dict)

    Returns:
        None

    Examples:
        >>> driver = Chrome WebDriver
        >>> checker =
         {
            'department': {
                'departments': ['防洪排涝和排水管理科', '水政监察大队', '罗田水库管理站', '长流陂水库管理站', '工程事务中心'],
                'sc_number': '121'
            },
            'detachment': {
                'detachments': ['沙井水政监察中队', '松岗水政监察中队'],
                'sc_number': '29'
            }
        }
    """
    # 关闭科室框中默认选好的选项
    close_btn_elems = driver.find_elements_by_xpath(
        CONFIG['task_management']['sc_departments_close_xpath']
    )
    for close_btn_elem in close_btn_elems:
        time.sleep(0.5)
        close_btn_elem.click()
    # 重新选择科室框中的选项（多选）和抽取人数
    sc_departments_dropdown_xpath = []
    for sc_department in checker['department']['departments']:
        sc_department_id = departments_and_ids[sc_department]
        sc_deparment_dropdown_xpath = common.regex_replace_li_xpath(
            sc_department_id,
            CONFIG['task_management']['sc_departments_dropdown_xpath']
        )
        sc_departments_dropdown_xpath.append(sc_deparment_dropdown_xpath)
    common.select_multi_dropdown_items(
        driver,
        CONFIG['task_management']['sc_departments_xpath'],
        sc_departments_dropdown_xpath,
    )
    common.input_text(
        driver,
        CONFIG['task_management']['sc_departments_numbers_xpath'],
        checker['department']['sc_number']
    )
    # 选择中队框中的选项（多选）和抽取人数
    sc_detachments_dropdown_xpath = []
    for sc_detachment in checker['detachment']['detachments']:
        sc_detachment_id = detachments_and_ids[sc_detachment]
        sc_detachment_dropdown_xpath = common.regex_replace_li_xpath(
            sc_detachment_id,
            CONFIG['task_management']['sc_detachment_dropdown_xpath']
        )
        sc_detachments_dropdown_xpath.append(sc_detachment_dropdown_xpath)
    common.select_multi_dropdown_items(
        driver,
        CONFIG['task_management']['sc_detachment_xpath'],
        sc_detachments_dropdown_xpath,
    )
    common.input_text(
        driver,
        CONFIG['task_management']['sc_detachment_numbers_xpath'],
        checker['detachment']['sc_number']
    )


def __select_others(driver, create_task_params):
    '''选择创建任务对话框的其他选项（抽查频次、时段、起止时间、任务组数）
    
    Args:
        driver(WebDriver)
        create_task_params(dict)
    
    Examples:
        >>> driver = chrome WebDriver
        >>> create_task_params = 
        {
            'sc_frequency': '年',
            'sc_time_interval': '10月',
            'start_and_end_time': '2019-09-28~2019-10-30',
            'task_group': '1'
        }
    '''
    #选择抽查频次
    sc_frequency_dropdown_xpath = CONFIG['task_management']['sc_frequency_dropdown_xpath']
    sc_frequency_id = sc_frequencies_and_ids[create_task_params['sc_frequency']]
    sc_frequency_dropdown_xpath = common.regex_replace_li_xpath(
        sc_frequency_id,
        sc_frequency_dropdown_xpath
    )
    common.select_dropdown_item(
        driver,
        CONFIG['task_management']['sc_frequency_xpath'],
        sc_frequency_dropdown_xpath
    )
    # 选择抽查时段
    sc_time_interval_dropdown_xpath = CONFIG['task_management']['sc_time_interval_dropdown_xpath']
    sc_time_interval_id = make_months_and_ids()[create_task_params['sc_time_interval']]
    sc_time_interval_dropdown_xpath = common.regex_replace_li_xpath(
        sc_time_interval_id,
        sc_time_interval_dropdown_xpath
    )
    common.select_dropdown_item(
        driver,
        CONFIG['task_management']['sc_time_interval_xpath'],
        sc_time_interval_dropdown_xpath
    )
    input_date_elem = driver.find_element_by_xpath(
        CONFIG['task_management']['sc_start_to_end_time_xpath']
    )
    input_value = input_date_elem.get_attribute('value')
    print('before select_start_end_date:', input_value)
    if not input_value.startswith('20'):
        try:
            # 选择起止时间
            common.click_element(
                driver,
                CONFIG['task_management']['sc_start_to_end_time_xpath']
            )
            create_time_start_xpaths = [CONFIG['task_management']['create_time_start_month_xpath'],
                                        CONFIG['task_management']['create_time_start_month_table_xpath'],
                                        CONFIG['task_management']['create_time_start_day_xpath']]
            create_time_end_xpaths = [CONFIG['task_management']['create_time_end_month_xpath'],
                                      CONFIG['task_management']['create_time_end_month_table_xpath'],
                                      CONFIG['task_management']['create_time_end_day_xpath']]
            common.select_start_end_date(
                create_task_params['start_and_end_time'],
                create_time_start_xpaths,
                create_time_end_xpaths
            )
        except Exception as e :
            print('输入起止时间出错: ', e)
            time.sleep(60)

    input_date_elem = driver.find_element_by_xpath(
        CONFIG['task_management']['sc_start_to_end_time_xpath']
    )
    input_value = input_date_elem.get_attribute('value')
    if not input_value.startswith('20'):
        print('无法输入起止时间')
        time.sleep(60)
        raise Exception('无法输入起止时间')
    #选择任务组数
    common.input_text(
        driver,
        CONFIG['task_management']['sc_task_group_xpath'],
        create_task_params['task_group']
    )
    #发布任务
    common.click_element(
        driver,
        CONFIG['task_management']['sc_publish_task_xpath']
    )
    # 确认发布
    common.click_element(
        driver,
        CONFIG['task_management']['sc_task_confirm_btn_xpath']
    )


def __delete_sc_task_record(driver):
    common.wait_until_element_disappear(
        driver,
        CONFIG['task_management']['sc_publish_task_xpath']
    )
    # 点击抽查任务第一条记录的删除按钮
    common.click_element(
        driver,
        CONFIG['task_management']['sc_task_first_record_delete_btn_xpath']
    )
    # 确认删除
    common.click_element(
        driver,
        CONFIG['task_management']['sc_task_confirm_btn_xpath']
    )


def create_task(driver, create_task_params):
    task_code_text = common.wait_for_find_element(
        driver,
        CONFIG['task_management']['sc_task_first_record_task_code_xpath']
    ).text
    __click_create_task(driver)
    __select_sc_obj(driver, create_task_params['sc_object'])
    __select_checker(driver, create_task_params['checker'])
    __select_others(driver, create_task_params)
    not_equal = common.wait_for_not_equal(
        driver,
        CONFIG['task_management']['sc_task_code_xpath'],
        CONFIG['task_management']['sc_task_first_record_task_code_xpath'],
        '任务编号',
        task_code_text
    )
    assert not_equal is True
    time.sleep(1)
    __delete_sc_task_record(driver)






