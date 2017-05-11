#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 登录的好友推荐页

Authors: Turinblueice
Date: 2016/7/26
"""

from base import base_frame_view
from util import log
from gui_widgets.basic_widgets import frame_layout
from gui_widgets.basic_widgets import image_button
from gui_widgets.basic_widgets import image_view
from gui_widgets.basic_widgets import text_view
from gui_widgets.basic_widgets import edit_text
from gui_widgets.basic_widgets import button
from gui_widgets.basic_widgets import recycler_view

from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from activities import activities
from selenium.common.exceptions import TimeoutException

import time


class LoginFriendRecommendActivity(base_frame_view.BaseFrameView):

    """
    Summary:
        登陆活动页

    Attributes:
        parent: 该活动页的父亲framework

    """

    name = '.login.activity.FriendRecommendActivity'

    def __init__(self, parent):
        super(LoginFriendRecommendActivity, self).__init__(parent)

        self._scroll_view = recycler_view.RecyclerView(
            self.parent, id='com.jiuyan.infashion:id/login_srl_recommend_friend')

    @property
    def title(self):
        """
            Summary:
                标题
        """
        id_ = 'com.jiuyan.infashion:id/login_tv_title'
        return text_view.TextView(self.parent, id=id_).text

    @property
    def finish_button(self):
        """
        Summary:
            完成按钮
        """
        id_ = 'com.jiuyan.infashion:id/login_tv_title_right'
        return text_view.TextView(self.parent, id=id_)

    @property
    def find_friend_in_contact_button(self):
        """
            Summary:
                找一找通讯录好友
        """
        id_ = 'com.jiuyan.infashion:id/tv_recommend_find_friend_in_contact'
        return text_view.TextView(self.parent, id=id_)

    # ***********************操作方法*********************************

    def tap_finish_button(self):
        """
            Summary:
                点击完成按钮
        """
        log.logger.info("开始点击完成按钮")
        self.finish_button.tap()
        log.logger.info("结束完成按钮点击")
        if self.wait_one_of_activities(
                (activities.ActivityNames.IN_MAIN, activities.ActivityNames.LOGIN_GUIDE_CAMERA), 10):
            log.logger.info("成功进入主页或者引导页")
            return True
        log.logger.error("进入主页失败")
        return False
