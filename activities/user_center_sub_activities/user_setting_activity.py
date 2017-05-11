#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 用户中心-设置页面

Authors: Turinblueice
Date: 2016/7/27
"""
from base import base_frame_view
from util import log
from gui_widgets.basic_widgets import image_view
from gui_widgets.basic_widgets import text_view
from gui_widgets.basic_widgets import relative_layout
from gui_widgets.basic_widgets import linear_layout
from gui_widgets.basic_widgets import radio_button
from gui_widgets.basic_widgets import grid_view
from gui_widgets.basic_widgets import scroll_view
from gui_widgets.custom_widgets import alert

from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from activities import activities

import time


class UserSettingActivity(base_frame_view.BaseFrameView):

    """
        Summary:
            用户中心-设置页面

        Attributes:

    """
    name = '.usercenter.activity.setting.UserCenterSettingActivity'  # 用户设置页的activity名称

    def __init__(self, parent):
        super(UserSettingActivity, self).__init__(parent)
        self._scroll_view = scroll_view.ScrollView(self.parent, type='android.widget.ScrollView')

    @property
    def title_bar(self):
        """
            Summary:
                标题-设置
        """
        id_ = "com.jiuyan.infashion:id/title_bar"
        return text_view.TextView(self.parent, id=id_)

    @property
    def logout_bar(self):
        """
            Summary:
                退出栏
        """
        id_ = "com.jiuyan.infashion:id/rl_usercenter_logout"
        return relative_layout.RelativeLayout(self.parent, id=id_)

    # ************************操作***************************

    def tap_logout_bar(self, accept=True, timeout=10):
        """
            Summary:
                点击退出
            Args:
                accept: True:点击提示框的确认退出;False:点击提示框的取消退出
                timeout:等待时长
        """
        log.logger.info("开始点击退出登录")
        self.logout_bar.tap()
        log.logger.info("等待提示框弹出")
        WebDriverWait(self.base_parent, timeout).until(
            EC.presence_of_element_located((MobileBy.ID, 'android:id/parentPanel'))
        )
        curr_alert = alert.Alert(self.base_parent)
        if accept:
            log.logger.info("开始点击确认退出按钮")
            curr_alert.confirm_button.tap()
            if self.wait_activity(activities.ActivityNames.LOGIN_MAIN, timeout):
                log.logger.info("成功退出登录")
                return True
            else:
                log.logger.info("退出登录失败")
                return False
        else:
            log.logger.info("开始点击取消按钮")
            curr_alert.cancel_button.tap()
            if self.wait_activity(self.name, timeout):
                log.logger.info("成功取消退出登录")
                return True
            else:
                log.logger.info("取消退出登录失败")
                return False


