#-*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明:该模块为主页面底部tab栏
 
Authors: Turinblueice
Date:    16/3/16 16:46
"""

from base import base_frame_view
from gui_widgets.basic_widgets import relative_layout
from gui_widgets.basic_widgets import tab_widget

from util import log

from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from activities import activities

from selenium.common import exceptions

import time


class BottomTabWidget(base_frame_view.BaseFrameView):
    """
        Summary:
            主页面底部的tab栏组件
    """

    center_tab_title_value = u'我的'  #  中心tab的title，用于定位当前页面位于中心tab

    def __init__(self, parent):
        super(BottomTabWidget, self).__init__(parent)
        self.__id = "com.jiuyan.infashion:id/ll_tab"
        self.__tab_view = tab_widget.TabWidget(self.parent, id=self.__id)

    @property
    def focus_tab(self):
        """
            Summary:
                关注tab
        """
        xpath_ = '//android.widget.TabWidget[@resource-id="android:id/tabs"]/android.widget.RelativeLayout[1]'
        return relative_layout.RelativeLayout(self.base_parent, xpath=xpath_)

    @property
    def discovery_tab(self):
        """
            Summary:
                发现tab
        """
        xpath_ = '//android.widget.TextView[@resource-id=\"com.jiuyan.infashion:id/main_tab_title\" and @text=\"发现\"]'
        return relative_layout.RelativeLayout(self.base_parent, xpath=xpath_)

    @property
    def camera_tab(self):
        """
            Summary:
                相机tab
        """
        id_ = 'com.jiuyan.infashion:id/id_ib_button'
        return relative_layout.RelativeLayout(self.base_parent, id=id_)

    @property
    def in_note_tab(self):
        """
            Summary:
                in记tab
        """
        xpath_ = '//android.widget.TabWidget[@resource-id="android:id/tabs"]/android.widget.RelativeLayout[4]'
        return relative_layout.RelativeLayout(self.base_parent, xpath=xpath_)

    @property
    def center_tab(self):
        """
            Summary:
                中心tab
        """
        xpath_ = '//android.widget.TabWidget[1]/android.widget.RelativeLayout[5]'
        return relative_layout.RelativeLayout(self.base_parent, xpath=xpath_)

    # ********************* 操作方法************************

    def tap_center_tab(self, timeout=10):
        """
            Summary:
                点击中心tab
            Args：
                timeout: 等待时长
        """
        log.logger.info("开始点击中心tab")
        self.center_tab.tap()
        log.logger.info("中心tab点击完毕")

        if self.wait_for_element_present_under_alert(self.base_parent, id='com.jiuyan.infashion:id/title_bar'):
            log.logger.info("成功进入中心tab页面")
            return True

        log.logger.error("进入中心tab页面失败")
        return False

    def tap_focus_tab(self, wait_bubble=True, timeout=4):
        """
            Summary:
                点击关注tab
            Args：
                timeout: 等待时长
        """
        log.logger.info("等待相机气泡消失再点击发现按钮")
        while wait_bubble and self.wait_for_element_present(self.base_parent, timeout=5,
                                                            id='com.jiuyan.infashion:id/id_fl_parster'):
            log.logger.info("相机气泡存在，继续等待5秒")
            time.sleep(5)

        log.logger.info("开始点击关注tab")
        self.focus_tab.tap()
        log.logger.info("关注tab点击完毕")

        if self.wait_element_selected_under_alert(
                (MobileBy.XPATH, '//android.widget.TabWidget[1]/android.widget.RelativeLayout[1]'), timeout):
            log.logger.info("成功进入关注tab页面")
            return True
        log.logger.error("进入关注tab页面失败")
        return False

    def tap_discover_tab(self, wait_bubble=True, timeout=10):
        """
            Summary:
                点击发现tab
            Args:
                wait_bubble: True:等待相机气泡,False:不等待相机气泡
                timeout: 等待时长
        """
        log.logger.info("等待相机气泡消失再点击发现按钮")
        while wait_bubble and self.wait_for_element_present(self.base_parent, timeout=5, id='com.jiuyan.infashion:id/id_fl_parster'):
            log.logger.info("相机气泡存在，继续等待5秒")
            time.sleep(5)

        log.logger.info("开始点击发现tab")
        self.discovery_tab.tap()
        log.logger.info("发现tab点击完毕")
        if self.wait_element_selected_under_alert(
                (MobileBy.XPATH,
                 '//android.widget.TextView[@resource-id=\"com.jiuyan.infashion:id/main_tab_title\" and @text=\"发现\"]'),
                timeout):
            log.logger.info("成功进入发现tab页面")
            return True
        log.logger.error("进入发现tab页面失败")
        return False

    def tap_camera_tab(self, wait_bubble=True, timeout=10):
        """
            Summary:
                点击拍照tab
            Args：
                wait_bubble: True:等待相机气泡,False:不等待相机气泡
                timeout: 等待时长
        """
        log.logger.info("等待相机气泡消失再点击相机按钮")
        while wait_bubble and self.wait_for_element_present(self.base_parent, timeout=5, id='com.jiuyan.infashion:id/id_fl_parster'):
            log.logger.info("相机气泡存在，继续等待5秒")
            time.sleep(3)

        log.logger.info("开始点击拍照tab")
        self.camera_tab.tap()
        log.logger.info("拍照tab点击完毕")
        if self.base_parent.wait_activity(activities.ActivityNames.CAMERA2, timeout):
            log.logger.info("成功进入拍照页面")
            return True
        log.logger.error("进入拍照页面失败")
        return False

    def tap_in_diary_tab(self, timeout=10):
        """
            Summary:
                点击in记tab
            Args：
                timeout: 等待时长
        """
        log.logger.info("开始点击in记tab")
        self.in_note_tab.tap()
        log.logger.info("in记点击完毕")
        if self.wait_element_selected_under_alert(
                (MobileBy.XPATH, '//android.widget.TabWidget[1]/android.widget.RelativeLayout[4]'), timeout):
            log.logger.info("成功进入in记tab页面")
            return True
        log.logger.error("进入in记tab页面失败")
        return False
