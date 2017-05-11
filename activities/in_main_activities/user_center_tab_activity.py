#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: IN主页-中心tab页面

Authors: Turinblueice
Date: 2016/7/27
"""
from base import base_frame_view
from util import log

from gui_widgets.basic_widgets import text_view
from gui_widgets.basic_widgets import relative_layout
from gui_widgets.basic_widgets import linear_layout
from gui_widgets.basic_widgets import scroll_view

from activities import activities

from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import time


class UserCenterTabActivity(base_frame_view.BaseFrameView):

    """
        Summary:
            In主页面-用户中心tab

        Attributes:

    """
    name = '.InActivity'

    def __init__(self, parent):
        super(UserCenterTabActivity, self).__init__(parent)
        self._scroll_view = scroll_view.ScrollView(self.parent, type='android.widget.ScrollView')

    @property
    def title(self):
        """
            Summary:
                活动页标题
        """
        id_ = "com.jiuyan.infashion:id/title_bar"
        return text_view.TextView(self.parent, id=id_).text

    @property
    def user_head_bar(self):
        """
            Summary:
                用户头部信息栏，包括头像
        """
        id_ = 'com.jiuyan.infashion:id/usercenter_rl_header'
        return relative_layout.RelativeLayout(self._scroll_view, id=id_)

    @property
    def my_friends_bar(self):
        """
            Summary:
                我的好友栏
        """
        id_ = 'com.jiuyan.infashion:id/usercenter_my_friend'
        return relative_layout.RelativeLayout(self._scroll_view, id=id_)

    @property
    def paster_bar(self):
        """
            Summary:
                我的贴纸栏
        """
        id_ = 'com.jiuyan.infashion:id/usercenter_my_paster'
        return relative_layout.RelativeLayout(self._scroll_view, id=id_)

    @property
    def setting_bar(self):
        """
            Summary:
                设置栏
        """
        id_ = "com.jiuyan.infashion:id/usercenter_setting"
        return linear_layout.LinearLayout(self.parent, id=id_)

    # ************************操作***************************

    def tap_user_head_bar(self, timeout=10):
        """
            Summary:
                点击用户头部信息栏
            Args:
                timeout:等待时长
        """
        log.logger.info("开始点击个人中心-头部信息栏")
        self.user_head_bar.tap()
        if self.wait_activity(activities.ActivityNames.USER_INFO, timeout):
            log.logger.info("成功进入个人信息设置页")
            return True
        else:
            log.logger.error("进入个人信息设置页失败")
            return False

    def tap_paster_bar(self, timeout=10):
        """
            Summary:
                点击贴纸栏
            Args:
                timeout:等待时长
        """
        log.logger.info("开始点击个人中心-贴纸栏")
        self.paster_bar.tap()
        if self.wait_activity(activities.ActivityNames.PASTER_MALL, timeout):
            log.logger.info("成功进入贴纸商城页")
            return True
        else:
            log.logger.error("进入贴纸商城页失败")
            return False

    def tap_friends_bar(self, timeout=10):
        """
            Summary:
                点击我的好友
            Args:
                timeout:等待时长
        """
        log.logger.info("开始点击个人中心-我的好友")
        self.my_friends_bar.tap()
        if self.wait_activity(activities.ActivityNames.USER_CENTER_FRIEND, timeout):
            log.logger.info("成功进入我的好友")
            return True
        else:
            log.logger.error("点击进入我的好友页失败")
            return False

    def tap_settings_bar(self, timeout=10):
        """
            Summary:
                点击设置栏
            Args:
                timeout:等待时长
        """
        log.logger.info("开始点击个人中心-设置")
        self.setting_bar.tap()
        if self.wait_activity(activities.ActivityNames.USER_SETTING, timeout):
            log.logger.info("成功进入用户设置页")
            return True
        else:
            log.logger.error("点击设置进入用户设置页失败")
            return False
    
    def swipe_up_entire_scroll_view(self):
        """
            Summary:
                向上滑动整个scroll view的高度

        """
        location = self._scroll_view.location
        size = self._scroll_view.size
        x = location['x'] + 2
        start_y = location['y'] + size['height'] - 1
        end_y = location['y'] + 1

        log.logger.info("开始向上滑动整个可滑动区域的屏幕")
        self.swipe_up(x, start_y, end_y)
        log.logger.info("向上滑动结束")

    def swipe_down_entire_scroll_view(self):
        """
            Summary:
                向下滑动整个scroll view的高度
        """
        location = self._scroll_view.location
        size = self._scroll_view.size
        x = location['x'] + 2
        end_y = location['y'] + size['height'] - 1
        start_y = location['y'] + 1

        log.logger.info("开始向下滑动整个可滑动区域的屏幕")
        self.swipe_up(x, start_y, end_y)
        log.logger.info("向下滑动结束")