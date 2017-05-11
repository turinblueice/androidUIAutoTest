#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: QQ授权登录页

Authors: Turinblueice
Date: 2016/7/27
"""
from base import base_frame_view
from util import log

from gui_widgets.basic_widgets import button

from activities import activities
from appium.webdriver import WebElement
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import time


class QQAuthActivity(base_frame_view.BaseFrameView):

    """
        Summary:
            QQ授权登录页

        Attributes:

    """
    name = 'com.tencent.open.agent.AuthorityActivity'

    def __init__(self, parent):
        super(QQAuthActivity, self).__init__(parent)
        # 等待授权信息加载完毕
        WebDriverWait(self.base_parent, 10).until(
            EC.presence_of_element_located(
                (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("你已对该应用授权")')
            )
        )


    @property
    def login_button(self):
        """
            Summary:
                登录按钮
        Returns:

        """
        uiautomator_ = 'new UiSelector().text("登录")'
        return button.Button(self.parent, uiautomator=uiautomator_)

    def tap_login_button(self):
        """
            Summary:
                点击QQ登录
        Returns:

        """
        log.logger.info("开始点击登录")
        self.login_button.tap()
        log.logger.info("完成点击")
        if self.wait_activity(activities.ActivityNames.LOGIN_FRIEND_RECOMMEND, 10):
            log.logger.info("成功进入好友推荐页")
            return True
        log.logger.info("进入好友推荐页失败")
        return False

