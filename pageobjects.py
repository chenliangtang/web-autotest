# -*- coding: utf-8 -*-

import time
import os

from selenium.common.exceptions import TimeoutException
from utils import click_element, \
    input_text, \
    wait_for_find_element, \
    wait_for_find_elements, \
    wait_until_all_elements_visible

from parseconfig import CONFIG
from logger import Logger

logger = Logger().get_logger()


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
        except TimeoutException as timeout:
            err_msg = '登录出错: {}\n程序退出!\n '.format(timeout)
            logger.error(err_msg)
            if self.driver:
                self.driver.close()
        except AssertionError as err:
            err_msg = '断言出错: {}\n程序退出!\n '.format(err)
            logger.error(err_msg)
            if self.driver:
                self.driver.close()


class Logout(object):
    def __init__(self, driver):
        self.driver = driver
        self.exit_play_xpath = CONFIG['logout']['exit_play_xpath']
        self.logout_xpath = CONFIG['logout']['logout_xpath']

    def logout(self):
        try:
            click_element(self.driver, self.exit_play_xpath)
            logger.debug('退出播放')
            click_element(self.driver, self.logout_xpath)
            logger.debug('退出系统')
            if self.driver:
                self.driver.close()
                logger.debug('关闭浏览器')
        except TimeoutException as te:
            err_msg = '退出出错: {}\n程序退出!\n '.format(te)
            logger.error(err_msg)
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

    def test(self):
        logger.debug('--Controller > test() ---')
        elems = wait_for_find_elements(self.driver, self.nav_list_ct_xpath)
        print(len(elems))
        print('-------------')
        for elem in elems:
            print(elem.text)
            if elem.text.strip() == 'test11':
                elem.click()
                print(elem.text, elem.is_displayed())
                print(elem.text, elem.is_enabled())
                print(elem.text, elem.is_selected())
            print(elem.text, elem.is_displayed())
            print(elem.text, elem.is_enabled())
            print(elem.text, elem.is_selected())

    def start(self):
        try:
            # wait_until_all_elements_visible(self.driver, '/html/body')
            # logger.debug('等待登录成功后所有页面元素都加载出来')
            click_element(self.driver, self.start_xpath)
            logger.debug('点击播放文稿按钮')
            play_title_elem = wait_for_find_element(self.driver, self.play_title_xpath)
            logger.debug('断言 start_title_elem.text({}) == 文稿预览'.format(play_title_elem.text))
            assert play_title_elem.text.strip() == '文稿播放'
        except TimeoutException as timeout:
            err_msg = '点击播放文稿按钮出错: {}\n程序退出!\n '.format(timeout)
            logger.error(err_msg)
            if self.driver:
                self.driver.close()
                logger.debug('关闭浏览器')
        except AssertionError as err:
            err_msg = '断言出错: {}\n程序退出!\n '.format(err)
            logger.error(err_msg)
            if self.driver:
                self.driver.close()
                logger.debug('关闭浏览器')

    def next(self):
        try:
            click_element(self.driver, self.next_xpath)
            logger.debug('在文稿播放的状态点击下一页')
            preview_xpath_elem = wait_for_find_element(self.driver, self.preview_xpath)
            src = preview_xpath_elem.get_property('src')
            logger.info('预览图的 src = src 地址过长，省略。。。')
            # logger.info('预览图的 src = {}'.format(src))
            return src
        except TimeoutException as te:
            err_msg = '在文稿播放的状态点击下一页时出错: {}\n程序退出!\n '.format(te)
            logger.error(err_msg)
            if self.driver:
                self.driver.close()
                logger.debug('关闭浏览器')

    def pre(self):
        try:
            click_element(self.driver, self.pre_xpath)
            logger.debug('在文稿播放的状态点击上一页')
            preview_xpath_elem = wait_for_find_element(self.driver, self.preview_xpath)
            src = preview_xpath_elem.get_property('src')
            logger.info('预览图的 src = src 地址过长，省略。。。')
            # logger.info('预览图的 src = {}'.format(src))
            return src
        except TimeoutException as te:
            err_msg = '在文稿播放的状态点击上一页时出错: {}\n程序退出!\n '.format(te)
            logger.error(err_msg)
            if self.driver:
                self.driver.close()
                logger.debug('关闭浏览器')

    def loop_play(self):
        count = 0
        while True:
            try:
                srcs_list = []
                while self.next_exist():
                    src = self.next()
                    srcs_list.append(src)
                    if len(srcs_list) == 2:
                        logger.info('预览图的 src = src 地址过长，省略。。。')
                        # logger.info('srcs_list = {}'.format(srcs_list))
                        logger.info('比较 srcs_list[0] != srcs_list[1]')
                        assert srcs_list[0] != srcs_list[1]
                        srcs_list.pop(0)
                srcs_list.clear()
                while self.pre_exist():
                    src = self.pre()
                    srcs_list.append(src)
                    if len(srcs_list) == 2:
                        logger.info('预览图的 src = src 地址过长，省略。。。')
                        # logger.info('srcs_list = {}'.format(srcs_list))
                        logger.info('比较 srcs_list[0] != srcs_list[1]')
                        assert srcs_list[0] != srcs_list[1]
                        srcs_list.pop(0)
            except AssertionError as err:
                count += 1
                logger.error('断言失败的次数是：{}\n 当前程序或网络不稳定'.format(count))
                if count >= 999:
                    logger.fatal('有 999 次断言失败，退出程序')
                    logger.fatal(err)
                    if self.driver:
                        self.driver.close()

    def pre_exist(self):
        try:
            return wait_for_find_element(self.driver, self.pre_xpath)
        except TimeoutException:
            logger.info('pre 上一页元素不存在')
            return False

    def next_exist(self):
        try:
            return wait_for_find_element(self.driver, self.next_xpath)
        except TimeoutException:
            logger.info('next 下一页元素不存在')
            return False

    # def __del__(self):
    #     if self.driver:
    #         self.driver.close()