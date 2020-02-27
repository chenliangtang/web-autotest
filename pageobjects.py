# -*- coding: utf-8 -*-
# 操作的类方法
import time
import os
import random
from datetime import datetime

from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException
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

targets = [0.1, 0.5, 0.7, 1, 2, 3, 4, 5, 7, 10]


class ScreenShot(object):
    """
    封装了用于截屏的公共类
    """
    def __init__(self, driver, root_dir, msg=''):
        """
        在初始化构造函数中把 webdriver 实例、截图保存的根路径和提示信息三个参数给存下来

        :param driver: webdriver 实例
        :param root_dir: 截图保存的根路径
        :param msg: 提示信息
        """
        self.driver = driver
        self.root_dir = root_dir
        self.msg = msg

    def screen_shot(self):
        """
        用于截屏的具体方法

        :return: 无返回值
        """
        img_name = self._get_img_name()
        msg = self.msg if self.msg != '' else '将进行截屏操作，作为操作失败的原因的记录'
        logger.debug(msg)
        try:
            succeed = self.driver.save_screenshot(img_name)
            if succeed:
                logger.info('截图操作成功， 图片名称为：{}'.format(img_name))
            else:
                logger.error('截图失败!!!')
        except TimeoutException as timeout:
            logger.error('截图失败，超时了: {}'.format(timeout))
        except Exception as e:
            logger.error('未知的异常发生导致截图失败！！！:{}'.format(e))

    def _get_img_name(self):
        return os.path.join(
            self.root_dir,
            '{}.png'.format(datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f'))
        )


class Login(ScreenShot):
    """
    继承用于截图的公共类 ScreenShot，并封装了用于多屏控制端登录的类
    """
    def __init__(self, driver):
        """
        继承 ScreenShot 构造函数，并保存用于登录操作的数据

        :param driver: webdriver 对象
        """
        super(Login, self).__init__(driver, 'screenshots\\login')
        self.url = CONFIG['common']['url']
        self.username = CONFIG['common']['username']
        self.password = CONFIG['common']['password']
        self.username_xpath = CONFIG['login']['username_xpath']
        self.password_xpath = CONFIG['login']['password_xpath']
        self.login_btn_xpath = CONFIG['login']['login_btn_xpath']
        self.start_title_xpath = CONFIG['homepage']['start_title_xpath']

    def login(self):
        """
        登录多屏控制端的具体方法

        :return: 无返回值
        """
        count = 0
        while count < 9999:
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
                self.screen_shot()
            except AssertionError as err:
                count += 1
                err_msg = '断言出错: {},当前页面下没有“文稿预览”元素 '.format(err)
                logger.error(err_msg)
                self.screen_shot()
            except Exception as e:
                count += 1
                logger.error("发生未知的异常：{},准备进行重试".format(e))

        if count >= 9999:
            logger.fatal('登陆重试{}次, 退出程序！！！'.format(count))
            self.screen_shot()
            raise Exception('重试了 {} 次登陆都失败了，抛出异常!!!'.format(count))


class Logout(ScreenShot):
    """
    继承用于截图的公共类 ScreenShot，并封装了用于多屏控制端登出的类
    """
    def __init__(self, driver):
        """
        继承 ScreenShot 构造函数，并保存用于登出操作的数据
        :param driver: webdriver 对象
        """
        super(Logout, self).__init__(driver, 'screenshots\\logout')
        self.exit_play_xpath = CONFIG['logout']['exit_play_xpath']
        self.logout_xpath = CONFIG['logout']['logout_xpath']

    def logout(self):
        """
        登出多屏控制端的具体方法

        :return: 无返回值
        """
        try:
            if element_exist(self.driver, self.exit_play_xpath):
                click_element(self.driver, self.exit_play_xpath, 15)
                logger.debug('退出播放')
            if element_exist(self.driver, self.logout_xpath):
                click_element(self.driver, self.logout_xpath, 15)
                logger.debug('退出系统')
            if self.driver:
                self.driver.close()
                logger.debug('关闭浏览器')
        except TimeoutException:
            logger.error('登出操作超时!!!')
            self.screen_shot()
            if self.driver:
                self.driver.close()
        except Exception as e:
            logger.error("发生未知的异常：{}".format(e))
            self.screen_shot()
            if self.driver:
                logger.info('关闭浏览器')
                self.driver.close()


class Controller(ScreenShot):
    """
    继承用于截图的公共类 ScreenShot，并封装了用于播放多屏操作的类，里面包含了各个操作多屏控制端的类方法
    """
    def __init__(self, driver):
        """
       继承 ScreenShot 构造函数，并保存用于控制操作相关的数据

       :param driver: webdriver 对象
       """
        super(Controller, self).__init__(driver, 'screenshots\\control')
        self.page_xpath = CONFIG['homepage']['nav_content_xpath']
        self.start_xpath = CONFIG['homepage']['start_xpath']
        self.next_xpath = CONFIG['homepage']['next_xpath']
        self.pre_xpath = CONFIG['homepage']['pre_xpath']
        self.nav_list_ct_xpath = CONFIG['homepage']['nav_list_ct_xpath']
        self.play_title_xpath = CONFIG['homepage']['play_title_xpath']
        self.preview_xpath = CONFIG['homepage']['preview_xpath']
        self.exit_play_xpath = CONFIG['logout']['exit_play_xpath']
        self.start_title_xpath = CONFIG['homepage']['start_title_xpath']
        self.change_screen_xpath = CONFIG['homepage']['change_screen_xpath']
        self.select_screen_xpath = CONFIG['homepage']['select_screen_xpath']
        self.select_screen_confirm_xpath = CONFIG['homepage']['select_screen_confirm_xpath']

    def select_screen(self):
        """
        用于切换显示屏，切换成宝安中控的大屏

        :return: 无返回值
        """
        click_element(self.driver, self.change_screen_xpath, 10)
        click_element(self.driver, self.select_screen_xpath)
        click_element(self.driver, self.select_screen_confirm_xpath)

    def choice_doc(self, doc_name):
        """
        用于选择要播放的文稿

        :param doc_name: 要播放的文稿名称
        :return: 选择成功就返回 True，否则 False
        """
        for times in range(1, 4):
            try:
                elements = wait_for_find_elements(self.driver, self.nav_list_ct_xpath, 15)
                for element in elements:
                    if element.text.strip() == doc_name:
                        logger.debug('找到文稿：{}'.format(doc_name))
                        print('找到文稿：{}'.format(doc_name))
                        element.click()
                        time.sleep(5)

                        logger.debug('并成功选择了找到的文稿')
                        print('并成功选择了找到的文稿')
                        return True
            except TimeoutException:
                logger.error('查找文稿列表超时失败')
                self.screen_shot()
                logger.error('查找文稿列表超时失败,将进行第 {} 次重试!'.format(times))
            except Exception as e:
                logger.error("发生未知的异常：{}，准备进行重试".format(e))
                self.screen_shot()
        else:
            logger.fatal('进行了 {} 次重试，查找文稿列表依然超时失败'.format(times))
            return False

    def start(self):
        """
        用于点击启动播放按钮

        :return: 点击成功就返回 True，否则 False
        """
        for times in range(1, 4):
            try:
                click_element(self.driver, self.start_xpath)
                logger.debug('点击播放文稿按钮')
                play_title_elem = wait_for_find_element(self.driver, self.play_title_xpath)
                logger.debug('断言 start_title_elem.text({}) == 文稿预览'.format(play_title_elem.text))
                assert play_title_elem.text.strip() == '文稿播放'
                logger.debug('成功启动文稿播放')
                return True
            except TimeoutException as timeout:
                err_msg = '点击播放文稿按钮出错: {},准备进行{}次重试'.format(timeout, times)
                logger.error(err_msg)
                self.screen_shot()
            except AssertionError as err:
                err_msg = '断言出错:{},准备进行{}次重试'.format(err, times)
                logger.error(err_msg)
                self.screen_shot()
            except Exception as e:
                logger.error("发生未知的异常：{}，准备进行重试".format(e))
                self.screen_shot()
        else:
            logger.fatal('重试了{}次还是启动播放失败'.format(times))
            return False

    def next(self):
        """
        进入播放文稿页面下，用于点击下一页按钮

        :return: 操作成功返回预览图对象，失败返回 False
        """
        time.sleep(random.choice(targets))
        for times in range(1, 4):
            try:
                click_element(self.driver, self.next_xpath)
                logger.debug('在文稿播放的状态点击下一页')
                preview_xpath_elem = wait_for_find_element(self.driver, self.preview_xpath)
                src = preview_xpath_elem.get_property('src')
                logger.info('预览图的 src 地址过长，省略打印。。。')
                return src
            except TimeoutException as timeout:
                err_msg = '在文稿播放的状态点击下一页时超时失败:{}，准备重试第{}次 '.format(timeout, times)
                logger.error(err_msg)
                self.screen_shot()
            except Exception as e:
                logger.error("发生未知的异常：{}，准备进行重试".format(e))
                self.screen_shot()
        else:
            logger.fatal('重试点击下一页按钮{}次了依然失败!!!'.format(times))
            return False

    def pre(self):
        """
        进入播放文稿页面下，用于点击上一页按钮

        :return: 操作成功返回预览图对象，失败返回 False
        """
        time.sleep(random.choice(targets))
        for times in range(1, 4):
            try:
                click_element(self.driver, self.pre_xpath)
                logger.debug('在文稿播放的状态点击上一页')
                preview_xpath_elem = wait_for_find_element(self.driver, self.preview_xpath)
                src = preview_xpath_elem.get_property('src')
                logger.info('成功获取预览图的 src 属性（src属性 过长，省略。。。）')
                return src
            except TimeoutException as timeout:
                err_msg = '在文稿播放的状态点击上一页时超时失败:{}，准备重试第{}次 '.format(timeout, times)
                logger.error(err_msg)
                self.screen_shot()
            except Exception as e:
                logger.error("发生未知的异常：{}，准备进行重试".format(e))
                self.screen_shot()
        else:
            logger.error('点击上一页按钮{}次了依然失败!!!'.format(times))
            return False

    def loop_play(self):
        """
        循环去播放一个文稿（一直按下一页下一页，到底后再按上一页上一页，如此反复）

        :return: 无返回值
        """
        for times in range(1, 11):
            print('loop_times: {}'.format(times))
            try:
                img_src_list = []
                while self.next_exist():
                    src = self.next()
                    if src is False:
                        logger.error('无法点击下一页元素，尝试去点击上一页')
                        break
                    img_src_list.append(src)
                    if len(img_src_list) == 2:
                        logger.info('进行两次操作后，准备断言前后两次操作的预览图不一致')
                        assert img_src_list[0] != img_src_list[1]
                        logger.info('断言成功，前后两次操作的预览图不一致')
                        img_src_list.pop(0)
                img_src_list.clear()
                while self.pre_exist():
                    src = self.pre()
                    if src is False:
                        logger.error('无法点击上一页元素，尝试去点击下一页')
                        break
                    img_src_list.append(src)
                    if len(img_src_list) == 2:
                        logger.info('进行两次操作后，准备断言前后两次操作的预览图不一致')
                        assert img_src_list[0] != img_src_list[1]
                        logger.info('断言成功，前后两次操作的预览图不一致')
                        img_src_list.pop(0)
            except AssertionError:
                logger.error('断言失败，原因可能是上一页或下一页按钮不可点击；'
                             '又或者按钮点击了预览图没有更新，请看下方截图。')
                self.screen_shot()
            except StaleElementReferenceException as sere:
                logger.error('过期元素引用异常:{}'.format(sere))
                self.screen_shot()
            except Exception as e:
                logger.error("发生未知的异常：{}，准备进行重试".format(e))
                self.screen_shot()

        if self.exit_play_exist():
            try:
                click_element(self.driver, self.exit_play_xpath)
                logger.debug('退出播放')
                print('退出播放')
                start_title_elem = wait_for_find_element(self.driver, self.start_title_xpath, 20)
                logger.info('找到文稿预览元素，成功退出播放')
                logger.info('准备断言退出播放成功')
                assert start_title_elem.text.strip() == '文稿预览'
                logger.debug('断言退出播放成功')
            except TimeoutException:
                logger.error('无法找到文稿预览元素，已超时')
                print('无法找到文稿预览元素，已超时')
                self.screen_shot()
            except AssertionError:
                logger.error('断言退出播放失败')
                self.screen_shot()
            except Exception as e:
                logger.error("发生未知的异常：{}，准备进行重试".format(e))
                self.screen_shot()

    def pre_exist(self):
        """
        判断播放状态下的上一页按钮是否存在

        :return: 存在返回该元素，不存在返回 False
        """
        return element_exist(self.driver, self.pre_xpath)

    def next_exist(self):
        """
        判断播放状态下的下一页按钮是否存在

        :return: 存在返回该元素，不存在返回 False
        """
        return element_exist(self.driver, self.next_xpath)

    def exit_play_exist(self):
        """
        判断退出播放的按钮是否存在

        :return: 存在返回该元素，不存在返回 False
        """
        return element_exist(self.driver, self.exit_play_xpath)




