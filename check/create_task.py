# -*- coding: utf-8 -*-

import requests
import json

from utils import CONFIG

category_and_id = {
    '全部': None,
    '防洪排涝和排水类': '2c93808e6bacbd79016be3ea8d01040d',
    '水资源和水土保持类': '2c93808e6bacbd79016be3ea4160040b',
    '在建水务工程类': '2c93808e6bacbd79016be3eabbc8040e'
}

category_and_id = {
    '测试类别': '2c9380956ca7bcc1016ca868313d0000',
    '防洪排涝和排水类': '2c93808e6bacbd79016be3ea8d01040d',
    '水资源和水土保持类': '2c93808e6bacbd79016be3ea4160040b',
    '在建水务工程类': '2c93808e6bacbd79016be3eabbc8040e'
}

territory_and_id = {
    '新安': '2c9380826c2df926016c4274debc0048',
    '西乡': '2c9380826c2df926016c42763c07004a',
    '航城': '2c9380826c2df926016c42767c37004b',
    '福永': '2c9380826c2df926016c427925480052',
    '福海': '2c9380826c2df926016c427946a10053',
    '新桥': '2c9380826c2df926016c4279675d0054',
    '沙井': '2c9380826c2df926016c4279a0e70055',
    '燕罗': '2c9380826c2df926016c4279c8cc0056',
    '石岩': '2c9380826c2df926016c427a28620057',
    '松岗': '2c9380826c2df926016c4278ead60051'
}

request = requests.session()
hostname = CONFIG['common']['hostname']


def available_sc_objs():
    '''统计可用的抽查对象

    Return：
        >>> _list(list)

    Example:
        >>> _list =
            [
                ['水资源和水土保持类', '新安', 2],
                ['水资源和水土保持类', '西乡', 4],
                ['水资源和水土保持类', '航城', 1]
            ]
    '''
    _list = []
    path = '/api/shuangsuiji/category/getMatters'
    url = hostname + path
    for category_name, category_id in category_and_id.items():
        for territory_name, territory_id in territory_and_id.items():
            params = {
                        'categoryid': category_id,
                        'territory': territory_id
                     }
            response = request.get(url, params=params)
            dict_content = json.loads(response.content)
            count = 0
            for item in dict_content['data']:
                if item['mattername'] == '备案抽查':
                    count += item['bxdx']
            if count > 1:
                _list.append([category_name, territory_name, count])
    return _list


def available_departments_checker():
    '''统计可用的检查部门

    Return：
        >>> _list(list)

    Example:
        >>> _list =
           [
               {'长流陂水库管理站': 9},
               {'防洪排涝和排水管理科': 21},
               {'测试部': 5},
               {'技术监管中心': 56}
           ]
    '''
    path = '/api/shuangsuiji/department/getDepartments'
    url = hostname + path
    response = request.get(url, params={'type': '检查科室'})
    dict_content = json.loads(response.content)
    _list = []
    for item in dict_content:
        if item['bxrs'] > 1:
            _list.append({item['departmentname']: item['bxrs']})
    return _list


def available_detachment_checker():
    '''统计可用的检查中队

    Return：
        >>> _list(list)

    Example:
        >>> _list =
           [
               {'福海水政监察中队': 16},
               {'新安水政监察中队': 10},
               {'西乡水政监察中队': 17},
               {'航城水政监察中队': 16}
           ]
    '''
    path = '/api/shuangsuiji/department/getDepartments'
    url = hostname + path
    response = request.get(url, params={'type': '备选'})
    dict_content = json.loads(response.content)
    _list = []
    for item in dict_content:
        if item['bxrs'] > 1:
            _list.append({item['departmentname']: item['bxrs']})
    return _list