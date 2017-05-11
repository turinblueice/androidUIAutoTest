#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 故事设置页

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


class StorySettingActivity(base_frame_view.BaseFrameView):

    """
        Summary:
            发布故事集-故事设置页

        Attributes:

    """
    name = '.story.activity.StorySettingActivity'  # 用户设置页的activity名称

    def __init__(self, parent):
        super(StorySettingActivity, self).__init__(parent)

        # 滑动区域
        self._scroll_view = recycler_view.RecyclerView(
            self.parent, id='com.jiuyan.infashion:id/rv_story_set_story')

    @property
    def title(self):
        """
            Summary:
                标题-编辑故事
        """
        id_ = "com.jiuyan.infashion:id/tv_egg"
        return text_view.TextView(self.parent, id=id_).text

    @property
    def back_button(self):
        """
            Summary:
                后退按钮
        """
        id_ = "com.jiuyan.infashion:id/iv_story_set_cancel"
        return image_view.ImageView(self.parent, id=id_)

    @property
    def finish_button(self):
        """
            Summary:
                完成按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/tv_story_set_done'
        return text_view.TextView(self.parent, id=id_)

    @property
    def diary_name_edit_box(self):
        """
            Summary:
                故事名称编辑框
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/tv_story_set_name'
        return edit_text.EditText(self._scroll_view, id=id_)

    @property
    def diary_cover_date(self):
        """
            Summary:
                故事时间
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/tv_story_set_date'
        return text_view.TextView(self._scroll_view, id=id_)

    @property
    def diary_cover_location(self):
        """
            Summary:
                故事地点
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/tv_story_set_place'
        return text_view.TextView(self._scroll_view, id=id_)

    @property
    def privacy_setting_bar(self):
        """
            Summary:
                隐私设置栏
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/rl_story_cover_set'
        return relative_layout.RelativeLayout(self._scroll_view, id=id_)

    @property
    def category_list(self):
        """
            Summary:
                分类列表
        """
        id_ = 'com.jiuyan.infashion:id/rl_story_set_item'
        return relative_layout.RelativeLayoutList(self.parent, id=id_).relative_layout_list

    # ************************操作***************************

    def tap_finish_button(self):
        """
            Summary:
                点击完成按钮
        :return:
        """
        log.logger.info("开始点击完成按钮")
        self.finish_button.tap()
        log.logger.info("点击完毕")
        if self.wait_activity(activities.ActivityNames.STORY_SHARE, 10):
            log.logger.info("成功进入故事分享页")
            return True
        log.logger.error("进入故事分享页失败")
        return False

    def select_category(self, index):
        """
            Summary:
                选择类别
            Args:
                index: 类别序号
        """
        log.logger.info("开始点击第{}个类目".format(index))
        self.category_list[index-1].tap()
        time.sleep(1)
        log.logger.info("完成点击")

    def is_category_selected(self, index):
        """
            Summary:
                判断类目是否选中
            Args:
                index： 序号
        """
        if self.wait_for_element_present(self.category_list[index-1],
                                         id='com.jiuyan.infashion:id/iv_story_set_type_select'):
            return True
        return False