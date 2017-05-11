#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 发布-文字标签页

Authors: Turinblueice
Date: 2016/7/27
"""
from base import base_frame_view
from util import log

from gui_widgets.basic_widgets import text_view
from gui_widgets.basic_widgets import recycler_view
from gui_widgets.basic_widgets import image_view
from gui_widgets.basic_widgets import relative_layout
from gui_widgets.basic_widgets import linear_layout
from gui_widgets.basic_widgets import edit_text
from activities import activities

from appium.webdriver import WebElement
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


class PublishWordsTagActivity(base_frame_view.BaseFrameView):

    """
        Summary:
            发布-文字标签页

        Attributes:

    """
    name = '.publish.component.tag.PublishTagActivity'

    def __init__(self, parent):
        super(PublishWordsTagActivity, self).__init__(parent)
        self.__words_tag = None

    @property
    def back_button(self):
        """
            Summary:
                返回按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/tv_publish_tag_previous'
        return text_view.TextView(self.parent, id=id_)

    @property
    def icon_list(self):
        """
            Summary:
                表情列表
        """
        xpath_ = '//android.widget.GridView[1]/android.widget.LinearLayout'
        return linear_layout.LinearLayoutList(
            self.base_parent, xpath=xpath_).layout_list

    @property
    def edit_box(self):
        """
            Summary:
                文本输入框
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/et_tag_content'
        return edit_text.EditText(self.parent, id=id_)

    @property
    def add_button(self):
        """
            Summary:
                添加按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/tv_tag_add'
        return text_view.TextView(self.parent, id=id_)

    @property
    def icon_button(self):
        """
            Summary:
                表情显/隐按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/iv_tag_icon'
        return image_view.ImageView(self.parent, id=id_)

    # **************************操作方法******************************

    def input_words(self, values):
        """
            Summary:
                输入文字
        :return:
        """
        self.__words_tag = values
        log.logger.info("开始输入文字，说点什么")
        self.edit_box.clear_text_field()
        self.edit_box.send_keys(values)
        time.sleep(2)
        log.logger.info("完成输入")

    def tap_add_button(self):
        """
            Summray:
                点击添加按钮
        """
        log.logger.info("开始点击添加按钮")
        self.add_button.tap()
        log.logger.info("完成添加按钮点击")
        if self.wait_activity(activities.ActivityNames.PUBLISH_CORE, 10):
            log.logger.info("成功进入发布加工页")
            return True
        log.logger.error("进入发布加工页失败")
        return False

    def is_tag_added_successful(self):
        """
            Summary:
                是否添加成功
        :return:
        """

        tags = self.find_elements(id='com.jiuyan.infashion:id/tv_tag_right')

        words_tag = unicode(self.__words_tag, 'utf8') \
            if not isinstance(self.__words_tag, unicode) else self.__words_tag
        for tag in tags:
            if words_tag in tag.text:
                return True
        return False

