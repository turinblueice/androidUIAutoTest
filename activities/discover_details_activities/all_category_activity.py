#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明:全部分类页

Authors: Turinblueice
Date: 2016/9/10
"""

from base import base_frame_view
from util import log

from gui_widgets.basic_widgets import frame_layout
from gui_widgets.basic_widgets import image_view
from gui_widgets.basic_widgets import scroll_view
from gui_widgets.basic_widgets import text_view
from gui_widgets.basic_widgets import linear_layout
from gui_widgets.basic_widgets import recycler_view

from appium.webdriver import WebElement
from appium.webdriver.common import touch_action
from selenium.webdriver.common.touch_actions import TouchActions
from activities import activities
import time


class AllCategoryActivity(base_frame_view.BaseFrameView):

    """
        Summary:
            全部分类页面

        Attributes:

    """
    name = '.module.square.activity.SquareCategoryActivity'

    def __init__(self, parent):
        super(AllCategoryActivity, self).__init__(parent)
        self._scroll_view = scroll_view.ScrollView(self.parent, type='android.widget.ScrollView')

    @property
    def near_by(self):
        """
            Summary:
                附近的人
        """
        id_ = 'com.jiuyan.infashion:id/iv_square_nearby'
        return image_view.ImageView(self.parent, id=id_)

    @property
    def topic_square(self):
        """
            Summary:
                话题分类
        """
        id_ = 'com.jiuyan.infashion:id/iv_square_label'
        return image_view.ImageView(self.parent, id=id_)

    @property
    def talent(self):
        """
            Summary:
                达人分类
        """
        id_ = 'com.jiuyan.infashion:id/iv_square_favorite'
        return image_view.ImageView(self.parent, id=id_)

    @property
    def brand(self):
        """
            Summary:
                品牌专区
        """
        id_ = 'com.jiuyan.infashion:id/iv_square_brand'
        return image_view.ImageView(self.parent, id=id_)

    @property
    def near_by(self):
        """
            Summary:
                附近的人
        """
        id_ = 'com.jiuyan.infashion:id/iv_square_nearby'
        return image_view.ImageView(self.parent, id=id_)

    @property
    def back_button(self):
        """
            Summary:
                返回按钮
        """
        id_ = 'com.jiuyan.infashion:id/layout_left'
        return frame_layout.FrameLayout(self.parent, id=id_)

    # ***********************精选分类******************************

    @property
    def category_list(self):
        """
            Summary:
                精选分类列表
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/tv_square_category_content'
        return text_view.TextViewList(self.parent, id=id_).text_view_list

    # **************************操作方法*****************************

    def tap_talent(self):
        """
            Summary:
                点击达人分类
        Returns:

        """
        log.logger.info("开始点击达人分类")
        self.talent.tap()
        log.logger.info("点击完毕")
        if self.wait_activity(activities.ActivityNames.TALENT_RECOMMEND, 10):
            log.logger.info("成功进入达人推荐页面")
            return True
        log.logger.error("进入达人推荐页面失败")
        return False
