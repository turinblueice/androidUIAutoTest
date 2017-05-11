#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 图片发布页

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


class PublishActivity(base_frame_view.BaseFrameView):

    """
        Summary:
            图片发布页

        Attributes:

    """
    name = '.publish.component.publish.activity.PublishActivity'

    def __init__(self, parent):
        super(PublishActivity, self).__init__(parent)

    @property
    def back_button(self):
        """
            Summary:
                返回按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/publish_send_header_back'
        return image_view.ImageView(self.parent, id=id_)

    @property
    def photo_available_list(self):
        """
            Summary:
                顶栏图片列表
        """
        recycler_view_ = recycler_view.RecyclerView(self.parent, id='com.jiuyan.infashion:id/rv_publish_photos')
        return relative_layout.RelativeLayoutList(
            recycler_view_, type='android.widget.RelativeLayout').relative_layout_list

    @property
    def edit_box(self):
        """
            Summary:
                文本输入框
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/et_input'
        return edit_text.EditText(self.parent, id=id_)


    @property
    def publish_button(self):
        """
            Summary:
                完成按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/pub_body_send_bar'
        return linear_layout.LinearLayout(self.parent, id=id_)

    @property
    def at_button(self):
        """
            Summary:
                “@”按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/tv_at_btn'
        return text_view.TextView(self.parent, id=id_)

    @property
    def privacy_button(self):
        """
            Summary:
                公开按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/ll_privacy_layout'
        return linear_layout.LinearLayout(self.parent, id=id_)

    @property
    def location_button(self):
        """
            Summary:
                添加位置按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/ll_location_layout'
        return linear_layout.LinearLayout(self.parent, id=id_)

    @property
    def topic_button(self):
        """
            Summary:
                添加话题按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/tv_add_topic_btn'
        return text_view.TextView(self.parent, id=id_)

    # **************************操作方法******************************
    def tap_back_button(self):
        """
            Summary:
                点击返回按钮
        Returns:

        """
        log.logger.info('点击返回按钮')
        self.back_button.tap()
        log.logger.info("完成返回按钮的点击")
        if self.wait_activity(activities.ActivityNames.PUBLISH_CORE, 10):
            log.logger.info("回到发布加工页")
            return True
        log.logger.error("回到发布加工页失败")
        return False

    def input_words(self, *values):
        """
            Summary:
                输入文字
        :return:
        """
        log.logger.info("开始输入文字，说点什么")
        self.edit_box.clear_text_field()
        self.edit_box.send_keys(*values)
        time.sleep(2)
        log.logger.info("完成输入")

    def tap_publish_button(self):
        """
            Summray:
                点击完成按钮
        """
        log.logger.info("开始点击发布按钮")
        self.publish_button.tap()
        log.logger.info("完成发布按钮点击")
        if self.wait_activity(activities.ActivityNames.IN_MAIN, 10):
            log.logger.info("成功进入发布页")
            return True
        log.logger.error("进入发布页失败")
        return False

    def is_publish_successful(self):
        """
            Summary:
                是否发布成功
        :return:
        """
        try:
            WebDriverWait(self.base_parent, 15).until(
                EC.text_to_be_present_in_element(
                    (MobileBy.ID, 'com.jiuyan.infashion:id/share_head_title'), u'发布成功')
            )
            return True
        except TimeoutException:
            return False
