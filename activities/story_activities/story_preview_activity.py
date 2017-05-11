#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 故事预览页

Authors: Turinblueice
Date: 2016/7/27
"""
from base import base_frame_view
from util import log
from gui_widgets.basic_widgets import image_view
from gui_widgets.basic_widgets import text_view
from gui_widgets.basic_widgets import relative_layout
from gui_widgets.basic_widgets import edit_text
from gui_widgets.basic_widgets import linear_layout
from gui_widgets.basic_widgets import button
from gui_widgets.basic_widgets import frame_layout
from gui_widgets.basic_widgets import scroll_view
from gui_widgets.basic_widgets import recycler_view
from gui_widgets.custom_widgets import alert

from activities.common_activities import photo_picker_activity
from activities.common_activities import cropper_image_activity

from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from activities import activities

import time
import random


class StoryPreviewActivity(base_frame_view.BaseFrameView):

    """
        Summary:
            发布故事集-故事预览页

        Attributes:

    """
    name = '.story.activity.StoryDetailsAct'  # 用户设置页的activity名称

    def __init__(self, parent):
        super(StoryPreviewActivity, self).__init__(parent)

        # 滑动区域
        self._scroll_view = linear_layout.LinearLayout(
            self.parent, id='com.jiuyan.infashion:id/story_detail_zoom_rcyv')

    @property
    def next_button(self):
        """
            Summary:
                预览按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/story_detail_title_publish_btn'
        return text_view.TextView(self.parent, id=id_)

    # ************************操作***************************

    def tap_next_button(self):
        """
            Summary:
                点击下一步按钮
        :return:
        """
        log.logger.info("开始点击下一步按钮")
        self.next_button.tap()
        log.logger.info("点击完毕")
        if self.wait_activity(activities.ActivityNames.STORY_SETTING, 10):
            log.logger.info("成功进入故事设置页")
            return True
        log.logger.error("进入故事设置页失败")
        return False
