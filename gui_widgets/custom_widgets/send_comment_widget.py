#-*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明:该模块为底部发表评论组件
 
Authors: Turinblueice
Date:    16/3/16 16:46
"""

from base import base_frame_view
from gui_widgets.basic_widgets import relative_layout
from gui_widgets.basic_widgets import edit_text
from gui_widgets.basic_widgets import text_view

from util import log

from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from activities import activities

from selenium.common import exceptions

import time


class SendCommentWidget(base_frame_view.BaseFrameView):
    """
        Summary:
            底部发表评论组件
    """

    def __init__(self, parent, **kwargs):
        super(SendCommentWidget, self).__init__(parent)
        self.__id = "com.jiuyan.infashion:id/comment_box"

        if kwargs:
            self._layout_view = self.find_element(**kwargs)
        else:
            self._layout_view = self.find_element(id=self.__id)

    @property
    def edit_box(self):
        """
            Summary:
                文本框
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/et_content'
        return edit_text.EditText(self.base_parent, id=id_)

    @property
    def send_button(self):
        """
            Summary:
                发送按钮
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/tv_send'
        return text_view.TextView(self.base_parent, id=id_)

    # ********************* 操作方法************************

    def input_words(self, value):
        """
            Summary:
                输入文字
            Args：
                value:文字
        """
        log.logger.info("开始输入文字")
        self.edit_box.clear_text_field()
        self.edit_box.send_keys(value)
        log.logger.info("文字输入完毕")
        time.sleep(2)

    def tap_send_button(self):
        """
            Summary:
                点击发送按钮
        """
        log.logger.info("开始点击发送按钮")
        self.send_button.tap()
        log.logger.info("发送按钮点击完毕")
        time.sleep(2)