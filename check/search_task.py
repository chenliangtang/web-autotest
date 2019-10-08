# -*- coding: utf-8 -*-

import re
import json
import jmespath
import requests
from datetime import datetime

from utils import CONFIG

hostname = CONFIG['common']['hostname']

task_code_and_id = {
    '全部': None,
    '待发布': 0,
    '待检查': 1,
    '检查中': 2,
    '已检查': 3,
    '已超时': 4
}

request_kwargs = {
    'input_text': None,
    'selected_content': None,
    'create_start_date_to_end_date': '2019-8-9~2019-10-1',
    'end_start_date_to_end_date': '2019-1-9~2019-12-1'
}

category_and_id = {
    '全部': None,
    '防洪排涝和排水类': '2c93808e6bacbd79016be3ea8d01040d',
    '水资源和水土保持类': '2c93808e6bacbd79016be3ea4160040b',
    '在建水务工程类': '2c93808e6bacbd79016be3eabbc8040e'
}

category_and_task_id_prefix = {
    '防洪排涝和排水类': 'PS',
    '水资源和水土保持类': 'ST',
    '在建水务工程类': 'GC'
}

get_sc_tasks_params = {
    'page': 1,
    'pagesize': 10,
    'categoryId': None,
    'taskCode': None,
    'taskState': None,
    'createStartTime': datetime(2018, 9, 12, 00, 00, 00),
    'createEndTime': datetime(2019, 9, 15, 23, 59, 59),
    'startTime': None,
    'endTime': None
}


def __query_times(total_items):
    cnt = 0
    if total_items % 10 > 0:
        cnt += 1
    cnt += int(total_items / 10)
    return cnt


def __date2dateime(start_date_to_end_date):
    '''字符串形式的起止日期转为 python 对象的日期格式

    Args:
        start_date_to_end_date(str)

    returns:
        start_datetime(datetime), end_datetime(datetime)

    Examples:
        >>> start_date_to_end_date = '2018-9-12~2019-9-15'
        >>> start_datetime = datetime(2018, 9, 12, 00, 00, 00)
        >>> end_datetime = datetime(2019, 9, 15, 23, 59, 59)
    '''
    start_datetime = None
    end_datetime = None
    dates_list = start_date_to_end_date.split('~')
    for index, date in enumerate(dates_list):
        split_date_list = date.split('-')
        if len(split_date_list) != 3:
            return
        year, mouth, day = int(split_date_list[0]), int(split_date_list[1]), int(split_date_list[2])
        if index == 0:
            start_datetime = datetime.strptime(date, '%Y-%m-%d')
        if index == 1:
            end_datetime = datetime(year, mouth, day, 23, 59, 59)
    return start_datetime, end_datetime


def make_params(request_kwargs):
    '''将用户实际选择时看到的请求参数转为后台接口可以识别的请求参数

    Args：
        request_kwargs(dict)

    Returns:
        params(dict)

    Examples:
        >>> request_kwargs =
        {
             'input_text': 'GK',
            'selected_content': '防洪排涝和排水类',
            'create_start_date_to_end_date': '2019-8-9~2019-10-1',
            'end_start_date_to_end_date': '2019-1-9~2019-12-1'
        }
        >>> params =
        {
            'page': 1,
            'pagesize': 10,
            'categoryId': '2c93808e6bacbd79016be3ea8d01040d',
            'taskCode': 'GK',
            'taskState': None,
            'createStartTime': datetime(2019, 8, 9, 00, 00, 00),
            'createEndTime': datetime(2019, 10, 1, 23, 59, 59),
            'startTime': datetime(2019, 1, 9, 00, 00, 00),
            'endTime': datetime(2019, 12, 1, 23, 59, 59)
        }

    '''
    params = {
        'page': 1,
        'pagesize': 10,
        'categoryId': 'None',
        'taskCode': None,
        'taskState': None,
        'createStartTime': None,
        'createEndTime': None,
        'startTime': None,
        'endTime': None
    }
    for key, value in request_kwargs.items():
        if key == 'input_text':
            params.update({'taskCode': value})
        if key == 'selected_content':
            params.update({'categoryId': category_and_id.get(value, None)})
        if key == 'create_start_date_to_end_date':
            createStartTime, createEndTime = __date2dateime(value)
            params.update(
                {
                    'createStartTime': createStartTime,
                    'createEndTime': createEndTime
                }
            )
        if key == 'end_start_date_to_end_date':
            startTime, endTime = __date2dateime(value)
            params.update(
                {
                    'startTime': startTime,
                    'endTime': endTime
                }
            )
    request_params = {
        'headers': {
            'Content-Type': 'application/json'
        },
        'params': params
    }
    return request_params


def __select_query_page(request_params, page_num):
    request_params['params'].update({'page': page_num})
    return request_params


def __query_sc_task(kwargs):
    request = requests.session()
    path = '/api/shuangsuiji/v1/getScTasks'
    url = hostname + path
    response = request.get(url, **kwargs)
    return json.loads(response.content)


def __utc_str_2_cst_datetime(utc_str):
    _date = re.findall(r'.*?(?=T)', utc_str)[0]
    _time = re.findall(r'(?<=T).*(?=\.)', utc_str)[0]
    _utc = re.findall(r'(?<=\+).*?(?=$)', utc_str)[0]
    _timedelta = datetime.fromtimestamp(0) - datetime.utcfromtimestamp(0)
    _datetime = datetime.strptime(
        _date + ' ' + _time, '%Y-%m-%d %H:%M:%S'
    )
    return _datetime + _timedelta


def __parse_report_time(report_time):
    if report_time is None:
        return ''
    else:
        report_datetime = __utc_str_2_cst_datetime(report_time)
        return report_datetime.strftime('%Y-%m-%d %H:%M:%S')


def __make_start_end_time(utc_start_time, utc_end_time):
    start_datetime = __utc_str_2_cst_datetime(utc_start_time)
    end_datetime = __utc_str_2_cst_datetime(utc_end_time)
    start_str = start_datetime.strftime('%Y-%m-%d')
    end_str = end_datetime.strftime('%Y-%m-%d')
    return start_str + '~' + end_str


def __parse_task_state(task_state_id):
    task_state_and_id = {
        #None: '全部',
        '0': '待发布',
        '1': '待检查',
        '2': '检查中',
        '3': '已检查',
        '4': '已超时'
    }
    if task_state_id is None:
        return '全部'
    else:
        return task_state_and_id[task_state_id]


def __none_obj_to_none_str(obj):
    return obj if obj else ''


def make_contents(request_args):
    dict_content = __query_sc_task(request_args)
    times = __query_times(dict_content['total'])
    count = 0
    content_list = []
    if times == 0:
        return content_list

    for page in range(1, times + 1, 1):
        request_args = __select_query_page(request_args, page)
        content = __query_sc_task(request_args)
        total_cnt = jmespath.search('total', content)
        if total_cnt == 0 or total_cnt is None:
            return

        data = jmespath.search('data', content)
        if not isinstance(data, list):
            return

        for item in data:
            count += 1
            content_dict = {}
            content_dict.update({'序号': str(count)})
            content_dict.update({'任务编号': jmespath.search('taskcode', item)})
            content_dict.update(
                {
                    '任务创建时间': __utc_str_2_cst_datetime(
                        jmespath.search('createAt', item)
                    ).strftime('%Y-%m-%d %H:%M:%S')
                }
            )
            content_dict.update({'事项类别': jmespath.search('categoryname', item)})
            content_dict.update(
                {
                    '抽查时段': jmespath.search('timeinterval', item) \
                            + jmespath.search('frequency', item)
                }
            )
            content_dict.update({'检查对象数量': str(jmespath.search('objectnumber', item))})
            content_dict.update({'检察人员数': str(jmespath.search('personnelnumber', item))})
            content_dict.update(
                {
                    '起止时间': __make_start_end_time(
                        jmespath.search('starttime', item),
                        jmespath.search('endingtime', item)
                    )
                }
            )
            content_dict.update(
                {'上报时间': __parse_report_time(jmespath.search('reportingtime', item))}
            )
            content_dict.update(
                {
                    '任务状态': __parse_task_state(jmespath.search('taskstate', item))
                }
            )
            content_list.append(content_dict)
    return content_list


