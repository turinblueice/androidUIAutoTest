#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 登录的引导页

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


class LoginGuideCameraActivity(base_frame_view.BaseFrameView):

    """
    Summary:
        登陆引导页

    Attributes:
        parent: 该活动页的父亲framework

    """

    name = '.login.activity.GuideCameraActivity'

    def __init__(self, parent):
        super(LoginGuideCameraActivity, self).__init__(parent)

    @property
    def camera_guide_login(self):
        """
            Summary:
                登录页的摄像头
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/iv_guide_camera'
        return image_view.ImageView(self.parent, id=id_)

    @property
    def skip_guide_login_button(self):
        """
            Summary:
                登录引导页的跳过，首次安装会出现
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/tv_guide_skip'
        return text_view.TextView(self.parent, id=id_)

    @property
    def skip_dialogue_button(self):
        """
            Summary:
                弹出框的跳过按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/dialog_guide_camera_cancel'
        return text_view.TextView(self.parent, id=id_)

    @property
    def take_a_photo_dialogue_button(self):
        """
            Summary:
                弹出框的’拍一张‘按钮
        """
        id_ = 'com.jiuyan.infashion:id/dialog_guide_camera_confirm'
        return text_view.TextView(self.parent, id=id_)

    # ***********************操作方法*********************************

    def tap_skip_button(self, skip=True):
        """
            Summary:
                跳过引导
            Args:
                skip:True:点击提示框的跳过按钮，False：点击提示框的拍一张按钮
        """
        log.logger.info("点击跳过引导页")
        self.skip_guide_login_button.tap()
        log.logger.info("点击完毕")
        try:
            WebDriverWait(self.base_parent, 10).until(
                EC.presence_of_element_located(
                    (MobileBy.ID, 'com.jiuyan.infashion:id/dialog_guide_camera_content'))
            )
            log.logger.info("弹出了提示框")
            if skip:
                log.logger.info("点击提示框的跳过按钮")
                self.skip_dialogue_button.tap()
                log.logger.info("点击完毕")
                if self.wait_activity(activities.ActivityNames.IN_MAIN, 10):
                    log.logger.info("成功进入In主页")
                    return True
                log.logger.error("进入In主页失败")
                return False
            else:
                log.logger.info("点击拍一张按钮")
                self.take_a_photo_dialogue_button.tap()
                log.logger.info("点击完毕")
                if self.wait_activity(activities.ActivityNames.PHOTO_STORY_GALLERY, 10):
                    log.logger.info("成功进入图片选择页")
                    return True
                log.logger.error("进入图片选择页失败")
                return False
        except TimeoutException:
            log.logger.error("没有出现提示框")
            return False

