# -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明:class:WebElement基础页面控件的封装

Authors: Turinblueice
Date:    16/3/16 12:12
"""

from base import base_frame_view
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException

from util import log
import time


class BaseMobileElement(base_frame_view.BaseFrameView):
    """
        Attributes:
            parent:父容器对象
            element:mobile_element元素
            alert_accept: 提示框遮罩处理方式,True:点击确定;False:点击取消
    """
    def __init__(self, parent, element=None, alert_accept=True, **kwargs):
        super(BaseMobileElement, self).__init__(parent)
        while True:
            try:
                self._element = element if isinstance(element, WebElement) else self.find_element(**kwargs)
                break
            except NoSuchElementException as exp:
                #  未找到该元素,判断是否是被提示框遮挡
                if self.wait_for_element_present(
                        self.base_parent, uiautomator='new UiSelector().resourceIdMatches(".+id/parentPanel")'):  #'alertTitle'
                    log.logger.info("屏幕有提示框遮罩")

                    # title = self.base_parent.find_element(
                    #     by=MobileBy.ANDROID_UIAUTOMATOR,
                    #     value='new UiSelector().resourceIdMatches(".+id/alertTitle")').text
                    # # 提示框消息取消用ID的方法寻找, 使用类型的方式寻找, text_view类型首个元素为title, 第二个为message
                    # message = self.base_parent.find_elements(by=MobileBy.CLASS_NAME, value='android.widget.TextView')[1]
                    # log.logger.info("系统提示框显示:{}".format(message.text.encode('utf8')))
                    # try:
                    #     check_box = self.base_parent.find_element(by=MobileBy.CLASS_NAME, value='android.widget.CheckBox')
                    #     log.logger.info("勾选复选框")
                    #     check_box.click()
                    # except:
                    #     pass
                    #
                    # if alert_accept:
                    #     button = self.base_parent.find_element(
                    #         by=MobileBy.ANDROID_UIAUTOMATOR,
                    #         value='new UiSelector().resourceIdMatches(".+id/button1")')
                    #     button_name = '确定'
                    # else:
                    #     button = self.base_parent.find_element(
                    #         by=MobileBy.ANDROID_UIAUTOMATOR,
                    #         value='new UiSelector().resourceIdMatches(".+id/button2")')
                    #     button_name = '取消\拒绝'
                    #
                    # log.logger.info("点击提示框遮罩的\"{}\"按钮".format(button_name))
                    # button.click()
                    # log.logger.info("已关闭\"{}\"提示框".format(title.encode('utf8')))
                    self._manage_android_alert(alert_accept)
                    continue   # 处理完引导提示后再寻找一次原元素

                # 非提示框遮挡却找不到元素,则抛出异常
                log.logger.info("没有找到该元素,也未发现提示框遮罩")
                raise exp

    def __getattr__(self, item):
        return getattr(self._element, item, None)

    def tap(self, timeout=0.5):
        """
        :param timeout 等待时间
        Args:
            
        Returns:
        Raises
        """
        self._element.click()
        self.base_parent.implicitly_wait(timeout)


class BaseMobileElementList(base_frame_view.BaseFrameView):
    """

    """
    def __init__(self, parent, alert_accept=True, **kwargs):
        super(BaseMobileElementList, self).__init__(parent)

        while True:
            try:
                self._element_list = self.find_elements(**kwargs)
                break
            except NoSuchElementException as exp:
                #  未找到该元素,判断是否是被提示框遮挡
                if self.wait_for_element_present(
                        self.base_parent,
                        uiautomator='new UiSelector().resourceIdMatches(".+id/parentPanel")'):  # 'alertTitle'
                    log.logger.info("屏幕有提示框遮罩")

                    title = self.base_parent.find_element(
                        by=MobileBy.ANDROID_UIAUTOMATOR,
                        value='new UiSelector().resourceIdMatches(".+id/alertTitle")').text
                    message = self.base_parent.find_element(by=MobileBy.ANDROID_UIAUTOMATOR,
                                                            value='new UiSelector().resourceIdMatches(".+id/message")')
                    log.logger.info("系统提示框显示:{}".format(message.text.encode('utf8')))
                    try:
                        check_box = self.base_parent.find_element(by=MobileBy.CLASS_NAME,
                                                                  value='android.widget.CheckBox')
                        log.logger.info("勾选复选框")
                        check_box.click()
                    except:
                        pass

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
                    time.sleep(3)
                    continue  # 处理完引导提示后再寻找一次原元素

                # 非提示框遮挡却找不到元素,则抛出异常
                log.logger.info("没有找到该元素,也未发现提示框遮罩")
                raise exp

    @property
    def element_list(self):

        return [BaseMobileElement(element.parent, element) for element in self._element_list]


