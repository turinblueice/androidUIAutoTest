#-*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
finder模块,控件查找的基类

Authors: Turinblueice
Date:    16/3/15 12:04
"""
import datetime
import os
import time

from appium.webdriver.common.mobileby import MobileBy
from selenium import webdriver
from selenium.common import exceptions
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from base import thread_device_pool
from devices_manager import command_prompt
from util import config_initial, log


class BaseFrameViewMetaClass(type):

    def __new__(mcs, name, bases, dct):
        if 'by_dct' not in dct or not type(dct['by_dct']) == 'dict':
            dct['by_dct'] = dict()

        elem_list = ['elem', 'elems']
        dct['by_dct']['name'] = dict(zip(elem_list, ['find_element_by_accessibility_id',
                                                     'find_elements_by_accessibility_id']))
        dct['by_dct']['xpath'] = dict(zip(elem_list, ['find_element_by_xpath',
                                                      'find_elements_by_xpath']))
        dct['by_dct']['uiautomator'] = dict(zip(elem_list, ['find_element_by_android_uiautomator',
                                                            'find_elements_by_android_uiautomator']))
        dct['by_dct']['id'] = dict(zip(elem_list, ['find_element_by_id',
                                                   'find_elements_by_id']))
        # find_element_by_class_name("android.widget.EditText")
        dct['by_dct']['type'] = dict(zip(elem_list, ['find_element_by_class_name',
                                                     'find_elements_by_class_name']))
        dct['by_dct']['tag'] = dict(zip(elem_list, ['find_element_by_tag_name',
                                                    'find_elements_by_tag_name']))

        return super(BaseFrameViewMetaClass, mcs).__new__(mcs, name, bases, dct)


class BaseFrameView(object):

    """
    Summary:
        基础界面框架类,界面控件的父类,查找上层控件

    Attribute:
        _parent: 查找的父层,最底层即基层为驱动层driver

    """

    __metaclass__ = BaseFrameViewMetaClass

    def __init__(self, parent=None):

        super(BaseFrameView, self).__init__()
        self._parent = parent
        self._layout_view = None  # WebElement对象，等待子类实现
        self._scroll_view = None  # 可滑动区域对象，等待子类实现

    @property
    def parent(self):
        """
        Summary:
            返回父亲界面

        Return:
            返回对象的父亲界面对象
        """
        if isinstance(self._parent, BaseFrameView) or isinstance(self._parent, webdriver.Remote) or \
                isinstance(self._parent, WebElement):
            return self._parent
        return None

    @property
    def base_parent(self):
        curr_parent = self._parent

        #  如果当前的父界面是基础界面类型而不是webdriver.Remote类型,则追溯到最底层的父亲界面,最底层类型约定为webdrive.Remote类
        while not isinstance(curr_parent, webdriver.Remote) and isinstance(curr_parent, BaseFrameView):
            curr_parent = curr_parent.parent

        if isinstance(curr_parent, WebElement):
            curr_parent = curr_parent.parent
            return curr_parent

        if not isinstance(curr_parent, webdriver.Remote):
            curr_parent = None

        return curr_parent

    def __getattr__(self, item):

        return getattr(self.base_parent, item, None)

    def find_element(self, **kwargs):

        elem = None
        by_dct = getattr(self.__class__, 'by_dct')
        for key in kwargs:
            if key in by_dct:
                func = getattr(self.parent, by_dct[key]['elem'], None)
                if func:
                    elem = func(kwargs[key])
                    break
        return elem

    def find_elements(self, **kwargs):

        elems = None
        by_dct = getattr(self.__class__, 'by_dct')
        for key in kwargs:
            if key in by_dct:
                func = getattr(self.parent, by_dct[key]['elems'], None)
                if func:
                    elems = func(kwargs[key])
                    break
        return elems

    def save_screen_shot(self, name, image_dir=None):
        """

        :param name:
        :param image_dir:
        Args:
            name:截图保存名称
            image_dir: 保存图片目录名称
        Return:
        """
        now = datetime.datetime.now()
        now_str = now.strftime("%Y%m%d%H%M%S")
        today_str = now.strftime("%Y%m%d")
        default_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../outputs/screen_shots/'+today_str))

        screen_shot_dir = image_dir or default_dir
        if not os.path.isdir(screen_shot_dir):
            os.makedirs(screen_shot_dir)

        screen_shot_name = os.path.join(screen_shot_dir, 'test_'+name+'_'+now_str+'.png')

        try:
            log.logger.info("开始截图")
            self.base_parent.save_screenshot(screen_shot_name)
        except Exception:
            log.logger.info("使用官方提供的方法截图失败，使用自定义方法截图")
            device_info = thread_device_pool.ThreadDeviceInfoPool.get_current_device()
            device_udid = device_info['device_id']
            cp = command_prompt.CommandPrompt()
            ret_code1 = cp.run_command_sync(
                config_initial.config_parser.get('system_cmd', 'rm_image').replace('#device#', device_udid))[1]
            ret_code2 = cp.run_command_sync(
                config_initial.config_parser.get('system_cmd', 'create_image').replace('#device#', device_udid))[1]
            ret_code3 = cp.run_command_sync(config_initial.config_parser.get('system_cmd', 'pull_image').replace(
                '#device#', device_udid).replace('#filepath#', screen_shot_name))[1]
            if not ret_code1 == 0 or not ret_code2 == 0 or not ret_code3 == 0:
                log.logger.error("执行自定义截图命令出错")
                raise
        log.logger.info("截图已保存到目录:" + screen_shot_dir)

    # *************************************等待子元素出现***********************************
    def wait_for_element_present(self, parent=None, timeout=10, poll=0.5, **kwargs):
        """
            Summary:
                等待当前元素的子元素出现
            Args:
                parent: 父容器
                timeout: 等待时长
                poll: 检查间隔
                kwargs: id=''
        """
        parent = parent or self._layout_view
        by_dct = getattr(self.__class__, 'by_dct')
        key = kwargs.keys()[0]

        end_time = time.time() + timeout
        while True:
            try:
                func = getattr(parent, by_dct[key]['elem'])
                if func:
                    func(kwargs[key])
                    return True
                raise
            except NoSuchElementException:
                if time.time() > end_time:
                    break
                time.sleep(poll)
        return False

    def _manage_android_alert(self, alert_accept):
        """
            Summary:
                处理android系统弹框
            Args:
                alert_accept: 是否点击接受

        Returns:

        """

        title = self.base_parent.find_element(
            by=MobileBy.ANDROID_UIAUTOMATOR,
            value='new UiSelector().resourceIdMatches(".+id/alertTitle")').text
        # message = self.base_parent.find_element(by=MobileBy.ANDROID_UIAUTOMATOR,
        #                                         value='new UiSelector().resourceIdMatches(".+id/message")')

        # 提示框消息取消用ID的方法寻找, 使用类型的方式寻找, text_view类型首个元素为title, 第二个为message
        message = self.base_parent.find_elements(by=MobileBy.CLASS_NAME, value='android.widget.TextView')[1]
        log.logger.info("系统提示框显示:{}".format(message.text.encode('utf8')))
        # try:
        #     check_box = self.base_parent.find_element(by=MobileBy.CLASS_NAME, value='android.widget.CheckBox')
        #     log.logger.info("勾选\"不再提示\"的复选框")
        #     check_box.click()
        #     log.logger.info("\"不再提示\"的复选框勾选完毕")
        # except:
        #     pass

        if alert_accept:
            button = self.base_parent.find_element(
                by=MobileBy.ANDROID_UIAUTOMATOR,
                value='new UiSelector().resourceIdMatches(".+id/button1")')
            button_name = '确定'
        else:
            button = self.base_parent.find_element(
                by=MobileBy.ANDROID_UIAUTOMATOR,
                value='new UiSelector().resourceIdMatches(".+id/button2")')
            button_name = '取消\拒绝'

        log.logger.info("点击提示框遮罩的\"{}\"按钮".format(button_name))
        button.click()
        log.logger.info("已关闭\"{}\"提示框".format(title.encode('utf8')))
        time.sleep(1)

    def wait_for_element_present_under_alert(self, parent, timeout=10,
                                             poll=0.5,  check_count=3,
                                             alert_accept=True, **kwargs):
        """

        Summary:
                等待当前元素的子元素出现,如果被提示框遮罩影响,则关闭遮罩
        Args:
                parent: 父容器
                timeout: 等待时长
                check_count: 检查次数
                poll: 检查间隔
                alert_accept: 是否接受
                kwargs: id=''

        """
        status = self.wait_for_element_present(parent, timeout, poll, **kwargs)
        count = 0  # 重复检测次数
        while not status and count < check_count:
            # count表示提示框取消次数,最多取消3次,意思为最多支持同时出现三个提示框
            # 预期的元素没出现,检查是否是系统遮罩引起
            if self.wait_for_element_present(
                    self.base_parent, timeout=3,
                    uiautomator='new UiSelector().resourceIdMatches(".+id/parentPanel")'):  # 'parentPanel'
                log.logger.info("屏幕有提示框遮罩")

                self._manage_android_alert(alert_accept)  # 处理弹框
                status = self.wait_for_element_present(parent, timeout, poll, **kwargs) # 处理完毕后,再次检查是否具有指定控件
                count += 1  # 提示框取消后,再次找寻控件
                continue

            elif count > 0:
                log.logger.info("无系统提示框遮罩")
            break  # 若没有系统提示框,则直接退出
        return status

    def wait_for_system_alert(self, parent=None, timeout=10, poll=0.5, **kwargs):
        """
            Summary:
                等待系统提示框出现
            Args:
                parent: 父容器
                timeout: 等待时长
                poll: 检查间隔
                kwargs: id=''
        """

        if self.wait_for_element_present(parent, timeout, poll,
                                         uiautomator='new UiSelector().resourceIdMatches(".+id/parentPanel")'):
            log.logger.info("当前存在系统提示框")
            return True
        return False

    def wait_for_element_disappear(self, parent=None, timeout=10, poll=0.5, **kwargs):
        """
            Summary:
                等待当前元素消失
            Args:
                parent: 父容器
                timeout: 等待时长
                poll: 检查间隔
                kwargs: id=''
        """
        parent = parent or self._layout_view
        by_dct = getattr(self.__class__, 'by_dct')
        key = kwargs.keys()[0]

        end_time = time.time() + timeout
        while True:
            try:
                func = getattr(parent, by_dct[key]['elem'])
                if func:
                    func(kwargs[key])
                    if time.time() > end_time:
                        break
                    time.sleep(poll)
                else:
                    raise
            except NoSuchElementException:
                return True
        return False

    def wait_activity(self, activity_name, timeout=10, alert_accept=True):
        """
            Summary:
                等待活动页,封装driver的同名方法,增加对系统弹窗的判断
        Args:
            activity_name:
            timeout:
            alert_accept:
        Returns:

        """

        status = self.base_parent.wait_activity(activity_name, timeout)
        count = 0  # 重复次数
        while not status and count < 3:
            # count表示提示框取消次数,最多取消3次,意思为最多支持同时出现三个提示框
            # 预期的元素没出现,检查是否是系统遮罩引起
            if self.wait_for_element_present(
                    self.base_parent, timeout=4,
                    uiautomator='new UiSelector().resourceIdMatches(".+id/parentPanel")'):  # 'parentPanel'
                log.logger.info("屏幕有提示框遮罩")

                self._manage_android_alert(alert_accept)  # 处理遮罩
                status = self.base_parent.wait_activity(activity_name, timeout)  # 处理完毕后,再次检查是否进入新的活动页
                count += 1  # 提示框取消后,再次找寻控件
                continue
            log.logger.info("已无系统提示框遮罩")
            break  # 若没有系统提示框,则直接退出
        return status

    def wait_element_selected(self, locator=(), timeout=5):

        try:
            WebDriverWait(self.base_parent, timeout).until(
                EC.element_located_to_be_selected(locator)
            )
            log.logger.info("成功进入关注tab页面")
            return True

        except exceptions.TimeoutException:
            log.logger.error("进入关注tab页面失败")
            return False

    def wait_element_selected_under_alert(self, locator, timeout=5, alert_accept=True):

        status = self.wait_element_selected(locator, timeout)
        count = 0  # 重复次数
        while not status and count < 3:
            # count表示提示框取消次数,最多取消3次,意思为最多支持同时出现三个提示框
            # 预期的元素没出现,检查是否是系统遮罩引起
            if self.wait_for_element_present(
                    self.base_parent, timeout=4,
                    uiautomator='new UiSelector().resourceIdMatches(".+id/parentPanel")'):  # 'parentPanel'
                log.logger.info("屏幕有提示框遮罩")

                self._manage_android_alert(alert_accept)  # 处理遮罩
                status = self.wait_element_selected(locator, timeout)  # 处理完毕后,再次检查是否被选中
                count += 1  # 提示框取消后,再次找寻控件
                continue
            log.logger.info("已无系统提示框遮罩")
            break  # 若没有系统提示框,则直接退出
        return status


    # ***********************************元素的基础操作*****************************************  #

    def swipe_up(self, x, start_y, end_y, duration=None):
        """
            Summary:
                向上滑动
        """
        if end_y >= start_y:
            log.logger.error("向上滑动,结束位置不应大于起始位置")
            return None
        return self.base_parent.swipe(x, start_y, x, end_y, duration)

    def swipe_down(self, x, start_y, end_y, duration=None):
        """
            Summary:
                向下滑动
        """
        if end_y <= start_y:
            log.logger.error("向下滑动,结束位置不应小于起始位置")
            return None
        return self.base_parent.swipe(x, start_y, x, end_y, duration)

    def swipe_left(self, start_x, end_x, y, duration=None):
        """
            Summary:
                向左滑动
        """
        if start_x <= end_x:
            log.logger.error("向左滑动,结束位置不应大于起始位置")
            return None
        return self.base_parent.swipe(start_x, y, end_x, y, duration)

    def swipe_right(self, start_x, end_x, y, duration=None):
        """
            Summary:
                向右滑动
        """
        if start_x >= end_x:
            log.logger.error("向右滑动,结束位置不应小于起始位置")
            return None
        return self.base_parent.swipe(start_x, y, end_x, y, duration)

    def swipe_up_entire_scroll_view(self, x=None):
        """
            Summary:
                向上滑动整个scroll view的高度

        """
        location = self._scroll_view.location
        size = self._scroll_view.size
        x = x or location['x'] + size['width']/2
        start_y = location['y'] + size['height'] - 1
        end_y = location['y'] + 1

        log.logger.info("开始向上滑动整个可滑动区域的屏幕")
        self.swipe_up(x, start_y, end_y)
        log.logger.info("向上滑动结束")
        time.sleep(2)

    def swipe_down_entire_scroll_view(self):
        """
            Summary:
                向下滑动整个scroll view的高度
        """
        location = self._scroll_view.location
        size = self._scroll_view.size
        x = location['x'] + size['width']/2
        end_y = location['y'] + size['height'] - 1
        start_y = location['y'] + 1

        log.logger.info("开始向下滑动整个可滑动区域的屏幕")
        self.swipe_down(x, start_y, end_y)
        log.logger.info("向下滑动结束")
        time.sleep(2)

    def swipe_right_entire_scroll_view(self):
        """
            Summary:
                向上滑动整个scroll view的高度

        """
        location = self._scroll_view.location
        size = self._scroll_view.size
        y = location['y'] + size['height']/2
        start_x = location['x'] + 1
        end_x = location['x'] + size['width'] - 1

        log.logger.info("开始向右滑动整个可滑动区域的屏幕")
        self.swipe_right(start_x, end_x, y)
        log.logger.info("向右滑动结束")
        time.sleep(2)

    def swipe_left_entire_scroll_view(self):
        """
            Summary:
                向左滑动整个scroll view的高度

        """
        location = self._scroll_view.location
        size = self._scroll_view.size
        y = location['y'] + size['height']/2
        start_x = location['x'] + size['width'] - 1
        end_x = location['x'] + 1

        log.logger.info("开始向左滑动整个可滑动区域的屏幕")
        self.swipe_left(start_x, end_x, y)
        log.logger.info("向左滑动结束")
        time.sleep(2)

    def swipe_up_any_view(self, x=None, ratio=1):
        """
            Summary:
                向上滑动任意指定高度
            Args:
                x: 滑动的x坐标;
                ratio: 滑动的比率

        """
        location = self._scroll_view.location
        size = self._scroll_view.size
        x = x or location['x'] + size['width']/3
        start_y = location['y'] + size['height'] - 1
        end_y = location['y'] + size['height']*(1-ratio)

        log.logger.info("开始向上滑动整个可滑动区域的屏幕")
        self.swipe_up(x, start_y, end_y)
        log.logger.info("向上滑动结束")
        time.sleep(2)

    # **********************************系统方法************************************************  #

    def tap_window_center(self):
        """
            Summary:
                点击窗口中心
        :return:
        """
        size = self.base_parent.get_window_size()

        x = size['width']/2
        y = size['height']/2
        log.logger.info("点击屏幕中央")
        self.base_parent.tap([(x, y)])
        time.sleep(3)

    def tap_window_top(self):
        """
            Summary:
                点击窗口顶部
        :return:
        """
        size = self.base_parent.get_window_size()

        x = size['width']/2
        y = size['height']/10

        self.base_parent.tap([(x, y)])
        time.sleep(3)

    def wait_one_of_activities(self, activities=(), timeout=5, interval=1):
        """
            Summary:
                等待活动页列表中的某个页面出现
            Args:
                activities:活动页列表
                timeout:超时时间
                interval：间隔时间
        """
        try:
            WebDriverWait(self.base_parent, timeout, interval).until(
                lambda d: d.current_activity in activities)
            return True
        except TimeoutException:
            return False