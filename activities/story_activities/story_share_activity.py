#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 故事分享页

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


class StoryShareActivity(base_frame_view.BaseFrameView):

    """
        Summary:
            发布故事集-故事分享页

        Attributes:

    """
    name = '.story.activity.StoryShareActivity2'  # 用户设置页的activity名称

    def __init__(self, parent):
        super(StoryShareActivity, self).__init__(parent)

    @property
    def publish_success_tips(self):
        """
            Summary:
                发布成功提示——"发布成功"
        """
        return text_view.TextView(self.parent, type='android.widget.TextView').text

    @property
    def close_button(self):
        """
            Summary:
                关闭按钮
        """
        id_ = "com.jiuyan.infashion:id/iv_story_share_close"
        return image_view.ImageView(self.parent, id=id_)

    @property
    def wechat_button(self):
        """
            Summary:
                微信好友按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/tv_story_share_wechat'
        return text_view.TextView(self.parent, id=id_)

    @property
    def moments_button(self):
        """
            Summary:
                朋友圈按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/tv_story_share_moments'
        return text_view.TextView(self._scroll_view, id=id_)

    @property
    def weibo_button(self):
        """
            Summary:
                微博按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/tv_story_share_sina'
        return text_view.TextView(self.parent, id=id_)

    @property
    def qq_button(self):
        """
            Summary:
                QQ按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/tv_story_share_qq'
        return text_view.TextView(self.parent, id=id_)

    @property
    def qzone_button(self):
        """
            Summary:
                QQ空间按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/tv_story_share_qzone'
        return text_view.TextView(self.parent, id=id_)

    @property
    def save_picture_button(self):
        """
            Summary:
                保存长图按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/tv_story_save_long_pic'
        return text_view.TextView(self.parent, id=id_)

    @property
    def print_story_button(self):
        """
            Summary:
                打印故事集
        """
        id_ = 'com.jiuyan.infashion:id/tv_story_print'
        return text_view.TextView(self.parent, id=id_)

    # ************************操作***************************

    def tap_close_button(self):
        """
            Summary:
                点击关闭按钮
        :return:
        """
        log.logger.info("开始点击关闭按钮")
        self.close_button.tap()
        log.logger.info("点击完毕")
        if self.wait_activity(activities.ActivityNames.STORY_DETAIL, 10):
            log.logger.info("成功进入故事详情页")
            return True
        log.logger.error("进入故事详情页失败")
        return False

    def is_publish_success(self):
        """
            Summary:
                是否发布成功
        :return:
        """
        try:
            WebDriverWait(self.base_parent, 10).until(
                EC.text_to_be_present_in_element((MobileBy.CLASS_NAME, 'android.widget.TextView'), u'发布成功')
            )
            return True
        except TimeoutException:
            return False