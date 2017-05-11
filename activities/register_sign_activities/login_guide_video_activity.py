#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 登录的视频引导页

Authors: Turinblueice
Date: 2016/7/26
"""

from base import base_frame_view
from util import log

from gui_widgets.basic_widgets import text_view
from gui_widgets.basic_widgets import image_view
from gui_widgets.basic_widgets import button
from gui_widgets.basic_widgets import recycler_view

from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from activities import activities
from selenium.common.exceptions import TimeoutException

import time


class LoginGuideVideoActivity(base_frame_view.BaseFrameView):

    """
    Summary:
        登陆视频引导页

    Attributes:
        parent: 该活动页的父亲framework

    """

    name = '.login.activity.VideoGuideActivity'

    def __init__(self, parent):
        super(LoginGuideVideoActivity, self).__init__(parent)

    @property
    def skip_button(self):
        """
            Summary:
                跳过
        :return:
        """
        # id_ = 'com.jiuyan.infashion:id/iv_guide_skip'

        return image_view.ImageView(self.base_parent, type='android.widget.ImageView')

    # **********************弹出提示框**************************

    @property
    def dialogue_cancel_button(self):
        """
            Summary:
                我就要走按钮
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/in_base_dialog_cancel'
        return text_view.TextView(self.parent, id=id_)

    @property
    def dialogue_ok_button(self):
        """
            Summary:
                留下来玩按钮
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/in_base_dialog_ok'
        return text_view.TextView(self.parent, id=id_)

    # ***********************操作方法*********************************

    def tap_skip_button(self, skip=True):
        """
            Summary:
                跳过引导
            Args:
                skip:True:点击提示框的跳过按钮，False：点击提示框的拍一张按钮
        """
        log.logger.info("点击跳过视频引导页")
        if self.wait_for_element_present(self.parent, id='com.jiuyan.infashion:id/iv_guide_skip'):
            self.skip_button.tap()
            log.logger.info("点击完毕")
            try:
                WebDriverWait(self.base_parent, 10).until(
                    EC.presence_of_element_located(
                        (MobileBy.ID, 'com.jiuyan.infashion:id/in_base_dialog_content'))
                )
                log.logger.info("弹出了提示框")
                if skip:
                    log.logger.info("点击提示框的\"我就要走\"按钮")
                    self.dialogue_cancel_button.tap()
                    log.logger.info("点击完毕")
                    if self.wait_activity(activities.ActivityNames.LOGIN_FRIEND_RECOMMEND, 10):
                        log.logger.info("成功进入好友推荐页")
                        return True
                    log.logger.error("进入好友推荐页失败")
                    return False
                else:
                    log.logger.info("点击\"留下来玩\"按钮")
                    self.dialogue_ok_button.tap()
                    log.logger.info("点击完毕")
                    return True

            except TimeoutException:
                log.logger.error("没有出现提示框")
                return False
        log.logger.error("跳过引导按钮未出现")
        return False

