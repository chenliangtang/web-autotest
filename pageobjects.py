# -*- coding: utf-8 -*-

import time
import os
import random

from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    InvalidSessionIdException
)
from utils import (
    click_element,
    input_text,
    wait_for_find_element,
    wait_for_find_elements,
    element_exist
)

from parseconfig import CONFIG
from logger import Logger

logger = Logger().get_logger()

targets = [0.1, 0.5, 0.7, 1, 2, 3, 4, 5]


class Login(object):
    def __init__(self, driver):
        self.driver = driver
        self.url = CONFIG['common']['url']
        self.username = CONFIG['common']['username']
        self.password = CONFIG['common']['password']
        self.username_xpath = CONFIG['login']['username_xpath']
        self.password_xpath = CONFIG['login']['password_xpath']
        self.login_btn_xpath = CONFIG['login']['login_btn_xpath']
        self.start_title_xpath = CONFIG['homepage']['start_title_xpath']

    def login(self):
        count = 0
        while count < 5:
            try:
                self.driver.get(self.url)
                logger.debug('打开主页，进入登录页')
                self.driver.maximize_window()
                logger.debug('最大化窗口')
                input_text(self.driver, self.username_xpath, self.username)
                logger.debug('在登录页输入用户名')
                input_text(self.driver, self.password_xpath, self.password)
                logger.debug('在登录页输入密码')
                click_element(self.driver, self.login_btn_xpath)
                logger.debug('点击登陆按钮')
                start_title_elem = wait_for_find_element(self.driver, self.start_title_xpath)
                logger.debug('断言 start_title_elem.text({}) == 文稿预览'.format(start_title_elem.text))
                assert start_title_elem.text.strip() == '文稿预览'
                logger.debug('登陆成功')
                break
            except TimeoutException as timeout:
                count += 1
                err_msg = '登录超时: {},准备进行第{}次重试 '.format(timeout, count)
                logger.error(err_msg)
            except AssertionError as err:
                count += 1
                err_msg = '断言出错: {},当前业务没有“文稿预览”元素 '.format(err)
                logger.error(err_msg)
        if self.driver and count >= 5:
            logger.fatal('登陆重试{}次, 退出程序！！！'.format(count))
            self.driver.close()


class Logout(object):
    def __init__(self, driver):
        self.driver = driver
        self.exit_play_xpath = CONFIG['logout']['exit_play_xpath']
        self.logout_xpath = CONFIG['logout']['logout_xpath']

    def logout(self):
        try:
            if element_exist(self.driver, self.exit_play_xpath):
                click_element(self.driver, self.exit_play_xpath)
                logger.debug('退出播放')
            if element_exist(self.driver, self.logout_xpath):
                click_element(self.driver, self.logout_xpath)
                logger.debug('退出系统')
            if self.driver:
                self.driver.close()
                logger.debug('关闭浏览器')
        except TimeoutException:
            logger.error('登出操作超时，将关闭浏览器')
            if self.driver:
                self.driver.close()


class Controller(object):
    def __init__(self, driver):
        self.driver = driver
        self.page_xpath = CONFIG['homepage']['nav_content_xpath']
        self.start_xpath = CONFIG['homepage']['start_xpath']
        self.next_xpath = CONFIG['homepage']['next_xpath']
        self.pre_xpath = CONFIG['homepage']['pre_xpath']
        self.nav_list_ct_xpath = CONFIG['homepage']['nav_list_ct_xpath']
        self.play_title_xpath = CONFIG['homepage']['play_title_xpath']
        self.preview_xpath = CONFIG['homepage']['preview_xpath']
        self.exit_play_xpath = CONFIG['logout']['exit_play_xpath']
        self.start_title_xpath = CONFIG['homepage']['start_title_xpath']

    def choice_doc(self, doc_name):
        try:
            elements = wait_for_find_elements(self.driver, self.nav_list_ct_xpath)
            for element in elements:
                if element.text.strip() == doc_name:
                    logger.debug('找到文稿：{}'.format(doc_name))
                    print('找到文稿：{}'.format(doc_name))
                    element.click()
                    logger.debug('并成功选择了找到的文稿')
                    print('并成功选择了找到的文稿')
                    return True
        except TimeoutException:
            logger.error('选择文稿超时失败')
            return False

    def start(self):
        count = 0
        while count < 5:
            try:
                click_element(self.driver, self.start_xpath)
                logger.debug('点击播放文稿按钮')
                play_title_elem = wait_for_find_element(self.driver, self.play_title_xpath)
                logger.debug('断言 start_title_elem.text({}) == 文稿预览'.format(play_title_elem.text))
                assert play_title_elem.text.strip() == '文稿播放'
                logger.debug('成功启动文稿播放')
                return True
            except TimeoutException as timeout:
                count += 1
                err_msg = '点击播放文稿按钮出错: {},准备进行{}次重试'.format(timeout, count)
                logger.error(err_msg)

            except AssertionError as err:
                count += 1
                err_msg = '断言出错:{},准备进行{}次重试'.format(err, count)
                logger.error(err_msg)
        if count >= 5:
            logger.error('重试了{}次还是启动播放失败'.format(count))
            return False

    def next(self):
        time.sleep(random.choice(targets))
        count = 0
        while count < 3:
            try:
                click_element(self.driver, self.next_xpath)
                logger.debug('在文稿播放的状态点击下一页')
                preview_xpath_elem = wait_for_find_element(self.driver, self.preview_xpath)
                src = preview_xpath_elem.get_property('src')
                logger.info('预览图的 src = src 地址过长，省略。。。')
                return src
            except TimeoutException as timeout:
                count += 1
                err_msg = '在文稿播放的状态点击下一页时超时失败:{}，准备重试第{}次 '.format(timeout, count)
                logger.error(err_msg)

        if count >= 3:
            logger.fatal('重试点击上一页按钮{}次失败'.format(count))
            return False

    def pre(self):
        time.sleep(random.choice(targets))
        count = 0
        while count < 3:
            try:
                click_element(self.driver, self.pre_xpath)
                logger.debug('在文稿播放的状态点击上一页')
                preview_xpath_elem = wait_for_find_element(self.driver, self.preview_xpath)
                src = preview_xpath_elem.get_property('src')
                logger.info('成功获取预览图的 src 属性（src属性 过长，省略。。。）')
                return src
            except TimeoutException as timeout:
                count += 1
                err_msg = '在文稿播放的状态点击上一页时超时失败:{}，准备重试第{}次 '.format(timeout, count)
                logger.error(err_msg)

        if count >= 3:
            logger.fatal('重试点击上一页按钮{}次失败，关闭浏览器'.format(count))
            return False

    def loop_play(self):
        for loop_times in range(1, 4):
            print('loop_times: {}'.format(loop_times))
            try:
                srcs_list = []
                while self.next_exist():
                    src = self.next()
                    if src is False:
                        logger.info('无法点击下一页元素，尝试去点击上一页')
                        break
                    srcs_list.append(src)
                    if len(srcs_list) == 2:
                        logger.info('预览图的 src = src 地址过长，省略。。。')
                        logger.info('比较 srcs_list[0] != srcs_list[1]')
                        assert srcs_list[0] != srcs_list[1]
                        srcs_list.pop(0)
                srcs_list.clear()
                while self.pre_exist():
                    src = self.pre()
                    if src is False:
                        logger.info('无法点击上一页元素，尝试去点击下一页')
                        break
                    srcs_list.append(src)
                    if len(srcs_list) == 2:
                        logger.info('预览图的 src = src 地址过长，省略。。。')
                        # logger.info('srcs_list = {}'.format(srcs_list))
                        logger.info('比较 srcs_list[0] != srcs_list[1]')
                        assert srcs_list[0] != srcs_list[1]
                        srcs_list.pop(0)
            except AssertionError:
                logger.error('断言失败，原因可能是上一页或下一页按钮不可点击；'
                             '又或者按钮点击了预览图没有更新！')
            except StaleElementReferenceException as sere:
                msg = '过期元素引用异常:{}'.format(sere)
                logger.error(msg)
        if element_exist(self.driver, self.exit_play_xpath):
            click_element(self.driver, self.exit_play_xpath)
            logger.debug('退出播放')
            print('退出播放')
            try:
                start_title_elem = wait_for_find_element(self.driver, self.start_title_xpath, 20)
                logger.info('成功找到文稿预览元素')
            except TimeoutException:
                logger.error('无法找到文稿预览元素，已超时')
                print('无法找到文稿预览元素，已超时')
            try:
                assert start_title_elem.text.strip() == '文稿预览'
                logger.debug('页面已经显示文稿预览字样，退出播放成功')
            except AssertionError:
                logger.error('退出播放失败')

    def pre_exist(self):
        return element_exist(self.driver, self.pre_xpath)

    def next_exist(self):
        return element_exist(self.driver, self.next_xpath)
